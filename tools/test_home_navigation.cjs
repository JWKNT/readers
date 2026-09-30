/* Unit-test the real responsive relocation function without browser automation. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '../assets/reader.js'), 'utf8');
const fn = source.match(/  function moveHome\(\) \{[\s\S]*?\n  \}(?=\n  function moveSearch)/)[0];

function fixture(matches = true) {
  function element(id) {
    return { id, parent: null, children: [],
      insertBefore(child, next) {
        if (child === next) return;
        if (child.parent) child.parent.children.splice(child.parent.children.indexOf(child), 1);
        const index = next ? this.children.indexOf(next) : this.children.length;
        assert.notEqual(index, -1, 'Insertion reference must belong to its parent');
        this.children.splice(index, 0, child);
        child.parent = this;
      },
      prepend(child) { this.insertBefore(child, this.children[0] || null); },
    };
  }
  const body = element('body'), dock = element('home-nav'), tools = element('mobile-tools');
  const contents = element('contents-button'), search = element('search-button');
  const home = element('home-link');
  dock.insertBefore(home, null);
  tools.insertBefore(contents, null);
  tools.insertBefore(search, null);
  body.insertBefore(dock, null);
  body.insertBefore(tools, null);
  const nodes = { '.site-home-dock': dock, '.mobile-tools': tools, '#search-button': search };
  const desktop = { matches };
  const moveHome = vm.runInNewContext(fn + '\nmoveHome', {
    $: selector => nodes[selector], desktop, document: { body },
  });
  return { body, dock, tools, contents, search, home, nodes, desktop, moveHome };
}

test('desktop retains the same native dock at the beginning of the document', () => {
  const f = fixture();
  f.moveHome();
  assert.equal(f.body.children[0], f.dock);
  assert.equal(f.dock.children[0], f.home);
  assert.deepEqual(f.tools.children.map(x => x.id), ['contents-button', 'search-button']);
});

test('mobile puts the native Home between Contents and Search', () => {
  const f = fixture(false);
  f.moveHome();
  assert.deepEqual(f.tools.children.map(x => x.id), ['contents-button', 'home-nav', 'search-button']);
  assert.equal(f.dock.children[0], f.home);
  assert.equal(f.body.children.includes(f.dock), false);
});

test('repeated mobile/desktop switches never clone or strand the Home link', () => {
  const f = fixture();
  for (const matches of [false, false, true, true, false, true, false]) {
    f.desktop.matches = matches;
    f.moveHome();
    assert.equal(f.dock.parent, matches ? f.body : f.tools);
    assert.equal(f.dock.children.length, 1);
    assert.equal(f.dock.children[0], f.home);
    assert.equal([...f.body.children, ...f.tools.children].filter(x => x === f.dock).length, 1);
  }
});

test('missing optional dock or toolbar leaves the native document alone', () => {
  for (const selector of ['.site-home-dock', '.mobile-tools']) {
    const f = fixture(false);
    f.nodes[selector] = null;
    f.moveHome();
    assert.equal(f.dock.parent, f.body);
    assert.deepEqual(f.tools.children.map(x => x.id), ['contents-button', 'search-button']);
  }
});
