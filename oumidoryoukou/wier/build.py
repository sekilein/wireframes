# -*- coding: utf-8 -*-
"""近江度量衡 Webリニューアル ワイヤーフレーム（wier）ジェネレータ
原稿シート（16lXY…）の「近江度量衡様 修正案」を最優先、無ければ「参考」を採用。
更新性/利便性はサイトマップ(ver3)を反映（CMS更新ページに更新マーク）。
"""
import os
OUT = os.path.dirname(os.path.abspath(__file__))

# 共有プレビュー用の認証（GitHub Pages公開時）※コメント機能は廃止
AUTH_HEAD = '<script src="_auth.js"></script>'

# ---------- 共通パーツ ----------
def ph(label, cls="", style=""):
    return f'<div class="ph {cls}" style="{style}"><span>{label}</span></div>'

def cms(text="CMS更新"):
    return f'<span class="cms-flag">◯ {text}</span>'

def todo(text="要確認/素材待ち"):
    return f'<span class="todo-flag">★ {text}</span>'

CORP_NAV = [
    ("製品・技術", "products.html"),
    ("サービス案内", "service.html"),
    ("納入実績", "delivery.html"),
    ("会社案内", "company.html"),
    ("126年ヒストリー", "history.html"),
    ("新着情報", "news.html"),
]
RECRUIT_NAV = [
    ("採用TOP", "recruit.html"),
    ("社員インタビュー", "recruit-interview.html"),
    ("採用ニュース", "recruit-news.html"),
    ("募集要項", "recruit-jobs.html"),
]

def _nav(items, active):
    out = ""
    for n, u in items:
        cls = ' class="active"' if u == active else ''
        out += f'<a href="{u}"{cls}>{n}</a>'
    return out

# ── d_3 グローバルナビ定義（TOPと同テイスト：メガメニュー＋ハンバーガー） ──
# key, ラベル, 直リンク, メガ種別('cards'|'links'|None), 子項目[(名称,URL)]
NAV_GROUPS = [
    ("products", "製品・技術", "products.html", "cards", [
        ("農産物用計量システム", "products-agricultural.html"),
        ("穀類用計量システム", "products-weighing.html"),
        ("工業用計量システム", "products-industry.html"),
        ("その他・特殊用途", "products-other.html"),
    ]),
    ("service", "サービス案内", "service.html", "links", [
        ("保守・定期点検", "service.html"), ("校正・検査", "service.html"),
        ("導入・設置サポート", "service.html"), ("修理・オーバーホール", "service.html"),
    ]),
    ("delivery", "納入実績", "delivery.html", None, []),
    ("company", "会社案内", "company.html", "links", [
        ("企業理念", "company.html"), ("会社概要", "company.html"),
        ("沿革", "history.html"), ("アクセス", "company.html"),
    ]),
    ("history", "126年ヒストリー", "history.html", None, []),
    ("recruit", "採用情報", "recruit.html", "links", [
        ("新卒採用", "recruit-jobs-graduate.html"), ("キャリア採用", "recruit-jobs-career.html"),
        ("社員インタビュー", "recruit-interview.html"), ("募集要項", "recruit-jobs.html"),
    ]),
]
NAV_EN = {"products":"Products","service":"Service","company":"Company","recruit":"Recruit"}

def _active_key(active):
    a = active or ""
    if a.startswith("products"): return "products"
    if a == "service.html": return "service"
    if a == "delivery.html": return "delivery"
    if a == "company.html": return "company"
    if a == "history.html": return "history"
    if a.startswith("recruit"): return "recruit"
    return ""

def header(active="", recruit=False, overlay=False):
    akey = _active_key(active)
    items_html = ""
    sp_html = ""
    for key, label, url, mega, children in NAV_GROUPS:
        is_active = " is-active" if key == akey else ""
        if not mega:
            items_html += f'<div class="gnav__item{is_active}"><a class="gnav__link" href="{url}">{label}</a></div>'
            sp_html += f'<a class="spmenu__single" href="{url}">{label}</a>'
            continue
        en = NAV_EN.get(key, label)
        if mega == "cards":
            cards = "".join(
                f'<a class="mega__card" href="{cu}"><span class="mega__thumb">Image</span>'
                f'<span class="mega__cap">{cn}<i>›</i></span></a>' for cn, cu in children)
            panel = f'<div class="mega__cards">{cards}</div>'
        else:
            links = "".join(f'<li><a href="{cu}">{cn}<i>›</i></a></li>' for cn, cu in children)
            panel = f'<ul class="mega__links">{links}</ul>'
        items_html += (
            f'<div class="gnav__item{is_active}" data-mega>'
            f'<a class="gnav__link" href="{url}">{label}</a>'
            f'<div class="mega"><div class="mega__inner">'
            f'<div class="mega__lead"><span class="mega__en">{en}</span>'
            f'<span class="mega__jp">{label}</span>'
            f'<a class="mega__more" href="{url}">詳しく見る →</a></div>'
            f'{panel}</div></div></div>')
        sub = "".join(f'<a href="{cu}">{cn}</a>' for cn, cu in children)
        sp_html += (f'<div class="spmenu__group"><button class="spmenu__top" aria-expanded="false">{label}</button>'
                    f'<div class="spmenu__sub">{sub}</div></div>')
    return f'''<header class="nav">
  <a class="logo" href="top.html"><span class="logo-mark">近江度量衡</span><span class="logo-en">125th SINCE 1900</span></a>
  <nav class="gnav">{items_html}</nav>
</header>
<button class="burger" aria-label="メニュー" aria-expanded="false"><span></span><span></span><span></span></button>
<div class="spmenu" id="spmenu" aria-hidden="true"><nav class="spmenu__nav">{sp_html}</nav></div>'''

def breadcrumb(items):
    parts = []
    for i,(label,url) in enumerate(items):
        if url and i < len(items)-1:
            parts.append(f'<a href="{url}">{label}</a>')
        else:
            parts.append(f'<span style="color:#333">{label}</span>')
    return '<nav class="breadcrumb"><div class="inner">' + '<span>›</span>'.join(parts) + '</div></nav>'

def footer(recruit=False):
    # d_3 トーンのフッター（ブランド＋3カラム＋著作権バー）。TOPと統一。
    return '''
<footer class="foot">
  <div class="foot__cols">
    <div class="foot__brand">
      <span class="foot__logo">近江度量衡株式会社</span>
      <p class="foot__tagline"><b>OMISCALE CO.,LTD.</b>「いきる」をはかり、豊かな世界へ。</p>
      <div class="foot__info">
        〒525-0054　滋賀県草津市東矢倉三丁目11番70号<br>
        TEL 077-562-7111／受付 平日 9:00〜17:00<br>
        国内6拠点＋海外3拠点（上海・バンコク・韓国）
      </div>
    </div>
    <div class="foot__col">
      <h4>製品・技術</h4>
      <ul>
        <li><a href="products.html">製品・技術紹介</a></li>
        <li><a href="products-agricultural.html">農産物用計量システム</a></li>
        <li><a href="products-weighing.html">穀類用計量システム</a></li>
        <li><a href="products-industry.html">工業用計量システム</a></li>
        <li><a href="products-other.html">その他・特殊用途</a></li>
        <li><a href="service.html">サービス案内</a></li>
        <li><a href="delivery.html">納入実績</a></li>
      </ul>
    </div>
    <div class="foot__col">
      <h4>企業情報</h4>
      <ul>
        <li><a href="company.html">会社案内</a></li>
        <li><a href="history.html">126年ヒストリー</a></li>
        <li><a href="news.html">新着情報</a></li>
        <li><a href="contact.html">お問い合わせ</a></li>
        <li><a href="privacy.html">プライバシーポリシー</a></li>
      </ul>
    </div>
    <div class="foot__col">
      <h4>採用情報</h4>
      <ul>
        <li><a href="recruit.html">採用TOP</a></li>
        <li><a href="recruit-interview.html">社員インタビュー</a></li>
        <li><a href="recruit-news.html">採用ニュース</a></li>
        <li><a href="recruit-jobs.html">募集要項</a></li>
        <li><a href="recruit-jobs-graduate.html">新卒採用</a></li>
        <li><a href="recruit-jobs-career.html">中途採用</a></li>
      </ul>
    </div>
  </div>
  <div class="foot__bar"><a href="privacy.html">Privacy Policy</a><span>© 2026 OMISCALE CO.,LTD. All Rights Reserved.</span></div>
</footer>'''

def page(filename, title, body, active="", recruit=False, crumbs=None, overlay=False):
    bc = breadcrumb(crumbs) if crumbs else ""
    cls = ' class="theme-recruit"' if recruit else ""
    html = f'''<!DOCTYPE html>
<html lang="ja"{cls}>
<head>
{AUTH_HEAD}
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@500;600;700;800&family=Noto+Sans+JP:wght@400;500;700;900&family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
{header(active, recruit, overlay)}
{bc}
{body}
{footer(recruit)}
<script src="_nav.js"></script>
</body>
</html>'''
    with open(os.path.join(OUT, filename), "w", encoding="utf-8") as f:
        f.write(html)
    return filename

PAGES = []  # 後でindex生成に使う: (No, 名称, url, file, group, cms)

