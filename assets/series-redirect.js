/* Preserve existing book and paragraph links when entering a combined reader. */
'use strict';
(() => {
  const {series, prefix, first} = document.body.dataset;
  const target = new URL(`../${series}/`, location.href);
  target.search = location.search;
  target.hash = prefix + (location.hash.slice(1) || first);
  location.replace(target.href);
})();
