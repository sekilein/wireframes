// Scroll fade-in
const obs = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); obs.unobserve(e.target); } });
}, { threshold: 0.12 });
document.querySelectorAll('.fade-in, .cat-pullquote').forEach(el => obs.observe(el));

// タイムラインのスポットを順次表示
const spotObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      spotObs.unobserve(e.target);
    }
  });
}, { threshold: 0.15, rootMargin: '0px 0px -10% 0px' });
document.querySelectorAll('.timeline .spot').forEach(el => spotObs.observe(el));

// Hero bubble: cycle 12 texts (shoot in/out from bottom-left corner, hold 5s)
(function(){
  const bubble = document.querySelector('.hero-bubble');
  const span = bubble && bubble.querySelector('.hero-bubble-text');
  if (!bubble || !span) return;
  const lines = [
    '何食べよう？',
    'そばまさ、間に合う？',
    'お鍋、いいかもね。',
    'あの塔、登ってみる？',
    '海、見えるかな？',
    '提灯、見ていく？',
    'ビール、買って帰る？',
    'コーヒー、寄る？',
    '器、ひとつ選ぼうか。',
    '教会、寄っていく？',
    '朝ごはん、どうする？',
    '今夜、海の宿だね。'
  ];
  let i = 0;
  const HOLD = 5000;        // テキスト表示キープ時間
  const TEXT_OUT = 300;     // テキスト消失アニメ
  const BUBBLE_OUT = 350;   // 吹き出し縮小（左下へ）
  const BUBBLE_IN = 350;    // 吹き出し出現
  const TEXT_REVEAL = 500;  // テキスト左→右に表示

  setTimeout(tick, HOLD);

  function tick() {
    // 1. テキストを消す（右から左へワイプアウト）
    span.classList.add('hidden');
    setTimeout(() => {
      // 2. 吹き出しを左下に縮小
      bubble.classList.add('out');
      setTimeout(() => {
        // 3. 次の文言に差し替え
        i = (i + 1) % lines.length;
        span.textContent = lines[i];
        // 4. 吹き出しを出現
        bubble.classList.remove('out');
        setTimeout(() => {
          // 5. テキストを左から右に表示
          span.classList.remove('hidden');
          setTimeout(tick, HOLD);
        }, BUBBLE_IN);
      }, BUBBLE_OUT);
    }, TEXT_OUT);
  }
})();

// タイムライン縦軸線：スクロールに応じて伸びる
function updateTimelineProgress() {
  document.querySelectorAll('.timeline').forEach(timeline => {
    const panel = timeline.closest('.day-panel');
    if (panel && !panel.classList.contains('active')) return;
    const progress = timeline.querySelector('.timeline-progress');
    if (!progress) return;
    const rect = timeline.getBoundingClientRect();
    const viewportH = window.innerHeight;
    const trigger = viewportH * 0.5; // 画面中央を基準
    const lineOffsetTop = 58;
    const lineOffsetBottom = 80;
    const distance = trigger - rect.top - lineOffsetTop;
    const maxHeight = Math.max(0, rect.height - lineOffsetTop - lineOffsetBottom);
    const height = Math.max(0, Math.min(distance, maxHeight));
    progress.style.height = height + 'px';
  });
}
window.addEventListener('scroll', updateTimelineProgress, { passive: true });
window.addEventListener('resize', updateTimelineProgress);
updateTimelineProgress();

// コースタブ切替
document.querySelectorAll('.course-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    const target = tab.dataset.target;
    if (!target) return;
    document.querySelectorAll('.course-tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    document.querySelectorAll('.course-panel, .timeline-panel').forEach(p => {
      p.classList.toggle('active', p.dataset.panel === target);
    });
    // コース切替時はDAY1にリセット
    document.querySelectorAll('.day-tab').forEach(t => {
      t.classList.toggle('active', t.dataset.day === 'day1');
    });
    document.querySelectorAll('.day-panel').forEach(p => {
      p.classList.toggle('active', p.dataset.day === 'day1');
    });
    requestAnimationFrame(updateTimelineProgress);
    // クリック後、該当コースの mymap までスクロール
    const activePanel = document.querySelector(`.course-panel.active[data-panel="${target}"]`);
    const map = activePanel && activePanel.querySelector('.day-mymap');
    if (map) {
      requestAnimationFrame(() => {
        const rect = map.getBoundingClientRect();
        const offset = window.pageYOffset + rect.top - 24;
        window.scrollTo({ top: offset, behavior: 'smooth' });
      });
    }
  });
});

// マップ iframe: クリックで操作可能化、ビューポート外に出たら解除（スクロール捕捉防止）
document.querySelectorAll('.day-map').forEach(map => {
  map.addEventListener('click', () => map.classList.add('interactive'));
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) map.classList.remove('interactive');
    });
  }, { threshold: 0.5 });
  io.observe(map);
});

// DAYトグル切替
document.querySelectorAll('.day-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    const day = tab.dataset.day;
    if (!day) return;
    document.querySelectorAll('.day-tab').forEach(t => {
      t.classList.toggle('active', t.dataset.day === day);
    });
    document.querySelectorAll('.day-panel').forEach(p => {
      p.classList.toggle('active', p.dataset.day === day);
    });
    requestAnimationFrame(updateTimelineProgress);
    const scrollTarget = tab.dataset.scroll;
    if (scrollTarget) {
      const el = document.querySelector(scrollTarget);
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});