# ======================= A. TOP =======================
top_body = '''
<section class="fv fv--full fv--center">
  <div class="fv__bg">
    <div class="fv__ph"><span>FV：全画面動画エリア（枠のみ・動画は後で挿入）</span></div>
  </div>
  <div class="fv__content">
    <h1 class="fv__title"><span>「いきる」をはかり、</span><span>豊かな世界へ。</span></h1>
  </div>
  <div class="fv__scroll">SCROLL</div>
</section>

<!-- ② 採用テザー（FV直下バナー） -->
<div class="recruit-banner">
  <div class="recruit-banner__inner">
    <div class="recruit-banner__text"><h2>「いきる」の単位とは、なんだろう。</h2><p>RECRUITMENT 採用情報</p></div>
    <div class="recruit-banner__cta"><a class="btn btn--white" href="recruit.html">採用サイトへ ↗</a></div>
  </div>
</div>

<!-- ③ PRODUCTS -->
<section class="section">
  <div class="container">
    <p class="section-meta">Products &amp; Technology</p>
    <h2 class="section-title">製品・技術紹介</h2>
    <div class="grid-4" style="margin-top:32px;">
      <a class="card" href="products-agricultural.html"><div class="card__img">''' + ph('農産物 選果イメージ') + '''</div><div class="card__body"><div class="card__title">農産物用計量システム</div><p class="card__text">果物・野菜向けの計量・選別システム。品質管理・等級選別に対応。</p></div></a>
      <a class="card" href="products-weighing.html"><div class="card__img">''' + ph('穀類施設イメージ') + '''</div><div class="card__body"><div class="card__title">穀類用計量システム</div><p class="card__text">米・大豆などの穀類計量システム。全国約2,000施設への納入実績。</p></div></a>
      <a class="card" href="products-industry.html"><div class="card__img">''' + ph('工場ラインイメージ') + '''</div><div class="card__body"><div class="card__title">工業用計量システム</div><p class="card__text">ガラス・鉄鋼・肥料・化学など7カテゴリに対応する計量ソリューション。</p></div></a>
      <a class="card" href="products-other.html"><div class="card__img">''' + ph('特殊用途イメージ') + '''</div><div class="card__body"><div class="card__title">その他・特殊用途</div><p class="card__text">家畜・競走馬向け動物計量など、特殊用途の計量システム。</p></div></a>
    </div>
  </div>
</section>

<!-- ④ 納入実績テザー -->
<section class="section section--grey">
  <div class="container">
    <div class="grid-2" style="align-items:center;">
      <div>''' + ph('導入現場 写真（選果場／カントリーエレベーター／工場ライン）','','aspect-ratio:4/3') + '''</div>
      <div>
        <p class="section-meta">Delivery Record</p>
        <h2 class="section-title">導入事例・納入実績</h2>
        <p class="section-lead">農産物選果場・米麦カントリーエレベーター・工場ラインなど、多岐にわたる現場への納入実績をご紹介します。</p>
        <a class="btn btn--outline btn--sm" href="delivery.html" style="margin-top:24px;">納入実績を見る</a>
      </div>
    </div>
  </div>
</section>

<!-- ⑤ STATEMENT -->
<section class="section section--dark">
  <div class="container statement">
    <p class="statement__en">OUR STATEMENT</p>
    <h2 class="statement__main">「いきる」をはかり、豊かな世界へ。</h2>
    <p class="statement__body">1900年の創業以来、客観的に、正確に「はかる」ことを命題として歩んできた近江度量衡。農産物から工業製品まで——あらゆる現場で今も使われ続けている、現在進行形の技術力と誠実さ。「はかる」という仕事を通じて、日本と世界の社会を確かに支え続けること。それが、126年間変わらない私たちの使命です。</p>
    <div class="grid-3" style="margin-top:48px;text-align:left;">
      <div class="pillar"><div class="pillar__no">社是 01</div><div class="pillar__title">社会への貢献</div><p class="pillar__body">企業を通じた社会貢献と従業員の生活向上</p></div>
      <div class="pillar"><div class="pillar__no">社是 02</div><div class="pillar__title">技術の公用</div><p class="pillar__body">技術発展と優良品の製造</p></div>
      <div class="pillar"><div class="pillar__no">社是 03</div><div class="pillar__title">互助の精神</div><p class="pillar__body">職場の繁栄に向けた互助・協力</p></div>
    </div>
  </div>
</section>

<!-- ⑥ HISTORY ダイジェスト -->
<section class="section">
  <div class="container">
    <p class="section-meta">126 Years History</p>
    <h2 class="section-title">明治から令和へ。測り続けた126年。</h2>
    <p class="section-lead">1900年の創業から現在まで、時代とともに進化してきた近江度量衡の歩みをダイジェストでご紹介します。</p>
    <div class="timeline" style="margin-top:32px;">
      <div class="timeline-item"><div class="timeline-year"><span class="timeline-year__era">明治33年</span><span class="timeline-year__num">1900</span></div><div class="timeline-dot"></div><div class="timeline-content"><h3>創業</h3><p>滋賀県にて計量器の製造・販売を開始。農産物の取引計量を支える地域の職人集団として出発。</p></div></div>
      <div class="timeline-item"><div class="timeline-year"><span class="timeline-year__era">昭和中期</span><span class="timeline-year__num">1950s</span></div><div class="timeline-dot"></div><div class="timeline-content"><h3>選果機需要が急拡大</h3><p>高度経済成長期、農協向け選果・計量システムの供給体制を確立。全国への展開が始まる。</p></div></div>
      <div class="timeline-item"><div class="timeline-year"><span class="timeline-year__era">平成12年</span><span class="timeline-year__num">2000</span></div><div class="timeline-dot"></div><div class="timeline-content"><h3>ISO 9001 認証取得</h3><p>品質保証体制を国際規格で整備。全数検査・精度管理の仕組みを標準化。</p></div></div>
      <div class="timeline-item"><div class="timeline-year"><span class="timeline-year__era">平成期</span><span class="timeline-year__num">2010s</span></div><div class="timeline-dot"></div><div class="timeline-content"><h3>海外展開開始（上海・バンコク・韓国）</h3><p>アジアの農産物・食品産業の成長とともに海外3拠点を設立。技術と誇りを海外へ。</p></div></div>
      <div class="timeline-item"><div class="timeline-year"><span class="timeline-year__era">令和7年</span><span class="timeline-year__num">2025</span></div><div class="timeline-dot"></div><div class="timeline-content"><h3>創業126周年</h3><p>国内6拠点・海外3拠点・累計2,000施設への納入実績。次の126年へ向けたWebリニューアルプロジェクト進行中。</p></div></div>
    </div>
    <a class="btn btn--outline btn--sm" href="history.html" style="margin-top:32px;">126年ヒストリーを見る</a>
  </div>
</section>

<!-- ⑦ RECRUITMENT -->
<section class="section section--dark theme-recruit" style="background:#1a0d0d;">
  <div class="container">
    <p class="statement__en" style="color:#c98;">RECRUITMENT</p>
    <h2 class="statement__main" style="text-align:left;color:#fff;">「いきる」の単位とは、なんだろう。</h2>
    <p class="section-lead" style="color:#cbb;">地に足のついた仕事のリアル・職場環境・社員の声——飾らず正直に。あなたの確かな仕事で、豊かな未来を担う力になる。</p>
    <div class="entry-split" style="margin-top:40px;">
      <div class="entry-card"><div class="entry-card__label">NEW GRADUATE 新卒採用</div><div class="entry-card__copy">「未来を、ここからはかる。」</div><p class="entry-card__desc">理系・工学系だけじゃない。着実にものをつくる誠実さに共感できる人を求めています。</p><a class="btn btn--red" href="recruit-jobs-graduate.html" style="background:#111315;color:#fff;">新卒採用を見る</a></div>
      <div class="entry-card"><div class="entry-card__label">MID-CAREER 中途採用</div><div class="entry-card__copy">「培った経験を、126年の精度に加えてください。」</div><p class="entry-card__desc">年齢・業界不問。あなたの経験が、次の100年の基盤になる。</p><a class="btn btn--red" href="recruit-jobs-career.html" style="background:#111315;color:#fff;">中途採用を見る</a></div>
    </div>
  </div>
</section>

<!-- ⑧ PEOPLE -->
<section class="section section--grey">
  <div class="container">
    <p class="section-meta">People</p>
    <h2 class="section-title">技術と誇りを持って働く、近江の現場のことば。</h2>
    <p class="section-lead">現場・設計・営業——それぞれの視点で語る、近江度量衡の仕事。''' + todo('実在する社員情報・コメントに差し替え') + '''</p>
    <div class="grid-3" style="margin-top:32px;">
      <div class="interview-card"><div class="interview-card__img">''' + ph('社員写真') + '''</div><div class="interview-card__body"><div class="interview-card__dept">製造部</div><div class="interview-card__name">山田 〇〇</div><p class="interview-card__quote">毎回違う課題に向き合うから、技術者として本当に成長できる。誇りを持てる仕事です。</p></div></div>
      <div class="interview-card"><div class="interview-card__img">''' + ph('社員写真') + '''</div><div class="interview-card__body"><div class="interview-card__dept">設計部</div><div class="interview-card__name">鈴木 〇〇</div><p class="interview-card__quote">図面通りにつくるのではなく、現場に合わせてつくる。グローバルな現場を支える実感があります。</p></div></div>
      <div class="interview-card"><div class="interview-card__img">''' + ph('社員写真') + '''</div><div class="interview-card__body"><div class="interview-card__dept">営業部</div><div class="interview-card__name">田中 〇〇</div><p class="interview-card__quote">お客様の現場を見て、何が必要か考える。「いきる」をはかるという仕事の意味がここにあります。</p></div></div>
    </div>
    <a class="btn btn--outline btn--sm" href="recruit-interview.html" style="margin-top:32px;">社員インタビューを見る</a>
  </div>
</section>

<!-- ⑨ NEWS -->
<section class="section">
  <div class="container">
    <p class="section-meta">News</p>
    <h2 class="section-title">新着情報 ''' + cms('クライアント更新') + '''</h2>
    <ul class="news-list" style="margin-top:24px;">
      <li class="news-item"><span class="news-item__date">2025.06.01</span><span class="news-item__cat">お知らせ</span><span class="news-item__title">北海道営業所を開設しました</span></li>
      <li class="news-item"><span class="news-item__date">2025.03.01</span><span class="news-item__cat">お知らせ</span><span class="news-item__title">会社設立126周年を達成しました</span></li>
      <li class="news-item"><span class="news-item__date">2025.04.01</span><span class="news-item__cat">採用</span><span class="news-item__title">2027年度採用エントリー受付開始のご案内</span></li>
    </ul>
    <div class="cms-note">★ 表示はサンプル。実際の記事はクライアントがWordPress管理画面から都度更新（月1〜2本）。</div>
    <a class="btn btn--outline btn--sm" href="news.html" style="margin-top:24px;">新着情報一覧へ</a>
  </div>
</section>
'''
# 【TOP は別管理】TOPページは d_3 デザインベースの専用HTML（モノトーン・ダミー、自己完結のCSS/JS）を
#   手管理しているため、build.py では top.html を生成・上書きしない。
#   （旧ワイヤーTOPの top_body は未使用。レイアウト参考として残置）
# page("top.html", "近江度量衡株式会社｜「いきる」をはかり、豊かな世界へ。", top_body, active="", overlay=True)
PAGES.append(("A","トップページ","/","top.html","corp",False))

# ======================= B. 製品・技術紹介 =======================
products_body = '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">PRODUCTS &amp; TECHNOLOGY</p>
  <h1 class="page-header__title">製品・技術紹介</h1>
  <p class="page-header__lead">農産物・穀類・工業用など、あらゆる現場の計量ニーズに一品一様で応えます。</p>
</div></header>
<section class="section"><div class="container">
  <div class="grid-2">
    <a class="cat-card" href="products-agricultural.html"><div class="cat-card__img">''' + ph('AGRICULTURAL イメージ') + '''</div><div class="cat-card__body"><div class="cat-card__slug">AGRICULTURAL</div><div class="cat-card__title">農産物用計量システム</div><p class="cat-card__desc">果物・野菜向けの計量・選別システム。品質管理・等級選別に対応。</p><span class="cat-card__link">詳しく見る →</span></div></a>
    <a class="cat-card" href="products-weighing.html"><div class="cat-card__img">''' + ph('GRAIN イメージ') + '''</div><div class="cat-card__body"><div class="cat-card__slug">GRAIN</div><div class="cat-card__title">穀類用計量システム</div><p class="cat-card__desc">米・大豆などの穀類計量システム。全国約2,000施設への納入実績。</p><span class="cat-card__link">詳しく見る →</span></div></a>
    <a class="cat-card" href="products-industry.html"><div class="cat-card__img">''' + ph('INDUSTRIAL イメージ') + '''</div><div class="cat-card__body"><div class="cat-card__slug">INDUSTRIAL</div><div class="cat-card__title">工業用計量システム</div><p class="cat-card__desc">ガラス・鉄鋼・肥料・化学など7カテゴリに対応する計量ソリューション。</p><span class="cat-card__link">詳しく見る →</span></div></a>
    <a class="cat-card" href="products-other.html"><div class="cat-card__img">''' + ph('OTHERS イメージ') + '''</div><div class="cat-card__body"><div class="cat-card__slug">OTHERS</div><div class="cat-card__title">その他・特殊用途</div><p class="cat-card__desc">家畜・競走馬向け動物計量など、特殊用途の計量システム。</p><span class="cat-card__link">詳しく見る →</span></div></a>
  </div>
  <div class="cms-note">◯ 製品ページは投稿（カスタム投稿）で管理。新製品・新設備竣工時にクライアントが追加・更新（年1〜2件想定）。''' + cms('CMS更新') + '''</div>
</div></section>
<div class="recruit-banner" style="background:#222;"><div class="recruit-banner__inner">
  <div class="recruit-banner__text"><h2 style="font-size:24px;">製品・技術についてのお問い合わせ</h2><p>仕様・価格・納期・カスタマイズについてはご相談可能な体制を整備。</p></div>
  <div class="recruit-banner__cta"><a class="btn btn--white" href="contact.html">お問い合わせ</a></div>
</div></div>
'''
page("products.html","製品・技術紹介｜近江度量衡株式会社", products_body, active="products.html",
     crumbs=[("TOP","top.html"),("製品・技術紹介",None)])
PAGES.append(("B","製品・技術紹介","/products/","products.html","corp",True))

# ---- 製品サブページ共通テンプレ ----
def product_detail(slug_en, name, desc, features, uses, assets_note=""):
    feat = "".join(f'<li>{f}</li>' for f in features)
    use = "".join(f'<div class="use-item"><span class="use-item__no">用途 0{i+1}</span>{u}</div>' for i,u in enumerate(uses))
    asset = ('<div class="cms-note">参考素材（Drive）：' + assets_note + '</div>') if assets_note else ''
    return '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">''' + slug_en + '''</p>
  <h1 class="page-header__title">''' + name + '''</h1>
</div></header>
<section class="section"><div class="container grid-2" style="align-items:start;">
  <div>''' + ph(name + ' 製品イメージ／図解','','aspect-ratio:4/3') + asset + '''</div>
  <div><p class="section-lead" style="margin-top:0;">''' + desc + '''</p>
  <div class="cms-note" style="background:#fff7ec;border-left-color:#e0a030;">注記：詳細仕様・写真は機密保持の都合により非掲載。別途資料をご請求ください。</div></div>
</div></section>
<section class="section section--grey"><div class="container">
  <p class="section-meta">Features</p><h2 class="section-title">主な特長</h2>
  <ul class="feature-list" style="margin-top:24px;max-width:760px;">''' + feat + '''</ul>
</div></section>
<section class="section"><div class="container">
  <p class="section-meta">Use Case</p><h2 class="section-title">主な用途・導入現場</h2>
  <div class="use-grid" style="margin-top:24px;">''' + use + '''</div>
</div></section>
<div class="recruit-banner" style="background:#222;"><div class="recruit-banner__inner">
  <div class="recruit-banner__text"><h2 style="font-size:24px;">''' + name + '''についてのお問い合わせ</h2></div>
  <div class="recruit-banner__cta"><a class="btn btn--white" href="contact.html">お問い合わせ</a></div>
</div></div>
'''

def pdf_box(title, meta, href):
    return ('<div class="pdf-box"><div class="pdf-box__ic">PDF</div>'
      '<div class="pdf-box__body"><div class="pdf-box__title">'+title+'</div>'
      '<div class="pdf-box__meta">'+meta+'</div></div>'
      '<div class="pdf-box__btns"><a class="btn btn--dark btn--sm" href="'+href+'" target="_blank">PDFを開く</a>'
      '<a class="btn btn--outline btn--sm" href="'+href+'" download>ダウンロード</a></div></div>')

