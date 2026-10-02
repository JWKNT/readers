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


test('Home and theme share geometry, ink and icon scale without local overrides', () => {
  const utilities = base.slice(base.indexOf('a.site-home,'), base.indexOf('.site-utility-pair .theme-toggle'));
  for (const declaration of ['width: var(--utility-size, 2.75rem)', 'height: var(--utility-size, 2.75rem)', 'margin: 0', 'color: var(--muted-strong)', 'opacity: 1']) assert.ok(utilities.includes(declaration));
  assert.ok(base.includes('gap: var(--utility-gap, .375rem)'));
  assert.ok(base.includes('width: var(--utility-icon-size, 1.6rem)'));
  assert.ok(base.includes('icons/home-compass.svg'));
  assert.ok(!base.includes('icons/home-emblem.svg'));
  for (const icon of ['home-compass.svg', 'search-slash.svg']) assert.ok(fs.existsSync(path.join(__dirname, '..', 'assets/theme/icons', icon)));
  assert.ok(!css.includes('.static-header .theme-toggle{margin-left:auto}'));
  assert.ok(css.includes('a:not(.site-home):hover,a:not(.site-home):visited'));
  assert.ok(css.includes('button:not(.theme-toggle):focus-visible'));
  const library = read('assets/library.css');
  assert.ok(library.includes('.library-page a:not(.site-home) { color: var(--ink); }'));
  assert.ok(library.includes('.library-page button:not(.theme-toggle):focus-visible'));
});


test('reduced-motion disables transitions for Home and theme alike', () => {
  const reduced = base.slice(base.indexOf('@media (prefers-reduced-motion: reduce)'), base.indexOf('@media print'));
  assert.ok(reduced.includes('a.site-home, button.site-search,'));
  assert.ok(reduced.includes('[data-theme-toggle].theme-toggle,'));
  assert.ok(reduced.includes('transition: none;'));
});


test('vendored touch navigation keeps the Home utility in the same grid as the dial', () => {
  const touch = base.split('@media (pointer: coarse) {')[1].split('@media (prefers-reduced-motion: reduce)')[0];
  assert.match(touch, /\.site-header nav a:not\(\.site-home\), \.site-nav a:not\(\.site-home\)/);
  assert.doesNotMatch(touch, /\.site-header nav a\s*[,\{]|\.site-nav a\s*[,\{]/);
});


test('empty Readers theme buttons and Home fallback spans share the same icon track', () => {
  assert.match(base, /header a\.site-home,\s*header \[data-theme-toggle\]\.theme-toggle \{\s*grid-template-rows: minmax\(0, 1fr\);\s*grid-auto-rows: 0;/);
});
