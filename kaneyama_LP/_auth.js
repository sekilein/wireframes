if (!sessionStorage.getItem('kaneyama_auth')) {
  var next = encodeURIComponent(location.href);
  location.replace('login.html?next=' + next);
}