def machine(en, jp, target, bullets, imglabel):
    b = "".join('<li>'+x+'</li>' for x in bullets)
    return ('<div class="case" style="margin-top:24px;"><div class="case__img">'+ph(imglabel)+'</div>'
      '<div class="case__body"><div class="machine-meta">'+en+'</div>'
      '<div class="case__title" style="margin:0;">'+jp+'</div>'
      '<div class="machine-target">'+target+'</div>'
      '<ul class="feature-list" style="margin-top:4px;">'+b+'</ul></div></div>')

# ===== B1 農産物用：OMI STAR シリーズ（2021 STARパンフレット反映） =====
agri_body = '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">AGRICULTURAL</p>
  <h1 class="page-header__title">農産物用計量システム</h1>
  <p class="page-header__lead">選別機の新星「OMI STAR シリーズ」が「はかる」技術をさらに加速。柑橘から小粒農産物・根菜類まで、農産物を選ばない 3ライン＋α でお応えします。</p>
</div></header>
<section class="section"><div class="container">
  <p class="section-meta">STAR Series</p>
  <h2 class="section-title">画期的な技術を結集した高精度の選果システム</h2>
  <p class="section-lead">農産物選果は新しい時代へ。重量・外観を高精度に「はかる」3つの選別機（Rollerstar／Millistar／Calistar）＋ 柑橘選果システム（＋α）で、産地・農協の現場に一品一様で対応します。''' + todo('製品写真：Calistar.jpg / Millister.jpg / Rollerster.jpg（Drive B_製品）') + '''</p>
</div></section>
<section class="section section--grey"><div class="container">
  <p class="section-meta">3 Lines</p><h2 class="section-title">STAR シリーズ 3機種</h2>
''' + machine("Rollerstar ／ ローラスター","柑橘・落葉果実・トマト などの農産物の選別に最適",
      "対応：柑橘・落葉果実・トマト",
      ["二個乗りを防ぐ独自の整列機構","1グラム単位で正確に重量を測定できる「はかる」技術","最大16個／秒／条を正確に選別仕分けできる高能力を実現"],
      "Rollerstar 製品写真") + machine("Millistar ／ ミリスター","ミニトマト・キンカン など小粒農産物を選別仕分け",
      "対応：ミニトマト・キンカン・小粒農作物",
      ["25個／秒／条で農産物を選別仕分けする能力","二個乗りを確実に防ぐ整列コンベアが選果能力をアシスト","1つのワークを8面画像認識し形状や色彩を見分ける Advanced Vision 搭載","低騒音で働く人にやさしい作業環境を実現"],
      "Millistar 製品写真") + machine("Calistar ／ キャリスター","根菜類・パプリカ・玉ねぎ・柑橘 など農産物を選ばないオールランダー",
      "対応：根菜類・パプリカ・玉ねぎ・柑橘 ほか",
      ["吊り下げ方式搬送体が更に高精度な重量測定を実現","小さなものから大きなものまで確実にホールドできるクリッパー","吊り下げ方式の搬送体だから実現できる低落差","根菜類など土モノの土砂の影響を受けない安心構造"],
      "Calistar 製品写真") + '''
  <div class="cms-note">＋α：高精度・高性能の「柑橘選果システム」もラインアップ。</div>
</div></section>
<section class="section"><div class="container">
  <p class="section-meta">Case Study</p><h2 class="section-title">導入事例</h2>
  <div class="grid-3" style="margin-top:24px;">
    <div class="card"><div class="card__img">''' + ph('JA熊本うき 宇城柑橘選果場') + '''</div><div class="card__body"><div class="card__title">JA熊本うき 宇城柑橘選果場様</div><p class="card__text">世界初、温州みかんを予冷から同一ラインで選果可能にした大型プラント。</p></div></div>
    <div class="card"><div class="card__img">''' + ph('奄美市 奄美大島選果場') + '''</div><div class="card__body"><div class="card__title">奄美市 奄美大島選果場様</div><p class="card__text">高精度の内部・外部品質管理を実現した、奄美タンカン選果ライン。</p></div></div>
    <div class="card"><div class="card__img">''' + ph('有限会社さもと農園') + '''</div><div class="card__body"><div class="card__title">三重県 有限会社さもと農園様</div><p class="card__text">機能を絞った小規模プラントにも対応。</p></div></div>
  </div>
  ''' + pdf_box("2021 STAR シリーズ パンフレット","農産物選別機 Rollerstar／Millistar／Calistar（PDF）","assets/star-series.pdf") + '''
</div></section>
<div class="recruit-banner" style="background:#222;"><div class="recruit-banner__inner">
  <div class="recruit-banner__text"><h2 style="font-size:24px;">農産物用計量システムについてのお問い合わせ</h2></div>
  <div class="recruit-banner__cta"><a class="btn btn--white" href="contact.html">お問い合わせ</a></div>
</div></div>
'''
page("products-agricultural.html","農産物用計量システム｜近江度量衡株式会社", agri_body,
  active="products.html", crumbs=[("TOP","top.html"),("製品・技術紹介","products.html"),("農産物用",None)])
PAGES.append(("B1","農産物用計量システム","/products/agricultural/","products-agricultural.html","corp",True))

# ===== B2 穀類用：フルオートドライヤーシステム（DRYER SYSTEM反映） =====
grain_body = '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">GRAIN</p>
  <h1 class="page-header__title">穀類用計量システム</h1>
  <p class="page-header__lead">全国約2,000施設への納入実績。サンプル全自動自主検査「フルオートドライヤーシステム」で、穀類の自主検査工程を効率化します。</p>
</div></header>
<section class="section"><div class="container grid-2" style="align-items:start;">
  <div>''' + ph('フルオートドライヤーシステム 本体（CFD-120）','','aspect-ratio:4/3') + todo('製品写真：image_main / image_3D / image_panel（Drive B_製品 フルオートドライヤー）') + '''</div>
  <div>
    <p class="section-meta">OMI Total Full-Automatic Dryer System</p>
    <h2 class="section-title" style="font-size:24px;">フルオートドライヤーシステム</h2>
    <p class="section-lead" style="margin-top:12px;">業界初のサンプル全自動自主検査装置が、さらなる高効率化を実現してフルモデルチェンジ。200年以上の穀類フルオートドライヤー納入で培ったノウハウを結集し、現代のプラント設備に求められる性能を高い完成度で実現した新型システムです。<strong>米・麦・大豆の3品目兼用。</strong></p>
  </div>
</div></section>
<section class="section section--grey"><div class="container">
  <p class="section-meta">Feature</p><h2 class="section-title">特長</h2>
  <div class="feat-grid">
    <div class="feat-item"><div class="no">01</div><h4>省人化</h4><p>計量・乾燥・検査の全工程をオートメーション化。</p></div>
    <div class="feat-item"><div class="no">02</div><h4>省エネ</h4><p>乾燥精度をたもつ消費電力の抑え込み制御。</p></div>
    <div class="feat-item"><div class="no">03</div><h4>省スペース</h4><p>約64%削減したコンパクトなサイズ。</p></div>
    <div class="feat-item"><div class="no">04</div><h4>3品目兼用</h4><p>米・大豆・麦の3品目兼用が可能。</p></div>
    <div class="feat-item"><div class="no">05</div><h4>トータルコスト</h4><p>更新時の据置工程を統合しトータルコスト削減。</p></div>
  </div>
</div></section>
<section class="section"><div class="container">
  <p class="section-meta">Flow</p><h2 class="section-title">工程</h2>
  <div class="process" style="margin-top:24px;">
    <div class="process-step"><div class="process-step__num">01</div><div class="process-step__title">投入</div></div>
    <div class="process-step"><div class="process-step__num">02</div><div class="process-step__title">計量</div></div>
    <div class="process-step"><div class="process-step__num">03</div><div class="process-step__title">サンプル抽出</div></div>
    <div class="process-step"><div class="process-step__num">04</div><div class="process-step__title">乾燥</div></div>
    <div class="process-step"><div class="process-step__num">05</div><div class="process-step__title">検査</div></div>
  </div>
  <div class="grid-3" style="margin-top:32px;">
    <div class="value-item"><div class="value-item__title" style="font-size:15px;">搬送部</div><p class="value-item__body">搬送用ロボットアーム・昇降エレベーター・定量供給で、サンプルを確実に搬送。</p></div>
    <div class="value-item"><div class="value-item__title" style="font-size:15px;">サンプルボックス</div><p class="value-item__body">10ボックス×6段×2テーブル、計120サンプルを管理。</p></div>
    <div class="value-item"><div class="value-item__title" style="font-size:15px;">オートチェッカー</div><p class="value-item__body">抽出したサンプルを自動で検査し、自主検査工程を全自動化。</p></div>
  </div>
</div></section>
<section class="section section--grey" id="spec"><div class="container">
  <p class="section-meta">Spec &amp; Dimension</p><h2 class="section-title">仕様・寸法図（ドライヤー本体）</h2>
  <div class="spec-2col">
    <figure class="dim-figure"><img src="assets/dryer-dimension.png" alt="フルオートドライヤーシステム 寸法図"><figcaption>DIMENSION 寸法図（裏表紙より）</figcaption></figure>
    <table class="info-table" style="background:#fff;">
      <tr><th>型式</th><td>CFD-120</td></tr>
      <tr><th>対象物</th><td>穀類（米・麦・大豆）</td></tr>
      <tr><th>本体寸法（出荷時）</th><td>幅 2,020 × 高さ 1,800 × 奥行 700（mm）</td></tr>
      <tr><th>処理量</th><td>120サンプル（10ボックス×6段×2テーブル）</td></tr>
      <tr><th>操作部</th><td>7インチ型タッチパネル</td></tr>
      <tr><th>塗装色</th><td>マンセル 5Y7/1</td></tr>
      <tr><th>サンプルボックス最大投入量</th><td>約 800g（粉）</td></tr>
      <tr><th>機器重量</th><td>850kg</td></tr>
      <tr><th>消費電力</th><td>200V 約3.6kW 4.2KVA 18A</td></tr>
      <tr><th>消費エアー量</th><td>25L/min</td></tr>
      <tr><th>排風量</th><td>12㎥/min（50Hz）／14㎥/min（60Hz）</td></tr>
      <tr><th>備考</th><td>最大4台での連結可能／ヒーター自動温度制御／セーフティスイッチ／機内照明搭載</td></tr>
    </table>
  </div>
  ''' + pdf_box("フルオートドライヤーシステム 製品資料","OMI TOTAL FULL-AUTOMATIC DRYER SYSTEM（特長・工程・仕様・寸法図／PDF）","assets/dryer-system.pdf") + '''
</div></section>
<div class="recruit-banner" style="background:#222;"><div class="recruit-banner__inner">
  <div class="recruit-banner__text"><h2 style="font-size:24px;">穀類用計量システムについてのお問い合わせ</h2></div>
  <div class="recruit-banner__cta"><a class="btn btn--white" href="contact.html">お問い合わせ</a></div>
</div></div>
'''
page("products-weighing.html","穀類用計量システム｜近江度量衡株式会社", grain_body,
  active="products.html", crumbs=[("TOP","top.html"),("製品・技術紹介","products.html"),("穀類用",None)])
PAGES.append(("B2","穀類用計量システム","/products/weighing/","products-weighing.html","corp",True))

# ===== B3 工業用：工業分野（会社案内2025 工業ページ反映） =====
ind_body = '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">INDUSTRY</p>
  <h1 class="page-header__title">工業用計量システム</h1>
  <p class="page-header__lead">あらゆる工業分野で品質を支える「はかる」技術。</p>
</div></header>
<section class="section"><div class="container grid-2" style="align-items:center;">
  <div>
    <p style="font-size:14px;color:#444;line-height:2;">工業用ゴム、樹脂、ガラス、金属、化学薬品など、近江度量衡には様々な工業製品の原料や薬品の計量配合プラントの納入実績があります。液体、粉体、ペレット、顆粒状など様々な形状の原料をはかるノウハウで、産業分野を超えてお客様のニーズに応えます。</p>
  </div>
  <div>''' + ph('計量配合プラント 全体イメージ','','aspect-ratio:16/10') + '''</div>
</div></section>
<section class="section section--grey"><div class="container">
  <p class="section-meta">Products</p>
  <h2 class="section-title">一台の計量機から製造ライン全体まで。</h2>
  <p class="section-lead">高精度、高生産性の装置でものづくり現場を支えます。</p>
  <div class="grid-2" style="margin-top:28px;">
    <div class="card" style="background:#fff;"><div class="card__img">''' + ph('粉体原料用ホッパースケール') + '''</div><div class="card__body"><div class="card__title">粉体原料計量システム</div><p class="card__text">ガラス製品の製造工程では、計量だけでなく、原料の貯蔵・自動調合・ミキシング・定量供給装置など、製造工程のほとんどのプロセスの装置とシステムを手掛けます。流動性に優れた構造で、硬質素材と摩耗対策により高い耐久性を備えた高能力のシステムを提供しています。</p></div></div>
    <div class="card" style="background:#fff;"><div class="card__img">''' + ph('ゴム混練設備計量機') + '''</div><div class="card__body"><div class="card__title">タイヤ・工業用ゴム計量システム</div><p class="card__text">プラント全体における上流工程の原料計量設備、下流工程の完成品計量設備、その間の各ライン設備を設計・製作。さらに完全自動化のための生産管理統合システムを提供し、安定した精度を保ち、生産性向上と品質の保証に大きく寄与しています。</p></div></div>
  </div>
