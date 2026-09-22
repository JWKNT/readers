/* A navigable book, not a reading account. No stored position or personal-data UI. */
'use strict';
(() => {
  const $ = (s, p=document) => p.querySelector(s);
  const $$ = (s, p=document) => [...p.querySelectorAll(s)];
  const state = {manifest:null, chapter:null, terms:new Map(), cache:new Map(), search:null, token:0, loading:false};
  const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const norm = s => String(s).toLocaleLowerCase().replace(/[‘’]/g,"'").replace(/[“”]/g,'"');
  const clamp = (n,a,b) => Math.max(a,Math.min(b,n));
  const debounce = (f,delay) => {let t;return (...args)=>{clearTimeout(t);t=setTimeout(()=>f(...args),delay);};};
  const sourceWording = new URLSearchParams(location.search).get('wording')==='source';
  const edition = new URL(document.currentScript?.src || location.href).searchParams.get('v');
  const desktop = matchMedia('(min-width:920px)');
  let anchor=null, showTimer=null, closeTimer=null, ignoreFocus=null, scrollFrame=null, searchSequence=0;
  const popup=$('#word-popup');
  let marginItems=[], marginFrame=null;
  const svgNS='http://www.w3.org/2000/svg';
  async function getJSON(path) {
    const url = new URL(path, location.href);
    if(edition)url.searchParams.set('edition',edition);
    const r=await fetch(url,{credentials:'same-origin'});
    if(!r.ok)throw new Error(`${path}: HTTP ${r.status}`);
    return r.json();
  }
  function route() {try {const [chapter,paragraph]=decodeURIComponent(location.hash.slice(1)).split('/');return {chapter,paragraph};} catch {return {};}}
  function chapter(id) {return state.manifest?.chapters.find(c=>c.id===id);}
  function closeDialogs() {$$('dialog[open]').forEach(d=>d.close());}
  function showError(error) {
    const p=$('#error-panel');p.hidden=false;p.replaceChildren();
    const text=document.createElement('p');text.textContent=location.protocol==='file:'?'Serve this folder with the local HTTP command in README.md.':`This chapter could not be loaded. ${error.message}`;
    const a=document.createElement('a');a.href='contents.html';a.textContent='Read the ordinary HTML edition';p.append(text,a);
  }
  function toc(container) {
    container.replaceChildren();
    for(const v of state.manifest.volumes) {
      const detail=document.createElement('details');detail.dataset.volume=v.id;
      const head=document.createElement('summary');head.textContent=v.title.replace(/^The /,'');detail.append(head);
      const ul=document.createElement('ul');
      for(const c of state.manifest.chapters.filter(c=>c.volume===v.id&&c.kind!=='reference')) {
        const li=document.createElement('li'),a=document.createElement('a');a.href='#'+c.id;a.dataset.chapter=c.id;
        a.innerHTML=`<span class="chapter-number">${esc(c.label||'—')}</span><span>${esc(c.title)}</span>`;li.append(a);ul.append(li);
      }
      const refs=state.manifest.chapters.filter(c=>c.volume===v.id&&c.kind==='reference');
      if(refs.length){const more=document.createElement('details');more.className='source-matter';const summary=document.createElement('summary');summary.textContent='Names in the text';more.append(summary);for(const c of refs){const a=document.createElement('a');a.href='#'+c.id;a.dataset.chapter=c.id;a.textContent=c.title;more.append(a);}detail.append(ul,more);}else detail.append(ul);
      container.append(detail);
    }
  }

  function markCurrent() {
    for(const c of $$('.toc a[data-chapter]')) {
      const active=c.dataset.chapter===state.chapter.id;
      if(active){c.setAttribute('aria-current','page');for(let d=c.closest('details');d;d=d.parentElement.closest('details'))d.open=true;}
      else c.removeAttribute('aria-current');
    }
    const el=$('#desktop-contents a[aria-current]');
    if(el){const rail=$('#desktop-contents');const r=el.getBoundingClientRect(),b=rail.getBoundingClientRect();if(r.bottom>b.bottom||r.top<b.top)rail.scrollTop+=r.top-b.top-rail.clientHeight/3;}
  }
  function progress() {
    if(!state.chapter||state.loading)return;
    const blocks=$$('[data-block]',$('#chapter-body'));
    const el=blocks.find(e=>e.getBoundingClientRect().bottom>35)||blocks.at(-1);
    if(!el)return;
    const box=el.getBoundingClientRect();const offset=clamp((35-box.top)/Math.max(1,box.height),0,1);
    const i=Math.max(0,state.chapter.blocks.indexOf(el.id));
    const fraction=(i+offset)/Math.max(1,blocks.length);
    const contributes=state.chapter.kind!=='reference';
    const pct=clamp((state.chapter.startWords+(contributes?fraction*state.chapter.words:0))/state.manifest.totalWords*100,0,100);
    $('#progress-label').textContent=pct.toFixed(1)+'%';$('#progress-fill').style.width=pct+'%';
    $('#reading-progress').setAttribute('aria-valuenow',pct.toFixed(1));
    $('#position-label').textContent=(state.chapter.label?state.chapter.label+' · ':'')+state.chapter.title;
    // The visible address can identify a paragraph; nothing is saved in browser storage.
  }
  function turns() {
    const all=state.manifest.chapters.filter(c=>c.kind!=='reference');const i=all.findIndex(c=>c.id===state.chapter.id);const nav=$('#chapter-turns');nav.replaceChildren();if(i<0)return;
    for(const [c,previous] of [[all[i-1],true],[all[i+1],false]]) {
      if(!c)continue;const a=document.createElement('a');a.href='#'+c.id;
      a.textContent=previous?'← '+c.title:c.title+' →';a.rel=previous?'prev':'next';nav.append(a);
    }
  }
  function activateNotes() {
    for(const el of $$('.word[data-first="true"]',$('#chapter-body'))) {
      if(!state.terms.has(el.dataset.term))continue;
      el.tabIndex=0;el.setAttribute('role','button');el.setAttribute('aria-haspopup','dialog');el.setAttribute('aria-expanded','false');
      el.setAttribute('aria-label',el.textContent+' — definition');
    }
    for(const img of $$('.initial-image'))img.addEventListener('error',()=>img.closest('.initial')?.classList.add('initial-failed'),{once:true});
  }

  function setActiveTerm(id) {
    for(const el of $$('.word.is-active,.margin-note.is-active,.note-leaders path.is-active')) {
      if(el.matches('.word,.margin-note,.note-leaders path'))el.classList.remove('is-active');
    }
    if(!id)return;
    for(const el of $$('.word[data-first="true"],.margin-note,.note-leaders path'))if(el.dataset.term===id)el.classList.add('is-active');
  }
  function wordRect(el) {
    const rects=[...el.getClientRects()].filter(r=>r.width>0&&r.height>0);
    return rects.find(r=>r.height<48)||rects[0]||el.getBoundingClientRect();
  }
  function makeSidenotes() {
    $('#sidenotes').replaceChildren();$('#note-leaders').replaceChildren();marginItems=[];
    for(const word of $$('.word[data-first="true"][tabindex]',$('#chapter-body'))) {
      const term=state.terms.get(word.dataset.term);if(!term)continue;
      const note=document.createElement('section');note.className='margin-note';note.dataset.term=term.id;
      const head=document.createElement('button');head.type='button';head.className='margin-term';head.dataset.term=term.id;
      head.textContent=term.term;head.setAttribute('aria-haspopup','dialog');head.setAttribute('aria-expanded','false');
      head.setAttribute('aria-label',term.term+' — more detail and sources');
      const gloss=document.createElement('p');gloss.textContent=term.short||term.note;
      note.append(head,gloss);$('#sidenotes').append(note);
      const line=document.createElementNS(svgNS,'path'),trace=document.createElementNS(svgNS,'path');
      line.dataset.term=term.id;trace.dataset.term=term.id;trace.classList.add('leader-trace');
      $('#note-leaders').append(line,trace);marginItems.push({word,note,head,line,trace});
    }
    requestMarginLayout();
  }
  function requestMarginLayout() {
    if(marginFrame)return;
    marginFrame=requestAnimationFrame(()=>{marginFrame=null;layoutSidenotes();});
  }
  function layoutSidenotes() {
    const rail=$('.reference-rail'),layout=$('.book-layout'),leaders=$('#note-leaders');
    if(!desktop.matches){rail.style.minHeight='';return;}
    const rr=rail.getBoundingClientRect(),lr=layout.getBoundingClientRect(),body=$('#chapter-body').getBoundingClientRect();
    const floor=$('#margin-search-slot').offsetHeight+22;let offset=0;
    // Isotonic least-squares packing: minimise displacement from the word's line,
    // subject to non-overlap. Isolated notes keep their exact target position.
    const pools=[];
    for(let i=0;i<marginItems.length;i++){
      const item=marginItems[i];item.rect=wordRect(item.word);item.offset=offset;
      item.desired=item.rect.top-rr.top+3;item.height=item.note.offsetHeight;
      const block={start:i,end:i,sum:item.desired-offset,count:1};pools.push(block);
      while(pools.length>1){const a=pools.at(-2),b=pools.at(-1);if(a.sum/a.count<=b.sum/b.count)break;
        a.end=b.end;a.sum+=b.sum;a.count+=b.count;pools.pop();}
      offset+=item.height+14;
    }
    let bottom=0;
    for(const pool of pools){const level=Math.max(floor,pool.sum/pool.count);
      for(let i=pool.start;i<=pool.end;i++){
        const item=marginItems[i],top=item.offset+level;item.note.style.top=top+'px';bottom=Math.max(bottom,top+item.height);
        const sx=body.right-lr.left+7,sy=item.rect.top-lr.top+item.rect.height*.72;
        const ex=rr.left-lr.left-9,ey=rr.top-lr.top+top+10,mid=(sx+ex)/2;
        item.line.setAttribute('d',`M${sx},${sy} C${mid},${sy} ${mid},${ey} ${ex},${ey}`);
        const wy=item.rect.bottom-lr.top+1,wx=Math.min(body.right,item.rect.right)-lr.left+4;
        item.trace.setAttribute('d',`M${wx},${wy} H${sx-3}`);
        item.note.dataset.displacement=String(Math.round(top-item.desired));
      }
    }
    rail.style.minHeight=bottom?Math.ceil(bottom)+'px':'';
    leaders.setAttribute('viewBox',`0 0 ${layout.clientWidth} ${layout.clientHeight}`);
    maskSidenotes();
  }
  function maskSidenotes() {
    if(!desktop.matches)return;
    const dock=$('#margin-search-slot').getBoundingClientRect();
    for(const item of marginItems){const nr=item.note.getBoundingClientRect(),wr=wordRect(item.word);
      const covered=nr.top<dock.bottom+6;item.note.style.visibility=covered?'hidden':'';
      item.line.style.visibility=covered||wr.bottom<dock.bottom+6?'hidden':'';
      item.trace.style.visibility=covered?'hidden':'';
    }
  }
  for(const type of ['pointerover','focusin'])$('#sidenotes').addEventListener(type,e=>{
    const el=e.target.closest('.margin-term');if(!el||e.pointerType==='touch'||el===ignoreFocus)return;
    clearTimeout(closeTimer);clearTimeout(showTimer);showTimer=setTimeout(()=>showPopup(el),type==='focusin'?0:90);
  });
  $('#sidenotes').addEventListener('pointerout',e=>{if(e.target.closest('.margin-term'))delayClose();});
  $('#sidenotes').addEventListener('focusout',delayClose);
  $('#sidenotes').addEventListener('click',e=>{const el=e.target.closest('.margin-term');if(el)showPopup(el);});
  $('#sidenotes').addEventListener('keydown',e=>{const el=e.target.closest('.margin-term');if(el&&e.key==='Tab'&&!e.shiftKey&&!popup.hidden&&anchor===el){e.preventDefault();(popup.querySelector('a')||$('#word-close')).focus();}});
  const marginResize=new ResizeObserver(requestMarginLayout);
  marginResize.observe($('.reading-column'));marginResize.observe($('#margin-search-slot'));
  document.fonts?.ready.then(requestMarginLayout);

  async function openChapter(id,paragraph) {
    const meta=chapter(id);if(!meta)throw new Error('The chapter address does not exist.');
    closeDialogs();closePopup(false);$('#error-panel').hidden=true;
    if(state.chapter?.id===id){scrollToPassage(paragraph);return;}
    const token=++state.token;state.loading=true;$('#reading').setAttribute('aria-busy','true');
    try {
      let c=state.cache.get(id);if(!c){c=await getJSON('chapters/'+id+'.json');state.cache.set(id,c);if(state.cache.size>8)state.cache.delete(state.cache.keys().next().value);}
      if(token!==state.token)return;
      state.chapter=c;$('#chapter-title').textContent=c.title;document.title=c.title+' · '+state.manifest.title;
      $('#chapter-body').innerHTML=c.html;$('#chapter-body').dataset.volume=c.volume;$('#chapter-body').classList.toggle('dramatic-chapter',c.layout==='drama');
      for(const img of $$('#chapter-body img')){const src=img.getAttribute('src');if(src.startsWith('../images/'))img.setAttribute('src',src.slice(3));else if(src.startsWith('../../assets/'))img.setAttribute('src',src.slice(3));}
      for(const a of $$('#chapter-body a[data-route]'))a.href='#'+a.dataset.route;
      if(sourceWording)for(const e of $$('#chapter-body .text-fix')) {
        const word=e.querySelector('.word');
        // Keep a corrected term's hover target when the whole correction is that word.
        if(word && e.textContent===word.textContent && e.children.length===1) word.textContent=e.dataset.original;
        else e.textContent=e.dataset.original;
      }
      activateNotes();makeSidenotes();turns();markCurrent();state.loading=false;$('#reading').setAttribute('aria-busy','false');
      scrollToPassage(paragraph);progress();requestMarginLayout();
      for(const img of $$('#chapter-body img'))img.addEventListener('load',requestMarginLayout,{once:true});
      if($('#search-input').value.trim())doSearch();
    }catch(e){if(token===state.token){state.loading=false;$('#reading').setAttribute('aria-busy','false');showError(e);}}
  }
  function scrollToPassage(id) {
    const el=id?$('#chapter-body').querySelector('#'+CSS.escape(id)):null;
    if(el){el.scrollIntoView({block:'start',behavior:'instant'});window.scrollBy(0,-28);}
    else window.scrollTo({top:0,behavior:'instant'});
  }
  async function navigate() {
    if(!state.manifest)return;
    const r=route();const id=chapter(r.chapter)?r.chapter:state.manifest.defaultChapter;
    if(r.chapter&&!chapter(r.chapter)){showError(new Error('Unknown chapter address.'));return;}
    try{await openChapter(id,r.paragraph);}catch(e){showError(e);}
  }
  function positionPopup() {
    if(!anchor||popup.hidden)return;
    const b=anchor.getBoundingClientRect();if(b.bottom<0||b.top>innerHeight){closePopup(false);return;}const w=popup.offsetWidth,h=popup.offsetHeight;
    const left=clamp(b.left+b.width/2-w/2,14,innerWidth-w-14);
    let top=b.bottom+8;if(top+h>innerHeight-14)top=b.top-h-8;
    popup.style.left=left+'px';popup.style.top=clamp(top,14,Math.max(14,innerHeight-h-14))+'px';
  }
  function showPopup(el) {
    clearTimeout(showTimer);clearTimeout(closeTimer);
    const term=state.terms.get(el.dataset.term);if(!term)return;
    if(anchor&&anchor!==el)anchor.setAttribute('aria-expanded','false');anchor=el;
    $('#word-title').textContent=term.term;$('#word-note').textContent=term.note;$('#word-sources').replaceChildren();
    for(const src of term.sources||[]){try{const u=new URL(src.url);if(!['https:','http:'].includes(u.protocol))continue;const a=document.createElement('a');a.href=u.href;a.target='_blank';a.rel='noopener noreferrer';a.textContent=src.label||'Source';$('#word-sources').append(a);}catch{}}
    popup.hidden=false;el.setAttribute('aria-expanded','true');setActiveTerm(term.id);positionPopup();
  }
  function closePopup(restore=false) {
    clearTimeout(showTimer);clearTimeout(closeTimer);const old=anchor;anchor=null;popup.hidden=true;setActiveTerm(null);
    if(old){old.setAttribute('aria-expanded','false');if(restore){ignoreFocus=old;old.focus({preventScroll:true});setTimeout(()=>ignoreFocus=null,80);}}
  }
  function delayClose(){clearTimeout(showTimer);clearTimeout(closeTimer);closeTimer=setTimeout(()=>{if(!popup.matches(':hover')&&!popup.contains(document.activeElement)&&!anchor?.matches(':hover'))closePopup(false);},340);}
  function noteTarget(e) {return e.target.closest?.('.word[data-first="true"][tabindex]');}
  $('#chapter-body').addEventListener('pointerover',e=>{if(e.pointerType==='touch')return;const el=noteTarget(e);if(!el)return;clearTimeout(closeTimer);clearTimeout(showTimer);showTimer=setTimeout(()=>showPopup(el),90);});
  $('#chapter-body').addEventListener('pointerout',e=>{const el=noteTarget(e);if(el&&!el.contains(e.relatedTarget))delayClose();});
  $('#chapter-body').addEventListener('focusin',e=>{const el=noteTarget(e);if(el&&el!==ignoreFocus)showPopup(el);});
  $('#chapter-body').addEventListener('focusout',e=>{if(noteTarget(e))delayClose();});
  $('#chapter-body').addEventListener('click',e=>{const el=noteTarget(e);if(el){e.preventDefault();showPopup(el);}});
  $('#chapter-body').addEventListener('keydown',e=>{const el=noteTarget(e);if(!el)return;if(e.key==='Enter'||e.key===' '){e.preventDefault();showPopup(el);}else if(e.key==='Tab'&&!e.shiftKey&&!popup.hidden&&anchor===el){e.preventDefault();(popup.querySelector('a')||$('#word-close')).focus();}});
  popup.addEventListener('pointerenter',()=>clearTimeout(closeTimer));popup.addEventListener('pointerleave',delayClose);
  popup.addEventListener('focusin',()=>clearTimeout(closeTimer));popup.addEventListener('focusout',delayClose);
  $('#word-close').addEventListener('click',()=>closePopup(true));
  document.addEventListener('pointerdown',e=>{if(!popup.hidden&&!popup.contains(e.target)&&!anchor?.contains(e.target))closePopup(false);});
  function moveSearch() {
    const hadFocus=$('#search-panel').contains(document.activeElement)||document.body.dataset.searching==='true';requestMarginLayout();
    const dest=desktop.matches?$('#margin-search-slot'):$('#search-dialog-slot');dest.append($('#search-panel'));
    if(desktop.matches)closeDialogs();
    else if(hadFocus&&!$('#search-dialog').open)$('#search-dialog').showModal();
    if(hadFocus)$('#search-input').focus();
  }
  async function doSearch() {
    const serial=++searchSequence,q=$('#search-input').value.trim(),out=$('#search-results');out.replaceChildren();$('#search-options').hidden=!q;document.body.dataset.searching=q.length>=2?'true':'false';
    if(q.length<2){$('#search-status').textContent=q?'Enter at least two characters.':'';return;}
    $('#search-status').textContent='Searching…';
    try {
      if(!state.search)state.search=await getJSON('search.json');if(serial!==searchSequence)return;
      const needle=norm(q),scope=$('#search-scope').value;let count=0;const found=[];
      for(const c of state.search){if(c.kind==='reference')continue;if(scope==='chapter'&&c.id!==state.chapter.id)continue;if(scope==='through'&&c.index>state.chapter.index)continue;
        for(const p of c.paragraphs){const at=norm(p.text).indexOf(needle);if(at<0)continue;count++;if(found.length<60)found.push({c,p,at});}
      }
      for(const {c,p,at} of found){const a=document.createElement('a');a.className='search-result';a.href='#'+c.id+'/'+p.id;const start=Math.max(0,at-60),end=Math.min(p.text.length,at+q.length+100);
        const excerpt=(start?'…':'')+esc(p.text.slice(start,at))+'<mark>'+esc(p.text.slice(at,at+q.length))+'</mark>'+esc(p.text.slice(at+q.length,end))+(end<p.text.length?'…':'');
        a.innerHTML='<strong>'+esc(c.title)+'</strong><p>'+excerpt+'</p>';out.append(a);}
      $('#search-status').textContent=count?`${count} matching paragraph${count===1?'':'s'}${count>60?'; showing the first 60':''}.`:'No matching paragraphs.';
    }catch(e){if(serial===searchSequence)$('#search-status').textContent='Search could not load. The text is still available.';}
  }
  $('#search-input').addEventListener('input',debounce(doSearch,180));$('#search-scope').addEventListener('change',doSearch);
  $('#contents-button').addEventListener('click',()=>{$('#contents-dialog').showModal();$('#mobile-contents a[aria-current]')?.scrollIntoView({block:'center'});});
  $('#search-button').addEventListener('click',()=>{$('#search-dialog').showModal();$('#search-input').focus();});
  $$('[data-close]').forEach(b=>b.addEventListener('click',()=>b.closest('dialog').close()));
  $$('dialog').forEach(d=>d.addEventListener('click',e=>{if(e.target===d){const r=d.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)d.close();}}));
  document.addEventListener('click',e=>{const a=e.target.closest('a[href^="#"]');if(!a||a.classList.contains('skip-link'))return;if(a.hash===location.hash){e.preventDefault();closeDialogs();navigate();}else if(a.closest('.toc,#search-results'))closeDialogs();});
  document.addEventListener('keydown',e=>{
    if(e.key==='Escape'){if(!popup.hidden){e.preventDefault();closePopup(true);}else if(e.target===$('#search-input')&&e.target.value){e.preventDefault();e.target.value='';doSearch();}return;}
    if(e.target.closest('input,textarea,select,[contenteditable="true"]'))return;
    if(e.key==='/'||((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k')){e.preventDefault();if(!desktop.matches)$('#search-dialog').showModal();$('#search-input').focus();}
    if(e.key==='['||e.key===']'){if($('dialog[open]')||!state.chapter)return;const list=state.manifest.chapters.filter(c=>c.kind!=='reference');const next=list[list.findIndex(c=>c.id===state.chapter.id)+(e.key===']'?1:-1)];if(next)location.hash=next.id;}
  });
  window.addEventListener('hashchange',navigate);
  window.addEventListener('scroll',()=>{if(scrollFrame)return;scrollFrame=requestAnimationFrame(()=>{scrollFrame=null;progress();maskSidenotes();if(!popup.hidden)positionPopup();});},{passive:true});
  window.addEventListener('resize',()=>{positionPopup();progress();requestMarginLayout();});desktop.addEventListener('change',moveSearch);
  async function init() {
    moveSearch();
    try {const [m,g]=await Promise.all([getJSON('manifest.json'),getJSON('glossary.json')]);state.manifest=m;state.terms=new Map(g.map(x=>[x.id,x]));toc($('#desktop-contents'));toc($('#mobile-contents'));await navigate();}
    catch(e){showError(e);}
  }
  init();
})();
