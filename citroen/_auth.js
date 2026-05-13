(function () {
  try {
    if (sessionStorage.getItem('citroen_auth') === '1') return;
  } catch (e) { /* sessionStorage 利用不可は通過 */ }
  var here = location.pathname.split('/').pop() || '';
  if (here === 'login.html') return;
  var next = encodeURIComponent(location.pathname + location.search + location.hash);
  location.replace('login.html?next=' + next);
})();