</div></section>
<section class="section"><div class="container grid-2" style="align-items:center;">
  <div>
    <p class="section-meta">Total Engineering</p>
    <h2 class="section-title" style="font-size:24px;">ソフトウェアもハードウェアも自社製造で一括管理</h2>
    <p class="section-lead">高精度な計量を実現するためには、機械設備の設計・製作だけでなく、それらを制御するシステム開発が欠かせません。電気設備の設計・構築を専門とする技術電装部を抱え、機械設備の設計を行う設計部、製造を担当する製造部が連携したトータルエンジニアリングで、お客様に安心してお使いいただけるシステムをお届けしています。</p>
  </div>
  <div>''' + ph('電子部品の組立まで自社で実施','','aspect-ratio:4/3') + '''</div>
</div></section>
<section class="section section--grey"><div class="container">
  ''' + pdf_box("会社案内パンフレット 2025年版","工業分野ほか 事業・技術紹介（PDF）","assets/company-2025.pdf") + '''
</div></section>
<div class="recruit-banner" style="background:#222;"><div class="recruit-banner__inner">
  <div class="recruit-banner__text"><h2 style="font-size:24px;">工業用計量システムについてのお問い合わせ</h2></div>
  <div class="recruit-banner__cta"><a class="btn btn--white" href="contact.html">お問い合わせ</a></div>
</div></div>
'''
page("products-industry.html","工業用計量システム｜近江度量衡株式会社", ind_body,
  active="products.html", crumbs=[("TOP","top.html"),("製品・技術紹介","products.html"),("工業用",None)])
PAGES.append(("B3","工業用計量システム","/products/industry/","products-industry.html","corp",True))

page("products-other.html","その他・特殊用途｜近江度量衡株式会社",
  product_detail("OTHERS","その他・特殊用途",
    "家畜・競走馬向け動物計量など、特殊用途の計量システム。一品一様で多様な計量ニーズに対応します。",
    ["家畜・競走馬向け動物計量システム","特殊形状・特殊環境への個別対応","用途に応じた一品一様の設計・製造"],
    ["畜産施設","競走馬育成・管理施設","研究機関","その他特殊計量現場"]),
  active="products.html", crumbs=[("TOP","top.html"),("製品・技術紹介","products.html"),("その他",None)])
PAGES.append(("B4","その他・特殊用途","/products/other/","products-other.html","corp",True))

# ======================= C. サービス案内 =======================
service_body = '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">SERVICE</p>
  <h1 class="page-header__title">サービス案内</h1>
  <p class="page-header__lead">計量・測定のあらゆるニーズに対応するサービスを提供します。</p>
</div></header>
<section class="section"><div class="container">
  <div class="grid-2" style="gap:1px;background:var(--c-border);border:1px solid var(--c-border);">
    <div class="value-item" style="border:none;background:#fff;"><div class="value-item__num">01</div><div class="value-item__title">企画・エンジニアリング</div><p class="value-item__body">計量対象の特性や仕様条件について事前調査とヒアリングを実施。豊富な実績から類似事例を紹介し、現場に合った最適なシステムをご提案します。</p></div>
    <div class="value-item" style="border:none;background:#fff;"><div class="value-item__num">02</div><div class="value-item__title">設計</div><p class="value-item__body">ソフトウエアとハード製作の連携を重視。複数のデザインレビューを経て品質と精度を保証する高品質な設計を実現します。</p></div>
    <div class="value-item" style="border:none;background:#fff;"><div class="value-item__num">03</div><div class="value-item__title">製作・施工</div><p class="value-item__body">合理性を追求しニュープロダクト・システムを採用。コストパフォーマンスの高いシステムを製作・施工します。</p></div>
    <div class="value-item" style="border:none;background:#fff;"><div class="value-item__num">04</div><div class="value-item__title">メンテナンス・アフターサービス</div><p class="value-item__body">納入後も営業・技術サービス員が定期巡回。機器を最良の状態で維持するサポートを継続的に提供します。</p></div>
  </div>
</div></section>
<section class="section section--grey"><div class="container">
  <p class="section-meta">Flow</p><h2 class="section-title">ご依頼の流れ</h2>
  <div class="flow" style="margin-top:24px;max-width:760px;">
    <div class="flow-step"><div class="flow-step__num"></div><div class="flow-step__body"><h4>お問い合わせ</h4><p>Webフォーム・電話にてご連絡ください。</p></div></div>
    <div class="flow-step"><div class="flow-step__num"></div><div class="flow-step__body"><h4>現地調査・ヒアリング</h4><p>現場の状況を確認し、ご要望を詳しくお聞きします。</p></div></div>
    <div class="flow-step"><div class="flow-step__num"></div><div class="flow-step__body"><h4>提案・見積</h4><p>最適なシステム構成をご提案します。</p></div></div>
    <div class="flow-step"><div class="flow-step__num"></div><div class="flow-step__body"><h4>設計・製造</h4><p>一品一様で設計・製造します。</p></div></div>
    <div class="flow-step"><div class="flow-step__num"></div><div class="flow-step__body"><h4>納品・設置調整</h4><p>現地への納品・据付・調整を行います。</p></div></div>
    <div class="flow-step"><div class="flow-step__num"></div><div class="flow-step__body"><h4>保守・サポート</h4><p>全国ネットワークで継続サポートします。</p></div></div>
  </div>
</div></section>
<div class="recruit-banner" style="background:#222;"><div class="recruit-banner__inner">
  <div class="recruit-banner__text"><h2 style="font-size:24px;">サービス・保守についてのお問い合わせ</h2></div>
  <div class="recruit-banner__cta"><a class="btn btn--white" href="contact.html">お問い合わせ</a></div>
</div></div>
'''
page("service.html","サービス案内｜近江度量衡株式会社", service_body, active="service.html",
     crumbs=[("TOP","top.html"),("サービス案内",None)])
PAGES.append(("C","サービス案内","/service/","service.html","corp",False))

# ======================= D. 納入実績 =======================
delivery_body = '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">DELIVERY RECORD</p>
  <h1 class="page-header__title">納入実績</h1>
  <p class="page-header__lead">農産物選果場・穀類施設・工業ラインなど、多岐にわたる現場への納入実績。</p>
</div></header>

<!-- ② 統計フィーチャー -->
<section class="section"><div class="container">
  <div class="numbers-grid" style="grid-template-columns:repeat(5,1fr);">
    <div class="number-card"><div class="number-card__num">2,000<span class="number-card__unit">+</span></div><div class="number-card__label">累計納入施設数</div></div>
    <div class="number-card"><div class="number-card__num">126<span class="number-card__unit">年</span></div><div class="number-card__label">創業からの歴史</div></div>
    <div class="number-card"><div class="number-card__num">6<span class="number-card__unit">箇所</span></div><div class="number-card__label">国内サービス拠点</div></div>
    <div class="number-card"><div class="number-card__num">3<span class="number-card__unit">箇所</span></div><div class="number-card__label">海外サービス拠点</div></div>
    <div class="number-card"><div class="number-card__num">152<span class="number-card__unit">件</span></div><div class="number-card__label">選果機納入実績（1981〜2016年）</div></div>
  </div>
</div></section>

<!-- ③ 全国マップ（ver3：数字フィーチャー＋全国マップ形式） -->
<section class="section section--grey"><div class="container">
  <p class="section-meta">Service Area</p><h2 class="section-title">主な納入エリア</h2>
  <div class="basemap" style="margin-top:24px;">
    <div>''' + ph('全国／海外 納入マップ（ピン表示）','','aspect-ratio:4/3') + '''</div>
    <div>
      <p class="section-lead" style="margin-top:0;font-size:14px;">国内は北海道から九州まで全国対応。海外は中国（上海）、タイ（バンコク）、韓国に拠点展開。</p>
      <p style="font-size:12px;color:#666;margin-top:12px;line-height:2;">【国内】北海道・東北・関東・北陸・東海・近畿・中国・四国・九州・沖縄<br>【海外】中国・バンコク・韓国・アメリカ・ハンガリー</p>
    </div>
  </div>
</div></section>

<!-- ④⑤⑥ CASE -->
<section class="section"><div class="container">
  <p class="section-meta">Case Study</p><h2 class="section-title">導入事例</h2>''' + todo('クライアントより実際の案件名・詳細を提供') + '''

  <div class="case" style="margin-top:24px;">
    <div class="case__img">''' + ph('ふらの農協 玉葱選果場') + '''</div>
    <div class="case__body"><div class="case__cat">CASE 01 / 農産物用計量システム</div><div class="case__title">玉葱選果場の再編・統合（AIカメラ選別）</div>
      <table class="case__meta"><tr><th>導入先</th><td>ふらの農業協同組合（北海道）</td></tr><tr><th>導入年</th><td>2023年</td></tr><tr><th>規模</th><td>玉葱選別設備3系列／一日処理量 約400トン</td></tr>
      <tr><th>内容</th><td>既存の4ヶ所に分散していた玉葱選果場を再編・統合し1施設へ集約。AIカメラ選別システムで外観・内部品質を高精度判定。1玉ごとの重量計測で箱詰め時の入れ目ロスを低減し歩留まり向上に貢献。</td></tr></table>
      <div class="case__points"><span class="case__point">キャリスター（ハンガー式搬送体選別装置）</span><span class="case__point">AI画像処理装置による省人化</span><span class="case__point">1玉毎の重量計測で歩留まり向上</span></div>
    </div>
  </div>

  <div class="case" style="margin-top:24px;">
    <div class="case__img">''' + ph('カントリーエレベーター') + '''</div>
    <div class="case__body"><div class="case__cat">CASE 02 / 穀類用計量システム</div><div class="case__title">〇〇カントリーエレベーター 全工程刷新 ''' + todo('実案件待ち') + '''</div>
      <table class="case__meta"><tr><th>導入先</th><td>〇〇農産株式会社（〇〇県）</td></tr><tr><th>導入年</th><td>〇〇年</td></tr><tr><th>規模</th><td>受入ピット〇系統／袋詰めライン〇系統</td></tr>
      <tr><th>内容</th><td>受入から袋詰めまでの全工程をシステム化し、処理能力を従来比で大幅向上。タッチパネル操作で新任オペレーターも即日稼働可能に。</td></tr></table>
      <div class="case__points"><span class="case__point">処理能力向上</span><span class="case__point">品質管理自動化</span><span class="case__point">即日稼働可能</span></div>
    </div>
  </div>

  <div class="case" style="margin-top:24px;">
    <div class="case__img">''' + ph('工業プラント計量') + '''</div>
    <div class="case__body"><div class="case__cat">CASE 03 / 工業用計量システム</div><div class="case__title">〇〇化学工業 肥料製造ライン高精度化 ''' + todo('実案件待ち') + '''</div>
      <table class="case__meta"><tr><th>導入先</th><td>〇〇化学工業株式会社（〇〇県）</td></tr><tr><th>導入年</th><td>〇〇年</td></tr><tr><th>規模</th><td>計量ポイント〇箇所／24時間連続稼働</td></tr>
      <tr><th>内容</th><td>既設SCADAとのOPC-UA通信連携を実現し、リアルタイムデータ可視化と高精度計量でトレーサビリティを確保。</td></tr></table>
      <div class="case__points"><span class="case__point">リアルタイム可視化</span><span class="case__point">配合精度改善</span><span class="case__point">トレーサビリティ確保</span></div>
    </div>
  </div>
  <div class="cms-note">固定ページ。事例は更新頻度が低い（年0〜1件）ため、追加・修正は制作側で対応。</div>
</div></section>

<div class="recruit-banner" style="background:#222;"><div class="recruit-banner__inner">
  <div class="recruit-banner__text"><h2 style="font-size:24px;">掲載以外の実績についてお問い合わせください</h2><p>2,000施設以上の実績あり。詳細はお気軽にお問い合わせください。</p></div>
  <div class="recruit-banner__cta"><a class="btn btn--white" href="contact.html">お問い合わせ</a></div>
