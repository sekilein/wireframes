/* ============================================
   車両詳細ページ：空欄の自動非表示
   - 入力が無い行（td が空 or「−」）はその行を非表示
   - ブロック内の表示行が 0 になったらブロックごと非表示
   - 車両コメントが空ならコメントブロックごと非表示
   ※ 項目（テンプレート）は HTML に残したまま、入力が無い箇所だけ消す。
   ============================================ */
(function () {
    function isEmptyText(t) {
        t = (t || '').replace(/[\s　]/g, '');
        return t === '' || t === '-' || t === '−' /* − */ || t === '—' /* — */ || t === 'ー' /* ー */;
    }

    var blocks = document.querySelectorAll('.vehicle-block');
    Array.prototype.forEach.call(blocks, function (block) {
        // --- コメント等のテキストブロック ---
        var comment = block.querySelector('.vehicle-comment-box');
        if (comment) {
            if (isEmptyText(comment.textContent)) block.style.display = 'none';
            return;
        }

        // --- テーブル系ブロック：空行を消し、全行空ならブロックごと消す ---
        var rows = block.querySelectorAll('.vehicle-spec-table tr');
        if (!rows.length) return;

        var visibleCount = 0;
        Array.prototype.forEach.call(rows, function (tr) {
            var td = tr.querySelector('td');
            if (td && isEmptyText(td.textContent)) {
                tr.style.display = 'none';
            } else {
                visibleCount++;
            }
        });

        if (visibleCount === 0) block.style.display = 'none';
    });
})();
