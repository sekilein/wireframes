/* 下層共通：グローバルナビ（PC=ホバーでメガメニュー / SP=ハンバーガー＋アコーディオン） */
(function(){
  var nav = document.querySelector('.nav');
  var allItems = [].slice.call(document.querySelectorAll('.gnav__item'));
  function closeAll(){ allItems.forEach(function(it){ it.classList.remove('is-open'); }); }
  allItems.forEach(function(it){
    it.addEventListener('mouseenter', function(){
      closeAll();
      if(it.hasAttribute('data-mega')) it.classList.add('is-open');
    });
  });
  if(nav) nav.addEventListener('mouseleave', closeAll);

  var burger = document.querySelector('.burger');
  var sp = document.getElementById('spmenu');
  if(burger && sp){
    function setSp(open){
      sp.classList.toggle('is-open', open);
      burger.classList.toggle('is-open', open);
      burger.setAttribute('aria-expanded', open?'true':'false');
      sp.setAttribute('aria-hidden', open?'false':'true');
      document.body.classList.toggle('menu-open', open);
    }
    burger.addEventListener('click', function(){ setSp(!sp.classList.contains('is-open')); });
    sp.querySelectorAll('.spmenu__top').forEach(function(btn){
      btn.addEventListener('click', function(){
        var g = btn.parentNode;
        var open = g.classList.toggle('is-open');
        btn.setAttribute('aria-expanded', open?'true':'false');
      });
    });
    sp.querySelectorAll('a').forEach(function(a){ a.addEventListener('click', function(){ setSp(false); }); });
  }
})();