</div></div>
'''
page("delivery.html","納入実績｜近江度量衡株式会社", delivery_body, active="delivery.html",
     crumbs=[("TOP","top.html"),("納入実績",None)])
PAGES.append(("D","納入実績","/deliveryrecord/","delivery.html","corp",False))

# ======================= E. 会社案内 =======================
company_body = '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">COMPANY</p>
  <h1 class="page-header__title">会社案内</h1>
</div></header>
<nav class="page-nav"><div class="inner">
  <a href="#concept">企業理念</a><a href="#greeting">代表挨拶</a><a href="#servicebase">サービス拠点</a><a href="#profile">会社概要</a>
</div></nav>

<!-- ② 企業理念 -->
<section class="section section--dark" id="concept">
  <div class="container statement">
    <p class="statement__en">OUR STATEMENT — We measure the future</p>
    <h2 class="statement__main">「いきる」をはかり、豊かな世界へ。</h2>
    <p class="statement__body">1900年（明治33年）の創業以来、私たちは一貫して「はかる」という技術を磨き続けてきました。はかることは、単に数値を知ることではありません。品質を見極め、価値を創り、未来への可能性を拓くこと。時代が移り変わり、社会や産業の姿が大きく変化する中でも、私たちは常に新しい技術への挑戦を続け、お客様とともに未来を創り続けてきました。</p>
    <div class="grid-3" style="margin-top:48px;text-align:left;">
      <div class="pillar"><div class="pillar__no">社是 01</div><div class="pillar__title">社会貢献</div></div>
      <div class="pillar"><div class="pillar__no">社是 02</div><div class="pillar__title">技術の公用</div></div>
      <div class="pillar"><div class="pillar__no">社是 03</div><div class="pillar__title">互助の精神</div></div>
    </div>
  </div>
</section>

<!-- ③ MISSION / VISION / VALUES -->
<section class="section"><div class="container">
  <div class="grid-3">
    <div class="value-item"><div class="value-item__title">MISSION</div><p class="value-item__body">私たちは、はかる。重さを。量を。長さを。そして時には、品質を、価値を、未来を。一世紀以上に亘り受け継がれてきた技術と挑戦の精神は、これからも新しい時代へと受け継がれていきます。</p></div>
    <div class="value-item"><div class="value-item__title">VISION</div><p class="value-item__body">働く人が誇りを持てる場所から、お客様の信頼は生まれる。社員が豊かであることで初めてお客様への最良のサービスが生まれる。</p></div>
    <div class="value-item"><div class="value-item__title">VALUES</div><p class="value-item__body">堅実であること。誇りをもつこと。126年間ぶれずに現場と向き合ってきた姿勢と、仕事の社会的意義から生まれる誇り。</p></div>
  </div>
</div></section>

<!-- ④ 代表挨拶 -->
<section class="section section--grey" id="greeting"><div class="container grid-2" style="align-items:start;">
  <div>''' + ph('代表者写真（スーツ姿・顔出し）','','aspect-ratio:3/4') + todo('原稿(約800字)・写真をクライアント提供') + '''</div>
  <div>
    <p class="section-meta">Message</p><h2 class="section-title">代表挨拶</h2>
    <p style="font-size:13px;color:#888;margin-top:8px;">代表取締役社長　小谷 俊彦</p>
    <p style="font-size:14px;color:#444;line-height:2;margin-top:20px;">We Measure the Future.<br>私たち近江度量衡は、1900年の創業以来、126年以上にわたり「はかる」という技術を通じて社会を支えてきました。重さをはかる。量をはかる。品質をはかる。それが私たちの原点です。しかし、私たちが本当に大切にしているのは、数字そのものではありません。その先にある、お客様の安心や喜び、そして未来です。……（約800字）<br><br>未来を測り、未来を創る。それが私たち近江度量衡の変わらぬ使命です。</p>
  </div>
</div></section>

<!-- ⑤ サービス拠点 -->
<section class="section" id="servicebase"><div class="container">
  <p class="section-meta">Service Base</p><h2 class="section-title">サービス拠点</h2>
  <div class="basemap" style="margin-top:24px;">
    <div>''' + ph('グローバル拠点マップ（国内6＋海外3）','','aspect-ratio:4/3') + '''</div>
    <div class="base-list">
      <div class="base-item"><span>本社</span>滋賀県（草津）</div>
      <div class="base-item"><span>営業所</span>東京都</div>
      <div class="base-item"><span>営業所</span>北海道</div>
      <div class="base-item"><span>営業所</span>宮城県</div>
      <div class="base-item"><span>営業所</span>新潟県</div>
      <div class="base-item"><span>営業所</span>熊本県</div>
      <div class="base-item base-item--ov"><span>海外</span>上海（中国）</div>
      <div class="base-item base-item--ov"><span>海外</span>バンコク（タイ）</div>
      <div class="base-item base-item--ov"><span>海外</span>韓国</div>
    </div>
  </div>
</div></section>

<!-- ⑥ 会社概要 -->
<section class="section section--grey" id="profile"><div class="container">
  <p class="section-meta">Profile</p><h2 class="section-title">会社概要</h2>
  <table class="info-table" style="margin-top:24px;background:#fff;">
    <tr><th>会社名</th><td>近江度量衡株式会社（OMISCALE CO.,LTD.）</td></tr>
    <tr><th>設立</th><td>1900年（明治33年）</td></tr>
    <tr><th>資本金</th><td>200,000,000円 ''' + todo('現行サイト記載値を確認') + '''</td></tr>
    <tr><th>代表者</th><td>代表取締役社長　小谷 俊彦 ''' + todo('確認') + '''</td></tr>
    <tr><th>従業員数</th><td>約150名 ''' + todo('最新の人数を確認') + '''</td></tr>
    <tr><th>事業内容</th><td>計量システムの設計・制御・製造・販売・保守</td></tr>
    <tr><th>ISO認証</th><td>ISO 9001</td></tr>
    <tr><th>拠点数</th><td>国内6拠点＋海外3拠点</td></tr>
    <tr><th>所在地（本社）</th><td>〒525-0054 滋賀県草津市東矢倉三丁目11番70号</td></tr>
    <tr><th>TEL</th><td>077-562-7111</td></tr>
  </table>
</div></section>
'''
page("company.html","会社案内｜近江度量衡株式会社", company_body, active="company.html",
     crumbs=[("TOP","top.html"),("会社案内",None)])
PAGES.append(("E","会社案内","/company/","company.html","corp",False))

# ======================= F. 126年ヒストリー =======================
# (era導入, [(年号era, 年number, 見出し, 本文, 素材ファイル名 or '')])
HISTORY = [
 ("明治・大正（1900-1925）", "明治33年の草津工房開設から、精度への執念と地域への誠実さが原点。", [
   ("明治33年","1900","創業 ― 草津に計量器工房を開設","初代が滋賀県草津にて計量器製造・販売を開始。農産物取引の公正計量を使命に、棒秤・台秤を供給。","image_1900_1.jpg / image_1900_2.jpg"),
   ("明治43年","1910","法人化 ― 近江度量衡株式会社を設立","事業拡大にともない法人格取得。職人工房から組織経営へ移行、従業員約15名。",""),
   ("大正9年","1920","近畿・東海エリアへ販路拡大","大阪・名古屋の穀物取引所向け高精度台秤を納入。産業発展に合わせ滋賀県外へ展開。",""),
 ]),
 ("昭和前期（1926-1944）", "農業計量で培った精度ノウハウを、工業用計量器へと展開しはじめた時代。", [
   ("昭和5年","1930","二代目に経営承継 ― 製品ラインナップ拡充","台秤に加え吊り秤・分銅・検定器具製造開始。中小工場・卸業者向け基盤を整備。",""),
   ("昭和10年","1935","工業用計量器の試作開始","鉄鋼・繊維産業向け大型計量器（トラックスケール前身）試作開始。農業計量の精度ノウハウの産業転用を開始。",""),
 ]),
 ("昭和中期（1945-1969）", "計量法制定と高度経済成長。選果機・計量ライン事業へ参入し全国展開の布石を打つ。", [
   ("昭和25年","1950","計量法制定 ― 国家検定対応機器の製造を開始","計量法施行で国家検定基準適合が必須化。検定合格基準をいち早く確立し、業界標準設定に関与。","image_1946.jpg"),
   ("昭和30年","1955","選果機・計量コンベア事業参入","高度経済成長期の農業機械化需要を捉え、選果・計量ラインシステムを開発。農協大型施設への初納入実現。","image_1959.jpg"),
   ("昭和35年","1960","東京・大阪に営業所開設","首都圏・関西圏の大型農産物市場・食品加工業者へアクセス強化。全国展開の布石。","image_1961_1.jpg"),
 ]),
 ("昭和後期（1970-1988）", "穀類カントリーエレベーター向けで業界トップシェアへ。マイコン制御の次世代機も製品化。", [
   ("昭和50年","1975","穀類カントリーエレベーター向け計量システムを本格展開","食糧庁管轄穀物備蓄施設へのシステム納入本格化。累計100施設突破。業界シェアトップクラスを確立。","image_1974.jpg"),
   ("昭和55年","1980","マイコン制御計量システムの製品化","マイクロプロセッサ搭載計量制御システムを開発・製品化。自動計量・データ記録・印字一体化した次世代機を普及。","image_1980.jpg"),
   ("昭和62年","1987","北海道・九州に営業所を開設","北海道（帯広）・九州（福岡）に営業所開設。産地密着サービス体制を全国展開。",""),
 ]),
 ("平成（1989-2018）", "創業100周年とISO取得。累計1,000施設突破からアジア展開へ。", [
   ("平成12年","2000","創業100周年 ― ISO 9001 認証取得","品質保証体制を国際規格で整備。全数検査・精度管理の仕組みを標準化。「検定合格率100%」誓約。","image_2000_1.jpg / image_2000_2.jpg"),
   ("平成19年","2007","カントリーエレベーター累計1,000施設突破","全国CEへのシステム納入が累計1,000施設突破。国内穀類計量分野でのトップシェア確立。","image_2007.jpg"),
   ("平成22年","2010","アジア展開開始 ― 上海拠点設立","中国・アジアの農産物産業急成長とともに海外進出。上海に現地法人設立。",""),
   ("平成27年","2015","タイ・バンコクに拠点設立 ― 海外3拠点体制が完成","上海・ソウル・バンコク3拠点体制でアジア全域をカバー。","image_2015.jpg"),
 ]),
 ("令和（2019-現在）", "リモート保守体制の整備、累計2,000施設突破、そして新ブランドビジョンへ。", [
   ("令和2年","2020","コロナ禍でのリモートメンテナンス体制を整備","遠隔診断・オンラインサポートシステムを急速整備。「動かし続ける」メンテナンスへの信頼を向上。",""),
   ("令和5年","2023","累計納入施設2,000突破","国内外合計納入施設数が2,000施設を突破。農産物・穀類・工業三分野での実績が積み重なった節目。","image_2024.jpg"),
   ("令和7年","2025","創業126周年 ― 北海道営業所を拡充移転","3月に創業126周年達成。6月には北海道営業所を拡充移転。Webリニューアルプロジェクト始動。",""),
   ("令和8年","2026","新ブランドビジョンを発表 ― Webサイトリニューアル","「いきる」をはかり、豊かな世界へ。新ブランドステートメントのもとWebサイトをリニューアル。次の100年に向けた採用・広報体制を強化。",""),
 ]),
]
def history_eras():
    out = ""
    for era, intro, rows in HISTORY:
        items = ""
        for e,n,h,b,asset in rows:
            assethtml = ph('当時の写真：'+asset,'timeline-ph') if asset else ''
            items += f'''<div class="timeline-item"><div class="timeline-year"><span class="timeline-year__era">{e}</span><span class="timeline-year__num">{n}</span></div><div class="timeline-dot"></div><div class="timeline-content"><h3>{h}</h3><p>{b}</p></div>{assethtml}</div>'''
        out += f'''<div style="margin-top:48px;"><p class="eyebrow">{era}</p><p class="section-lead" style="margin-top:0;margin-bottom:16px;">{intro}</p><div class="timeline">{items}</div></div>'''
    return out

history_body = '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">126 YEARS HISTORY</p>
  <h1 class="page-header__title">明治から令和へ。</h1>
  <p class="page-header__lead">1900年創業から126年の歩みと、2,000施設以上への納入実績。</p>
</div></header>
<section class="section"><div class="container">
  <div class="numbers-grid" style="grid-template-columns:repeat(4,1fr);">
    <div class="number-card"><div class="number-card__num">126<span class="number-card__unit">年</span></div><div class="number-card__label">創業からの歴史（1900〜2026）</div></div>
    <div class="number-card"><div class="number-card__num">2,000<span class="number-card__unit">+</span></div><div class="number-card__label">累計納入施設数</div></div>
    <div class="number-card"><div class="number-card__num">9<span class="number-card__unit">拠点</span></div><div class="number-card__label">国内6＋海外3 サービス網</div></div>
    <div class="number-card"><div class="number-card__num">3<span class="number-card__unit">カ国</span></div><div class="number-card__label">海外展開（上海・バンコク・韓国）</div></div>
  </div>
  ''' + history_eras() + '''
  <!-- 証言ブロック -->
  <div class="grid-2" style="margin-top:56px;">
    <div class="value-item" style="background:var(--c-bg-light);"><p style="font-size:16px;font-weight:700;line-height:1.8;">「計量とは、人と人の信頼を結ぶ仕事だ。一グラムのずれも、嘘をつく。」</p><p style="font-size:12px;color:#888;margin-top:12px;">元社員・昭和40年代入社 ''' + todo('本番用原稿に差し替え') + '''</p></div>
    <div class="value-item" style="background:var(--c-bg-light);"><p style="font-size:16px;font-weight:700;line-height:1.8;">「一品一様というのは、ただ特注を作るということではない。お客様の現場を理解し、最適な精度で答えることだ。」</p><p style="font-size:12px;color:#888;margin-top:12px;">現役エンジニア ''' + todo('本番用原稿に差し替え') + '''</p></div>
  </div>
