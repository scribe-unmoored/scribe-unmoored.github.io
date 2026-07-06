// nav-toggle.js
// Adds close/open hamburger toggle

document.addEventListener('DOMContentLoaded', function () {
  var btn = document.getElementById('menu-toggle');
  var sidebar = document.querySelector('.sidebar');

  if (!btn || !sidebar) return; // safe no-op if a page is missing either

  btn.addEventListener('click', function () {
    var isOpen = sidebar.classList.toggle('open');
    btn.classList.toggle('is-active', isOpen);
    btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  });
});
