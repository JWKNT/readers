/* Source contracts for header-only Home; rendered browser QA is separate. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const read = file => fs.readFileSync(path.join(__dirname, '..', file), 'utf8');
const reader = read('assets/reader.js');
const css = read('assets/reader.css');
const theme = read('assets/theme/theme.js');
const base = read('assets/theme/base.css');

test('reader never moves or duplicates the native header Home', () => {
  for (const removed of ['moveHome', 'site-home', 'reader-controls-ready']) assert.ok(!reader.includes(removed));
  assert.match(reader, /desktop\.addEventListener\('change',moveSearch\)/);
});

test('Contents and Search retain their original mobile toolbar behavior', () => {
  assert.ok(css.includes('.mobile-tools{position:fixed;display:flex;'));
  assert.ok(!css.includes('.mobile-tools .site-home'));
  assert.ok(!css.includes('reader-controls-ready'));
});

test('header control area scrolls with the reader document', () => {
  assert.ok(css.includes('.appearance{display:flex;align-items:center;gap:.5rem;position:absolute;'));
  assert.ok(css.includes('.static-header .site-utility-pair{margin-left:auto}'));
});

test('shared Home has no footer spacer or focused-field scrolling handler', () => {
  assert.ok(!base.includes('--site-home-clearance'));
  assert.ok(!base.includes('body:has(.site-home)::after'));
  assert.ok(!theme.includes('keepFocusedControlClear'));
  assert.ok(!theme.includes('homeFocusBound'));
});
