/* Only the outgoing history entry is annotated; no reading position is stored. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const test = require('node:test');
const source = fs.readFileSync(require('node:path').join(__dirname, '../assets/reader.js'), 'utf8');
const helper = () => { const fn = source.match(/  function rememberPassage\([^]*?\n  }/)?.[0]; assert.ok(fn, 'history helper exists'); return fn; };
function setup({target = '', hasRoute = true, block = {id:'p-006'}, inside = true, href = 'https://jehlp.net/readers/book/?wording=source'} = {}) {
  const writes = [], originalState = { retained: true };
  const link = { target, hasAttribute: name => name === 'data-route' && hasRoute, closest: selector => selector === '#chapter-body' ? inside : block };
  const context = { state: { chapter: {id:'chapter-one'} }, URL, location: {href}, history: {state:originalState,replaceState: (state,_title,url) => writes.push({state,url:String(url)})} };
  vm.createContext(context); vm.runInContext(helper(),context);
  return {...context, link,writes,originalState};
}

test('a footnote leaves a chapter-and-paragraph origin for browser Back', () => {
  const h=setup();h.rememberPassage({button:0},h.link);
  assert.equal(h.writes.length,1);
  assert.equal(h.writes[0].url,'https://jehlp.net/readers/book/?wording=source#chapter-one/p-006');
  assert.equal(h.writes[0].state,h.originalState);
  const history=[h.writes[0].url,'https://jehlp.net/readers/book/?wording=source#notes/p-001'];
  history.pop();
  const route=decodeURIComponent(new URL(history.at(-1)).hash.slice(1)).split('/');
  assert.deepEqual(route,['chapter-one','p-006']);
});

test('modified clicks and other targets leave the current history entry untouched', () => {
  for(const event of [{button:1},{ctrlKey:true},{metaKey:true},{shiftKey:true},{altKey:true},{defaultPrevented:true}]) {
    const h=setup();h.rememberPassage(event,h.link);assert.equal(h.writes.length,0);
  }
  for(const target of ['_blank','another-frame']) {const h=setup({target});h.rememberPassage({},h.link);assert.equal(h.writes.length,0);}
});

test('ordinary links, outside links, and missing paragraph anchors do not alter history', () => {
  for(const options of [{hasRoute:false},{inside:false},{block:null},{block:{id:''}}]) {
    const h=setup(options);h.rememberPassage({},h.link);assert.equal(h.writes.length,0);
  }
});

test('an explicit same-tab link may retain its source passage', () => {
  const h=setup({target:'_self'});h.rememberPassage({button:0},h.link);assert.equal(h.writes.length,1);
});

test("the reader wires ordinary in-text navigation to the history helper", () => {
  assert.match(source, /else \{rememberPassage\(e,a\);if\(a\.closest/);
});