</div></section>
<div class="recruit-banner"><div class="recruit-banner__inner">
  <div class="recruit-banner__text"><h2>次の100年へ。ともに歩む人を募集中。</h2><p>126年の技術と誇りを受け継ぎ、更なる進化を担う仲間を求めています。</p></div>
  <div class="recruit-banner__cta"><a class="btn btn--red" href="recruit.html" style="background:#111315;color:#fff;">採用情報 ↗</a></div>
</div></div>
'''
page("history.html","126年ヒストリー｜近江度量衡株式会社", history_body, active="history.html",
     crumbs=[("TOP","top.html"),("126年ヒストリー",None)])
PAGES.append(("F","126年ヒストリー","/history/","history.html","corp",False))

# ======================= I. 新着情報 =======================
def news_list(cats, rows, detail="news-detail.html"):
    fil = "".join(f'<a class="page-nav-cat" style="padding:8px 16px;border:1px solid var(--c-border);font-size:12px;margin-right:8px;display:inline-block;">{c}</a>' for c in cats)
    items = ""
    for d,c,t in rows:
        items += f'<li class="news-item"><span class="news-item__date">{d}</span><span class="news-item__cat">{c}</span><a class="news-item__title" href="{detail}">{t}</a></li>'
    return fil, items

news_body_top = '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">NEWS</p>
  <h1 class="page-header__title">新着情報</h1>
  <p class="page-header__lead">近江度量衡の最新ニュース・お知らせ・プレスリリース</p>
</div></header>
<section class="section"><div class="container">'''
fil, items = news_list(["すべて","お知らせ","製品情報","採用","プレスリリース"],
  [("2025.06.01","お知らせ","北海道営業所を開設しました"),
   ("2025.03.01","お知らせ","会社設立126周年を達成しました"),
   ("2025.04.01","採用","2027年度採用エントリー受付開始のご案内")])
news_body = news_body_top + '<div style="margin-bottom:24px;">' + fil + '</div><ul class="news-list">' + items + '''</ul>
  <div class="cms-note">◯ 日刊工業新聞等メディア掲載・プレスリリースを中心に更新（月1〜2回／随時）。WordPress管理画面から投稿。''' + cms('CMS更新') + '''</div>
</div></section>'''
page("news.html","新着情報｜近江度量衡株式会社", news_body, active="news.html",
     crumbs=[("TOP","top.html"),("新着情報",None)])
PAGES.append(("I","新着情報","/news/","news.html","corp",True))

# I1 記事詳細
news_detail_body = '''
<section class="section"><div class="container" style="max-width:760px;">
  <p style="font-size:12px;color:#888;letter-spacing:.06em;">2025.06.01　<span style="border:1px solid var(--c-border);padding:1px 8px;">お知らせ</span></p>
  <h1 style="font-size:30px;font-weight:700;line-height:1.5;margin:16px 0 8px;">北海道営業所を開設しました ''' + cms('CMS更新') + '''</h1>
  <div style="margin:24px 0;">''' + ph('記事メイン画像（任意）','','aspect-ratio:16/9') + '''</div>
  <p style="font-size:15px;line-height:2;color:#333;">〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇''' + todo('記事ごとに入力') + '''</p>
  <p style="font-size:15px;line-height:2;color:#333;margin-top:16px;">〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇</p>
</div></section>
<section class="section section--grey"><div class="container">
  <h2 class="section-title" style="font-size:20px;">関連記事</h2>
  <ul class="news-list" style="margin-top:16px;">
    <li class="news-item"><span class="news-item__date">2025.03.01</span><a class="news-item__title" href="news-detail.html">会社設立126周年を達成しました</a></li>
    <li class="news-item"><span class="news-item__date">2025.04.01</span><a class="news-item__title" href="news-detail.html">2027年度採用エントリー受付開始のご案内</a></li>
  </ul>
  <a class="btn btn--outline btn--sm" href="news.html" style="margin-top:24px;">一覧へ戻る</a>
</div></section>
'''
page("news-detail.html","記事タイトル｜新着情報｜近江度量衡株式会社", news_detail_body, active="news.html",
     crumbs=[("TOP","top.html"),("新着情報","news.html"),("記事詳細",None)])
PAGES.append(("I1","記事詳細","/news/[slug]/","news-detail.html","corp",True))

# ======================= J. お問い合わせ =======================
contact_body = '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">CONTACT</p>
  <h1 class="page-header__title">お問い合わせ</h1>
  <p class="page-header__lead">製品・サービス・採用に関するご相談・お問い合わせはこちらから。</p>
</div></header>
<section class="section"><div class="container grid-2" style="gap:48px;align-items:start;">
  <div>
    <div style="display:flex;gap:0;margin-bottom:24px;flex-wrap:wrap;">
      <span class="page-nav" style="display:inline-block;"></span>
      <a class="btn btn--dark btn--sm" style="border-radius:0;">製品・技術について</a>
      <a class="btn btn--outline btn--sm" style="border-radius:0;">サービス・保守</a>
      <a class="btn btn--outline btn--sm" style="border-radius:0;">採用について</a>
      <a class="btn btn--outline btn--sm" style="border-radius:0;">その他</a>
    </div>
    <div class="form-group"><label class="form-label">会社名</label><input class="form-input" placeholder="（任意）"></div>
    <div class="form-group"><label class="form-label">お名前<span class="req">必須</span></label><input class="form-input"></div>
    <div class="form-group"><label class="form-label">部署・役職</label><input class="form-input" placeholder="（任意）"></div>
    <div class="form-group"><label class="form-label">メールアドレス<span class="req">必須</span></label><input class="form-input"></div>
    <div class="form-group"><label class="form-label">電話番号</label><input class="form-input" placeholder="（任意）"></div>
    <div class="form-group"><label class="form-label">お問い合わせ内容<span class="req">必須</span></label><textarea class="form-textarea"></textarea></div>
    <div class="form-group"><label style="font-size:13px;"><input type="checkbox"> <a href="privacy.html" style="border-bottom:1px solid #333;">プライバシーポリシー</a>に同意する</label></div>
    <a class="btn btn--dark" style="width:100%;text-align:center;">送信する</a>
    <p style="font-size:12px;color:#888;margin-top:12px;">送信後に自動返信メールをお送りします。</p>
  </div>
  <div>
    <div style="border:1px solid var(--c-border);padding:28px;">
      <h3 style="font-size:16px;font-weight:700;margin-bottom:16px;">本社</h3>
      <p style="font-size:13px;line-height:2;color:#444;">〒525-0054<br>滋賀県草津市東矢倉三丁目11番70号<br>TEL 077-562-7111<br>受付時間：平日 9:00〜17:00</p>
      <p style="font-size:12px;color:#888;margin-top:16px;line-height:1.8;">東京・大阪・名古屋など、全国の拠点が対応します。最寄りの拠点へ直接お問い合わせも可能です。</p>
    </div>
  </div>
</div></section>
'''
page("contact.html","お問い合わせ｜近江度量衡株式会社", contact_body, active="",
     crumbs=[("TOP","top.html"),("お問い合わせ",None)])
PAGES.append(("J","お問い合わせ","/contact/","contact.html","corp",False))

# ======================= K. プライバシーポリシー =======================
privacy_items = [
 ("個人情報の取得","個人情報を適法かつ公正な手段によって取得します。"),
 ("利用目的","お問い合わせへの対応・採用選考・製品・サービスのご案内のために利用します。"),
 ("第三者提供","法令に基づく場合を除き、ご本人の同意なく第三者に個人情報を提供しません。"),
 ("個人情報の管理","個人情報の漏洩・滅失・毀損の防止のため、適切なセキュリティ対策を講じます。"),
 ("開示・訂正・削除","ご本人から個人情報の開示・訂正・削除のご要請があった場合、合理的な範囲で対応します。"),
]
priv = "".join(f'<div style="margin-top:32px;"><h2 style="font-size:18px;font-weight:700;border-left:3px solid var(--c-omi-red);padding-left:12px;">{i+1}. {t}</h2><p style="font-size:14px;color:#444;line-height:2;margin-top:12px;">{b}</p></div>' for i,(t,b) in enumerate(privacy_items))
privacy_body = '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">PRIVACY POLICY</p>
  <h1 class="page-header__title">プライバシーポリシー</h1>
</div></header>
<section class="section"><div class="container" style="max-width:800px;">''' + priv + '''
  <div style="margin-top:32px;"><h2 style="font-size:18px;font-weight:700;border-left:3px solid var(--c-omi-red);padding-left:12px;">6. お問い合わせ窓口</h2>
    <p style="font-size:14px;color:#444;line-height:2;margin-top:12px;">近江度量衡株式会社 個人情報管理責任者<br>〒525-0054 滋賀県草津市東矢倉三丁目11番70号<br>Mail：info@omiscale.co.jp ''' + todo('メールアドレスを確認') + '''</p></div>
  <p style="font-size:12px;color:#888;margin-top:32px;">本ポリシーは〇〇年〇〇月〇〇日に制定し、必要に応じて改定します。''' + todo('制定日を記入') + '''</p>
</div></section>
'''
page("privacy.html","プライバシーポリシー｜近江度量衡株式会社", privacy_body, active="",
     crumbs=[("TOP","top.html"),("プライバシーポリシー",None)])
PAGES.append(("K","プライバシーポリシー","/privacy/","privacy.html","corp",False))

