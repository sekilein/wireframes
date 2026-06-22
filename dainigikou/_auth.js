if (!sessionStorage.getItem('dainigikou_auth')) {
  var path = location.pathname;
  var marker = '/dainigikou/';
  var idx = path.indexOf(marker);
  var loginUrl;
  if (idx >= 0) {
    loginUrl = path.substring(0, idx + marker.length) + 'login.html';
  } else {
    loginUrl = 'login.html';
  }
  location.replace(loginUrl + '?next=' + encodeURIComponent(location.href));
}
