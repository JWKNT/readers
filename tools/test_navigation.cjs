/* Execute the reader's navigation functions with deferred network responses.
   These are state/DOM-contract regressions; rendered browser QA is separate. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const test = require('node:test');
const source = fs.readFileSync(require('node:path').join(__dirname, '../assets/reader.js'), 'utf8');
const functionSource = name => source.match(new RegExp(`  async function ${name}\\([^]*?\\n  }`))[0];
const deferred = () => { let resolve, reject; const promise = new Promise((a, b) => { resolve = a; reject = b; }); return { promise, resolve, reject }; };

function setup() {
  const requests = new Map();
  const nodes = new Map();
  const node = selector => {
    if (!nodes.has(selector)) nodes.set(selector, { hidden: false, value: '', dataset: {}, classList: { toggle() {} }, setAttribute(name, value) { this[name] = value; } });
    return nodes.get(selector);
  };
  const current = { id: 'a', title: 'A', html: '<p>A</p>', volume: 'one' };
  const state = { manifest: { title: 'Book', defaultChapter: 'a', chapters: [current, { id: 'b' }, { id: 'c' }] }, chapter: current, cache: new Map(), token: 0, loading: false };
  const errors = [], passages = [];
  const context = {
    state, $: node, $$: () => [], document: {}, sourceWording: false, edition: null,
    chapter: id => state.manifest.chapters.find(c => c.id === id),
    route: () => context.currentRoute,
    getJSON: path => { const request = deferred(); requests.set(path, request); return request.promise; },
    closeDialogs() {}, closePopup() {}, activateNotes() {}, makeSidenotes() {}, turns() {}, markCurrent() {}, progress() {}, requestMarginLayout() {}, doSearch() {},
    scrollToPassage: paragraph => passages.push(paragraph), showError: error => errors.push(error.message),
  };
  vm.createContext(context);
  vm.runInContext(functionSource('openChapter') + '\n' + functionSource('navigate'), context);
  return { ...context, context, requests, node, errors, passages };
}

test('returning to the displayed chapter cancels an unfinished chapter change', async () => {
  const h = setup();
  const pending = h.openChapter('b');
  assert.equal(h.state.loading, true);
  await h.openChapter('a', 'p-2');
  assert.equal(h.state.loading, false);
  assert.equal(h.node('#reading')['aria-busy'], 'false');
  h.requests.get('chapters/b.json').resolve({ id: 'b', title: 'B', html: '<p>B</p>', volume: 'one' });
  await pending;
  assert.equal(h.state.chapter.id, 'a');
  assert.deepEqual(h.passages, ['p-2']);
});

test('a late failure from a cancelled chapter does not replace the current view', async () => {
  const h = setup();
  const pending = h.openChapter('b');
  await h.openChapter('a');
  h.requests.get('chapters/b.json').reject(new Error('Network interrupted'));
  await pending;
  assert.deepEqual(h.errors, []);
  assert.equal(h.state.chapter.id, 'a');
});

test('an unknown chapter address cancels a previous request and clears busy state', async () => {
  const h = setup();
  const pending = h.openChapter('b');
  h.context.currentRoute = { chapter: 'missing' };
  await h.navigate();
  assert.equal(h.state.loading, false);
  assert.equal(h.node('#reading')['aria-busy'], 'false');
  assert.deepEqual(h.errors, ['Unknown chapter address.']);
  h.requests.get('chapters/b.json').resolve({ id: 'b', title: 'B', html: '<p>B</p>', volume: 'one' });
  await pending;
  assert.equal(h.state.chapter.id, 'a');
});

test('the latest pending chapter wins and a failed request can be retried', async () => {
  const h = setup();
  const first = h.openChapter('b');
  const second = h.openChapter('c');
  h.requests.get('chapters/c.json').reject(new Error('Temporary failure'));
  await second;
  assert.equal(h.state.loading, false);
  const retry = h.openChapter('c');
  h.requests.get('chapters/c.json').resolve({ id: 'c', title: 'C', html: '<p>C</p>', volume: 'one' });
  await retry;
  h.requests.get('chapters/b.json').resolve({ id: 'b', title: 'B', html: '<p>B</p>', volume: 'one' });
  await first;
  assert.equal(h.state.chapter.id, 'c');
  assert.equal(h.node('#reading')['aria-busy'], 'false');
});