# ======================= G. 採用TOP =======================
recruit_body = '''
<section class="fv">
  <div class="fv__bg">''' + ph('採用キービジュアル（現場・社員）','','height:100%') + '''</div>
  <div class="fv__content">
    <p class="fv__eyebrow">OMISCALE RECRUIT 2027</p>
    <h1 class="fv__title"><span>「いきる」の単位とは、</span><span>なんだろう。</span></h1>
    <p class="fv__sub">「働く人を大切にする」という理念のもと、あなたの確かな仕事で、豊かな未来を担う力になる。</p>
    <div class="fv__cta"><a class="btn btn--red" href="recruit-jobs.html" style="background:#111315;color:#fff;">募集要項を見る</a><a class="btn btn--white" href="recruit-interview.html">社員インタビュー</a></div>
  </div>
</section>
<nav class="page-nav"><div class="inner">
  <a href="#vision">ビジョン</a><a href="#numbers">数字で見る</a><a href="recruit-interview.html">社員インタビュー</a><a href="#welfare">福利厚生</a><a href="#career">キャリアパス</a><a href="recruit-jobs.html">募集要項</a>
</div></nav>

<!-- ② VISION -->
<section class="section" id="vision"><div class="container statement">
  <p class="statement__en">VISION &amp; VALUES</p>
  <h2 class="statement__main">「いきる」をはかり、豊かな世界へ。</h2>
  <p class="statement__body">「技術」と「誇り」を礎に、日本から世界へ、計量という仕事で社会を豊かにし続けること。それが、近江度量衡の使命です。採用においても「働く人を大切にする」という理念を核に、長く誇りを持って働ける環境を目指しています。</p>
  <div class="grid-3" style="margin-top:40px;">
    <div class="pillar"><div class="pillar__title">技術</div></div>
    <div class="pillar"><div class="pillar__title">誇り</div></div>
    <div class="pillar"><div class="pillar__title">グローバル</div></div>
  </div>
  <p style="font-size:13px;margin-top:24px;"><a href="history.html" style="border-bottom:1px solid #999;">126年ヒストリーを見る →</a></p>
</div></section>

<!-- ③ NUMBERS -->
<section class="section section--dark" id="numbers"><div class="container">
  <p class="statement__en" style="text-align:center;">数字で見る近江度量衡</p>
  <div class="numbers-grid numbers-grid--dark" style="grid-template-columns:repeat(4,1fr);margin-top:24px;">
    <div class="number-card"><div class="number-card__num">126<span class="number-card__unit">年</span></div><div class="number-card__label">創業からの歴史</div></div>
    <div class="number-card"><div class="number-card__num">約150<span class="number-card__unit">名</span></div><div class="number-card__label">従業員数 ''' + todo('要確認') + '''</div></div>
    <div class="number-card"><div class="number-card__num">2,000<span class="number-card__unit">+</span></div><div class="number-card__label">累計納入施設数</div></div>
    <div class="number-card"><div class="number-card__num">9<span class="number-card__unit">拠点</span></div><div class="number-card__label">国内6＋海外3</div></div>
    <div class="number-card"><div class="number-card__num">〇〇<span class="number-card__unit">%</span></div><div class="number-card__label">新卒3年定着率 ''' + todo('数値提供待ち') + '''</div></div>
    <div class="number-card"><div class="number-card__num">〇〇<span class="number-card__unit">歳</span></div><div class="number-card__label">平均年齢 ''' + todo('数値提供待ち') + '''</div></div>
    <div class="number-card"><div class="number-card__num">ISO<span class="number-card__unit">9001</span></div><div class="number-card__label">品質認証取得</div></div>
    <div class="number-card"><div class="number-card__num">3<span class="number-card__unit">カ国</span></div><div class="number-card__label">海外展開</div></div>
  </div>
</div></section>

<!-- ④ PEOPLE -->
<section class="section"><div class="container">
  <p class="section-meta">People</p><h2 class="section-title">技術と誇りを持って働く、近江の現場のことば。</h2>
  <p class="section-lead">現場・設計・営業——それぞれの視点で語る、近江度量衡の仕事。''' + todo('実在社員に差し替え') + '''</p>
  <div class="grid-3" style="margin-top:32px;">
    <a class="interview-card" href="recruit-interview-detail.html"><div class="interview-card__img">''' + ph('社員写真') + '''</div><div class="interview-card__body"><div class="interview-card__dept">製造部 / 入社〇年目（20代）</div><div class="interview-card__name">山田 〇〇</div><p class="interview-card__quote">毎回違う課題に向き合うから、技術者として本当に成長できる。</p></div></a>
    <a class="interview-card" href="recruit-interview-detail.html"><div class="interview-card__img">''' + ph('社員写真') + '''</div><div class="interview-card__body"><div class="interview-card__dept">設計部 / 入社〇年目（30代）</div><div class="interview-card__name">鈴木 〇〇</div><p class="interview-card__quote">図面通りにつくるのではなく、現場に合わせてつくる。</p></div></a>
    <a class="interview-card" href="recruit-interview-detail.html"><div class="interview-card__img">''' + ph('社員写真') + '''</div><div class="interview-card__body"><div class="interview-card__dept">営業部 / 入社〇年目（30代）</div><div class="interview-card__name">田中 〇〇</div><p class="interview-card__quote">お客様の現場を見て、何が必要か考える。</p></div></a>
  </div>
  <a class="btn btn--outline btn--sm" href="recruit-interview.html" style="margin-top:24px;">インタビュー一覧へ</a>
</div></section>

<!-- ⑤ WELFARE -->
<section class="section section--grey" id="welfare"><div class="container">
  <p class="section-meta">Welfare</p><h2 class="section-title">福利厚生・職場環境</h2>
  <p class="section-lead">「働く人を大切にする」という理念を体現する制度・環境を整えています。</p>
  <div class="grid-3" style="margin-top:24px;">
    <div class="value-item" style="background:#fff;"><div class="value-item__title" style="font-size:15px;">各種社会保険完備</div></div>
    <div class="value-item" style="background:#fff;"><div class="value-item__title" style="font-size:15px;">有給休暇・育児休暇</div></div>
    <div class="value-item" style="background:#fff;"><div class="value-item__title" style="font-size:15px;">住宅手当・通勤手当</div></div>
    <div class="value-item" style="background:#fff;"><div class="value-item__title" style="font-size:15px;">研修制度</div></div>
    <div class="value-item" style="background:#fff;"><div class="value-item__title" style="font-size:15px;">フレックス・リモート対応 ''' + todo('実施状況を確認') + '''</div></div>
    <div class="value-item" style="background:#fff;"><div class="value-item__title" style="font-size:15px;">社内施設・福利厚生</div></div>
  </div>
</div></section>

<!-- ⑥ CAREER PATH -->
<section class="section" id="career"><div class="container">
  <p class="section-meta">Career Path</p><h2 class="section-title">研修・キャリアパス</h2>
  <p class="section-lead">入社後の育成プログラム・OJT・キャリアパス事例を紹介。技術者として誇りを持って成長できる環境を、具体的なロードマップで。</p>
  <div class="process" style="margin-top:32px;">
    <div class="process-step"><div class="process-step__num">STEP 01</div><div class="process-step__title">入社〜3ヶ月</div><div class="process-step__desc">入社時研修・OJT開始</div></div>
    <div class="process-step"><div class="process-step__num">STEP 02</div><div class="process-step__title">〜1年</div><div class="process-step__desc">OJT・現場実務</div></div>
    <div class="process-step"><div class="process-step__num">STEP 03</div><div class="process-step__title">〜3年</div><div class="process-step__desc">独立担当・専門性強化</div></div>
    <div class="process-step"><div class="process-step__num">STEP 04</div><div class="process-step__title">5年〜</div><div class="process-step__desc">リーダー・専門職</div></div>
  </div>
  <div class="grid-3" style="margin-top:24px;">
    <div class="use-item">技術スペシャリスト</div><div class="use-item">プロジェクトマネジャー</div><div class="use-item">海外担当</div>
  </div>
</div></section>

<!-- ⑦ ENTRY -->
<section class="section section--dark theme-recruit" id="entry" style="background:#1a0d0d;"><div class="container">
  <div class="statement"><h2 class="statement__main" style="color:#fff;">あなたの「測る」を見つけてください。</h2>
  <p class="statement__body" style="color:#cbb;">新卒・中途、いずれも募集中です。126年の技術と誇りを、次の世代へ。</p></div>
  <div class="entry-split" style="margin-top:40px;">
    <div class="entry-card"><div class="entry-card__label">NEW GRADUATE 新卒採用</div><div class="entry-card__copy">「未来を測る第一歩を、ここから。」</div><a class="btn btn--white" href="recruit-jobs-graduate.html">新卒採用</a></div>
    <div class="entry-card"><div class="entry-card__label">MID-CAREER 中途採用</div><div class="entry-card__copy">「培った経験を、126年の精度に加えてください。」</div><a class="btn btn--white" href="recruit-jobs-career.html">中途採用</a></div>
  </div>
</div></section>
'''
page("recruit.html","採用情報｜近江度量衡 ― 「いきる」の単位とは、なんだろう。", recruit_body,
     active="recruit.html", recruit=True, crumbs=None)
PAGES.append(("G","採用TOP","/recruit/","recruit.html","recruit",False))

RC = [("TOP","top.html"),("採用情報","recruit.html")]

# ======================= G3. 社員インタビュー一覧 =======================
INTERVIEWEES = [
 ("製造部 / 入社〇年目（20代）","山田 〇〇","毎回違う課題に向き合うから、技術者として本当に成長できる。誇りを持てる仕事です。"),
 ("設計部 / 入社〇年目（30代）","鈴木 〇〇","図面通りにつくるのではなく、現場に合わせてつくる。グローバルな現場を支える実感があります。"),
 ("営業部 / 入社〇年目（30代）","田中 〇〇","お客様の現場を見て、何が必要か考える。"),
 ("技術開発部 / 入社〇年目（20代）","佐藤 〇〇","入社後、こんなに任せてもらえると思っていなかった。"),
 ("サービス部 / 入社〇年目（40代）","伊藤 〇〇","全国の現場を飛び回って、お客様に「ありがとう」と言われる瞬間が好き。"),
]
cards = "".join(f'<a class="interview-card" href="recruit-interview-detail.html"><div class="interview-card__img">'+ph('社員写真')+f'</div><div class="interview-card__body"><div class="interview-card__dept">{d}</div><div class="interview-card__name">{n}</div><p class="interview-card__quote">{q}</p><span class="interview-card__link">インタビューを読む →</span></div></a>' for d,n,q in INTERVIEWEES)
interview_body = '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">PEOPLE</p>
  <h1 class="page-header__title">社員インタビュー</h1>
  <p class="page-header__lead">現場・設計・営業——それぞれの視点で語る、近江度量衡の仕事。</p>
</div></header>
<section class="section"><div class="container">
  <div class="grid-3">''' + cards + '''</div>
  <div class="cms-note">◯ 職種別3〜5名からスタートし段階的に増加。戦略的PR対象者（育休取得男性・働くお母さん等）も配置。インタビュー詳細は投稿テンプレートで自社更新（AI活用で持続可能な更新方式を検討）。''' + cms('CMS更新') + todo('実在社員・写真を提供') + '''</div>
</div></section>
'''
page("recruit-interview.html","社員インタビュー｜近江度量衡 採用", interview_body,
     active="recruit-interview.html", recruit=True, crumbs=RC+[("社員インタビュー",None)])
PAGES.append(("G3","社員インタビュー","/recruit/interview/","recruit-interview.html","recruit",True))

# G3-1 インタビュー詳細
QA = [
 ("近江度量衡を選んだ理由を教えてください。","〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇"),
 ("現在担当している業務内容を教えてください。","〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇"),
 ("仕事のやりがい・難しさを教えてください。","〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇"),
 ("今後の目標・キャリアの展望を教えてください。","〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇"),
 ("就活生・転職希望者へのメッセージをお願いします。","〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇"),
]
qahtml = "".join(f'<div class="qa"><div class="qa__q">{q}</div><div class="qa__a">{a}</div></div>' for q,a in QA)
interview_detail_body = '''
<section class="fv" style="min-height:420px;"><div class="fv__bg">''' + ph('社員メイン写真（現場）','','height:100%') + '''</div>
  <div class="fv__content"><p class="fv__eyebrow">PEOPLE — 製造部 / 入社〇年目（20代）''' + todo('社員ごとに入力') + '''</p>
  <h1 class="fv__title" style="font-size:32px;">「（その社員の引用文）」</h1>
  <p class="fv__sub">山田 〇〇</p></div>
</section>
<section class="section"><div class="container" style="max-width:820px;">
  <table class="info-table" style="margin-bottom:40px;">
    <tr><th>出身・学歴</th><td>〇〇大学 〇〇学部 卒業</td></tr>
    <tr><th>入社年</th><td>〇〇〇〇年入社</td></tr>
    <tr><th>現在の担当業務</th><td>〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇</td></tr>
  </table>''' + qahtml + '''
  <a class="btn btn--outline btn--sm" href="recruit-interview.html" style="margin-top:32px;">インタビュー一覧へ戻る</a>
</div></section>
'''
page("recruit-interview-detail.html","社員インタビュー 詳細｜近江度量衡 採用", interview_detail_body,
     active="recruit-interview.html", recruit=True, crumbs=RC+[("社員インタビュー","recruit-interview.html"),("詳細",None)])
PAGES.append(("G3-1","インタビュー詳細","/recruit/interview/[slug]/","recruit-interview-detail.html","recruit",True))

# ======================= G8. 採用ニュース =======================
fil, items = news_list(["すべて","説明会","インターン","中途募集","お知らせ"],
  [("2026.04.10","説明会","2027年度新卒向け合同会社説明会のご案内（5月開催）"),
   ("2026.04.01","中途募集","機械設計エンジニア・営業職の中途採用募集を開始しました"),
   ("2026.03.01","お知らせ","2027年度新卒エントリー受付を開始しました"),
   ("2026.02.10","インターン","京都大学工学部との連携インターンシップ参加者募集"),
   ("2025.10.15","インターン","冬季インターンシップ参加者募集")], detail="recruit-news.html")
recruit_news_body = '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">RECRUIT NEWS</p>
  <h1 class="page-header__title">採用ニュース</h1>
  <p class="page-header__lead">セミナー・説明会の開催情報、中途採用の募集情報など、採用に関するお知らせをタイムリーに発信します。</p>
</div></header>
<section class="section"><div class="container">
  <div style="margin-bottom:24px;">''' + fil + '''</div>
  <ul class="news-list">''' + items + '''</ul>
  <div class="cms-note">◯ コーポレートの新着情報（/news/）とは独立して運用。カスタム投稿でタイムリーに発信。''' + cms('CMS更新') + '''</div>
</div></section>
'''
page("recruit-news.html","採用ニュース｜近江度量衡 採用", recruit_news_body,
     active="recruit-news.html", recruit=True, crumbs=RC+[("採用ニュース",None)])
PAGES.append(("G8","採用ニュース","/recruit/news/","recruit-news.html","recruit",True))

# ======================= G6. 募集要項 =======================
jobs_body = '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">JOBS</p>
  <h1 class="page-header__title">募集要項</h1>
  <p class="page-header__lead">新卒・中途、いずれも積極採用中です。</p>
</div></header>
<section class="section"><div class="container grid-2">
  <a class="entry-card" href="recruit-jobs-graduate.html"><div class="entry-card__label">NEW GRADUATE 新卒採用</div><div class="entry-card__copy">「未来を測る第一歩を、ここから。」</div><p class="entry-card__desc">理系・工学系だけじゃない。ものをつくる誠実さに共感できる人を求めています。</p><span class="btn btn--white">新卒採用 募集要項 →</span></a>
  <a class="entry-card" href="recruit-jobs-career.html"><div class="entry-card__label">MID-CAREER 中途採用</div><div class="entry-card__copy">「培った経験を、126年の精度に加えてください。」</div><p class="entry-card__desc">年齢・業界不問。あなたの経験が次の100年の基盤になる。</p><span class="btn btn--white">中途採用 募集要項 →</span></a>
