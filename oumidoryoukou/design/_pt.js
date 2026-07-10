/* ページ遷移演出：ブロックごとに赤い幕が覆い→抜けていく（参考: gmining.com/careers）
   - 入場: 各ブロックを覆った幕が上へ抜けて中身が現れる（上から順にスタガー）
   - 退場: 内部リンククリックで幕が下から覆い→遷移
   - prefers-reduced-motion では無効 */
(function () {
  if (matchMedia('(prefers-reduced-motion:reduce)').matches) return;

  var RED = '#ff0000';
  var IN_DUR = 700, IN_STAG = 90, OUT_DUR = 460, EASE = 'cubic-bezier(.77,0,.18,1)';

  var style = document.createElement('style');
  style.textContent =
    '.pt-cover{position:absolute;inset:-3px;background:' + RED + ';z-index:990;pointer-events:none;' +
    'transform:scaleY(1);will-change:transform;}' +
    'html.pt-init body{visibility:hidden;}' +
    'html.pt-veil .burger,html.pt-veil .drawer{visibility:hidden!important;}';
  document.documentElement.appendChild(style);
  document.documentElement.classList.add('pt-init');
  document.documentElement.classList.add('pt-veil');

  function blocks() {
    var out = [];
    [].slice.call(document.body.children).forEach(function (k) {
      if (/^(SCRIPT|STYLE|LINK)$/.test(k.tagName)) return;
      if (k.classList && (k.classList.contains('burger') || k.classList.contains('drawer') || k.classList.contains('spmenu'))) return;
      var isWrap = k.tagName === 'DIV' && k.classList.contains('wrap');
      if (isWrap || /^(FOOTER|MAIN)$/.test(k.tagName)) {
        [].slice.call(k.children).forEach(function (c) {
          if (!/^(SCRIPT|STYLE)$/.test(c.tagName)) out.push(c);
        });
      } else out.push(k);
    });
    return out.filter(function (b) { return b.offsetHeight > 10; });
  }

  function addCovers(origin, initScale) {
    return blocks().map(function (b) {
      if (getComputedStyle(b).position === 'static') b.style.position = 'relative';
      var c = document.createElement('div');
      c.className = 'pt-cover';
      c.style.transformOrigin = origin;
      c.style.transform = 'scaleY(' + initScale + ')';
      b.appendChild(c);
      return c;
    });
  }

  /* ── 入場：幕が上へ抜ける ── */
  function reveal() {
    var covers = addCovers('top', 1);
    document.documentElement.classList.remove('pt-init');
    requestAnimationFrame(function () { requestAnimationFrame(function () {
      covers.forEach(function (c, i) {
        c.style.transition = 'transform ' + IN_DUR + 'ms ' + EASE + ' ' + (i * IN_STAG) + 'ms';
        c.style.transform = 'scaleY(0)';
      });
      setTimeout(function () {
        covers.forEach(function (c) { if (c.parentNode) c.parentNode.removeChild(c); });
        document.documentElement.classList.remove('pt-veil');
      }, IN_DUR + covers.length * IN_STAG + 100);
    }); });
  }

  /* ── 退場：幕が下から覆う → 遷移 ── */
  var leaving = false;
  document.addEventListener('click', function (e) {
    if (leaving || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
    var a = e.target.closest ? e.target.closest('a[href]') : null;
    if (!a || a.target === '_blank') return;
    var href = a.getAttribute('href');
    if (!href || /^(https?:|mailto:|tel:|#|javascript:)/.test(href)) return;
    if (href.indexOf('#') !== -1 && href.split('#')[0] === location.pathname.split('/').pop()) return;
    e.preventDefault();
    leaving = true;
    document.documentElement.classList.add('pt-veil');
    var covers = addCovers('bottom', 0);
    var stag = Math.min(60, Math.round(360 / Math.max(covers.length, 1)));
    requestAnimationFrame(function () { requestAnimationFrame(function () {
      covers.forEach(function (c, i) {
        c.style.transition = 'transform ' + OUT_DUR + 'ms ' + EASE + ' ' + (i * stag) + 'ms';
        c.style.transform = 'scaleY(1)';
      });
      setTimeout(function () { location.href = href; }, OUT_DUR + covers.length * stag + 60);
    }); });
  }, true);

  window.addEventListener('pageshow', function (e) {
    if (e.persisted) { leaving = false; reveal(); }
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', reveal);
  } else reveal();
})();