</div></section>
<div class="cms-note" style="max-width:1100px;margin:0 auto 56px;">◯ 募集要項はカスタム投稿で管理。選考フロー・FAQ・就活サイトリンクを設置。''' + cms('CMS更新') + todo('就活サイト連携要確認') + '''</div>
'''
page("recruit-jobs.html","募集要項｜近江度量衡 採用", jobs_body,
     active="recruit-jobs.html", recruit=True, crumbs=RC+[("募集要項",None)])
PAGES.append(("G6","募集要項","/recruit/jobs/","recruit-jobs.html","recruit",True))

# 募集要項詳細テンプレ
def job_detail(copy, desc, rows, flow):
    tr = "".join(f'<tr><th>{k}</th><td>{v}</td></tr>' for k,v in rows)
    steps = "".join(f'<div class="process-step"><div class="process-step__num">STEP 0{i+1}</div><div class="process-step__title">{s}</div></div>' for i,s in enumerate(flow))
    return '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">JOBS</p>
  <h1 class="page-header__title">''' + copy + '''</h1>
  <p class="page-header__lead">''' + desc + '''</p>
</div></header>
<section class="section"><div class="container" style="max-width:860px;">
  <h2 class="section-title" style="font-size:22px;">募集要項</h2>
  <table class="info-table" style="margin-top:20px;">''' + tr + '''</table>
  <h2 class="section-title" style="font-size:22px;margin-top:48px;">選考フロー</h2>
  <div class="process" style="margin-top:20px;">''' + steps + '''</div>
  <div style="margin-top:40px;text-align:center;"><a class="btn btn--red" href="recruit-entry-2027-graduate.html" style="background:#111315;color:#fff;">エントリーする</a></div>
</div></section>
'''
page("recruit-jobs-graduate.html","新卒採用 募集要項｜近江度量衡 採用2027",
  job_detail("未来を測る第一歩を、ここから。","理系・工学系だけじゃない。着実にものをつくる誠実さに共感できる人を求めています。",
   [("募集職種","技術系総合職（設計・製造・保守・営業） "+todo('最新の職種名を確認')),
    ("採用予定人数","〇〇名 "+todo('数値提供待ち')),
    ("応募資格","2027年3月卒業見込みの大学・大学院・短大・専門学校卒業予定の方（学部・学科不問）"),
    ("勤務地","本社（滋賀）および各拠点（転勤あり）"),
    ("給与（大卒）","〇〇万円 "+todo('数値提供待ち')),
    ("給与（院卒）","〇〇万円 "+todo('数値提供待ち')),
    ("諸手当","通勤手当・住宅手当・残業手当 等"),
    ("休日","土日祝・年末年始・有給休暇"),
    ("社会保険","健康保険・厚生年金・雇用保険・労災保険"),
    ("試用期間","3ヶ月（本採用と同条件）")],
   ["エントリー","書類選考","一次面接","適性検査","二次面接","内定"]),
  active="recruit-jobs.html", recruit=True, crumbs=RC+[("募集要項","recruit-jobs.html"),("新卒採用",None)])
PAGES.append(("G6-1","新卒採用","/recruit/jobs/graduate/","recruit-jobs-graduate.html","recruit",True))

page("recruit-jobs-career.html","中途採用 募集要項｜近江度量衡 採用2027",
  job_detail("培った経験を、126年の精度に加えてください。","年齢・業界不問。あなたの経験が、次の100年の基盤になる。",
   [("募集職種","技術系（設計・製造・保守）/ 営業 / 管理部門 "+todo('最新の募集職種を確認')),
    ("応募資格","業界・年齢不問。計量・機械・電気・ITに関連する経験者を歓迎。"),
    ("勤務地","本社（滋賀）または各拠点（相談可）"),
    ("給与","経験・能力を考慮のうえ、当社規定により決定 "+todo('給与レンジを確認')),
    ("諸手当","通勤手当・住宅手当・残業手当 等"),
    ("休日","土日祝・年末年始・有給休暇"),
    ("社会保険","健康保険・厚生年金・雇用保険・労災保険"),
    ("試用期間","3ヶ月（本採用と同条件）")],
   ["応募・書類選考","一次面接","適性検査","二次面接（場合により役員面接）","内定"]),
  active="recruit-jobs.html", recruit=True, crumbs=RC+[("募集要項","recruit-jobs.html"),("中途採用",None)])
PAGES.append(("G6-2","中途採用","/recruit/jobs/career/","recruit-jobs-career.html","recruit",True))

# ======================= G7. エントリーLP =======================
def entry_lp(copy, intro, stats, jobs, jobs_link):
    st = "".join(f'<div class="number-card"><div class="number-card__num">{v}</div><div class="number-card__label">{l}</div></div>' for l,v in stats)
    jr = "".join(f'<tr><th>{k}</th><td>{v}</td></tr>' for k,v in jobs)
    return '''
<section class="fv"><div class="fv__bg">''' + ph('エントリーLP キービジュアル','','height:100%') + '''</div>
  <div class="fv__content"><p class="fv__eyebrow">OMISCALE RECRUIT 2027</p>
  <h1 class="fv__title" style="font-size:40px;">''' + copy + '''</h1>
  <p class="fv__sub">''' + intro + '''</p>
  <div class="fv__cta"><a class="btn btn--red" href="#entry" style="background:#111315;color:#fff;">エントリーする</a></div></div>
</section>
<section class="section"><div class="container">
  <p class="section-meta">About</p><h2 class="section-title">近江度量衡とは</h2>
  <p class="section-lead">創業1900年。農産物・穀類・工業製品向けの計量システムを一品一様で設計・製造。</p>
  <div class="numbers-grid numbers-grid--dark" style="grid-template-columns:repeat(4,1fr);margin-top:24px;">''' + st + '''</div>
</div></section>
<section class="section section--grey"><div class="container" style="max-width:820px;">
  <h2 class="section-title" style="font-size:22px;">募集要項（抜粋）</h2>
  <table class="info-table" style="margin-top:20px;background:#fff;">''' + jr + '''</table>
  <p style="font-size:13px;margin-top:16px;"><a href="''' + jobs_link + '''" style="border-bottom:1px solid #999;">詳しい募集要項を見る →</a></p>
</div></section>
<section class="section section--dark theme-recruit" id="entry" style="background:#1a0d0d;"><div class="container statement">
  <h2 class="statement__main" style="color:#fff;">''' + copy + '''</h2>
  <p class="statement__body" style="color:#cbb;">エントリーは専用フォームより受け付けています。</p>
  <div style="margin-top:24px;"><a class="btn btn--red" href="contact.html" style="background:#111315;color:#fff;">エントリーフォームへ</a></div>
</div></section>
'''
page("recruit-entry-2027-graduate.html","2027 新卒採用エントリー｜近江度量衡",
  entry_lp("この先を拓く挑戦を一緒に。",
    "農産物・穀類・工業製品の「計量」で社会を支える、近江度量衡。2027年度、新卒採用のエントリーを受け付けています。",
    [("創業","126年"),("納入施設","2,000+"),("国内外","9拠点"),("従業員","約150名")],
    [("募集職種","技術系総合職・営業職 "+todo('確認')),("応募資格","2027年3月卒業見込み（学部・学科不問）"),("給与","経験・能力を考慮の上、優遇します"),("勤務地","本社（滋賀）または各拠点")],
    "recruit-jobs-graduate.html"),
  active="", recruit=True, crumbs=RC+[("2027 新卒エントリー",None)])
PAGES.append(("G7-1","2027年度 新卒エントリーLP","/recruit/entry/2027/graduate/","recruit-entry-2027-graduate.html","recruit",False))

page("recruit-entry-2027-career.html","2027 中途採用エントリー｜近江度量衡",
  entry_lp("培った経験を、精度に。",
    "創業1900年の計量システム企業。農産物・工業製品向けのはかりを設計・製造し、「いきる」をはかり、豊かな世界へというコーポレートスローガンを掲げています。国内外9拠点で従業員約150名が勤務。",
    [("創業から","126年"),("納入実績","2,000+"),("国内外","9拠点"),("従業員","約150名")],
    [("募集職種","技術系総合職・営業職 "+todo('確認')),("応募資格","業界・年齢不問・経験者歓迎"),("給与","経験・能力を考慮した優遇制度あり"),("勤務地","本社（滋賀）または各拠点")],
    "recruit-jobs-career.html"),
  active="", recruit=True, crumbs=RC+[("2027 中途エントリー",None)])
PAGES.append(("G7-2","2027年度 中途エントリーLP","/recruit/entry/2027/career/","recruit-entry-2027-career.html","recruit",False))

# ======================= index（ワイヤー一覧ハブ） =======================
def index_rows(group):
    out = ""
    for no,name,url,fil,grp,is_cms in PAGES:
        if grp != group: continue
        depth = 0
        if "-" in no: depth = 2
        elif len(no) > 1 and no[1:].isdigit(): depth = 1
        pad = ["name-main","name-sub","name-sub3"][min(depth,2)]
        corpcls = (" "+group) if depth==0 else ""
        flag = ' <span style="background:#e8f4ea;color:#2f6b3d;border:1px solid #5a9e6a;font-size:9px;padding:0 5px;border-radius:2px;">CMS</span>' if is_cms else ""
        out += f'<tr><td class="no">{no}</td><td class="{pad}{corpcls}">{name}{flag}</td><td class="url">{url}</td><td><a class="wf-link" href="{fil}">{fil}</a></td></tr>'
    return out

index_html = '''<!DOCTYPE html>
<html lang="ja"><head><script src="_auth.js"></script><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ワイヤーフレーム一覧｜近江度量衡 Webリニューアル（wier）</title>
<style>
  *{box-sizing:border-box;margin:0;padding:0;}
  body{padding:32px 40px;max-width:1040px;margin:0 auto;font-family:'Hiragino Sans','Yu Gothic',sans-serif;color:#222;}
  h1{font-size:16px;font-weight:700;margin-bottom:6px;padding-bottom:12px;border-bottom:2px solid #111;letter-spacing:.04em;}
  .badge{display:inline-block;background:#111315;color:#fff;font-size:10px;padding:1px 8px;letter-spacing:.06em;margin-right:8px;vertical-align:middle;}
  .meta{font-size:12px;color:#666;margin:10px 0 8px;line-height:1.9;}
  .legend{font-size:11px;color:#888;margin-bottom:20px;}
  .legend span{background:#e8f4ea;color:#2f6b3d;border:1px solid #5a9e6a;font-size:9px;padding:0 5px;border-radius:2px;}
  .section-label{font-size:11px;font-weight:700;letter-spacing:.14em;padding:8px 12px;margin:24px 0 8px;}
  .section-label--corp{background:#456489;color:#fff;}
  .section-label--recruit{background:#111315;color:#fff;}
  table{width:100%;border-collapse:collapse;font-size:12px;}
  th{background:#111;color:#fff;padding:7px 12px;text-align:left;font-weight:600;letter-spacing:.04em;white-space:nowrap;}
  td{padding:6px 12px;border-bottom:1px solid #ebebeb;vertical-align:middle;line-height:1.4;}
  tr:hover td{background:#fafafa;}
  td.no{color:#aaa;font-size:11px;width:52px;}
  td.url{font-family:monospace;font-size:11px;color:#777;}
  td.name-main{font-weight:700;font-size:12px;}
  td.name-main.corp{background:#eef3f8;}
  td.name-main.recruit{background:#fdf0f0;}
  td.name-sub{padding-left:22px;color:#444;}
  td.name-sub3{padding-left:40px;color:#666;font-size:11px;}
  a.wf-link{color:#111;text-decoration:underline;font-size:11px;font-family:monospace;}
</style></head>
<body>
<h1><span class="badge">wier</span>近江度量衡 Webリニューアル　ワイヤーフレーム一覧</h1>
<p class="meta">ステートメント：<b>「いきる」をはかり、豊かな世界へ。</b>／採用コピー：<b>「いきる」の単位とは、なんだろう。</b><br>
最新原稿シート（修正案優先）＋サイトマップ ver3（更新性・利便性）を反映して改めて構成。採用（G）は /recruit/ 以下に独立UIで統合。</p>
<p class="legend"><span>CMS</span> ＝ クライアントがWordPress管理画面から更新するページ（投稿・カスタム投稿）。それ以外は固定ページ（更新頻度：低）。</p>

<div class="section-label section-label--corp">▼ CORPORATE SITE　コーポレートサイト</div>
<table><thead><tr><th>No.</th><th>ページ名</th><th>URL</th><th>WFファイル</th></tr></thead><tbody>''' + index_rows("corp") + '''</tbody></table>

<div class="section-label section-label--recruit">▼ RECRUITMENT SITE　採用サイト（同ドメイン / /recruit/ 以下・独立UI）</div>
<table><thead><tr><th>No.</th><th>ページ名</th><th>URL</th><th>WFファイル</th></tr></thead><tbody>''' + index_rows("recruit") + '''</tbody></table>
</body></html>'''
with open(os.path.join(OUT,"index.html"),"w",encoding="utf-8") as f:
    f.write(index_html)
print("TOTAL PAGES:", len(PAGES)+1, "(incl. index)")
