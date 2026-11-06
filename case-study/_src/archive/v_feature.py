"""Version C, Feature Presentation: the case study plays as a screening. Scroll is the projector."""
import content as C
from components import *


def scene(media, subs, length=2, cls='', sid='', label=''):
    """A pinned frame. `subs` are (text, fx) pairs that play as subtitles while the frame holds."""
    lines = ''.join(f'<p data-fx="{fx}">{text}</p>' for text, fx in subs)
    i = f' id="{sid}"' if sid else ''
    tag = f'<span class="slate">{label}</span>' if label else ''
    return f'''<section class="scene {cls}"{i} style="--len:{length}" data-scene>
  <div class="scene__pin">{tag}<div class="scene__frame">{media}</div><div class="subs">{lines}</div></div>
</section>'''


def card(n, title, sub='', sid='', cls=''):
    """A title card: a cut to black."""
    i = f' id="{sid}"' if sid else ''
    s = f'<p class="card__s">{sub}</p>' if sub else ''
    return f'<section class="card {cls}"{i}><p class="card__n">{n}</p><h2 class="card__t chunk">{title}</h2>{s}</section>'


def cold_open():
    m = C.META
    tags = ' · '.join(m['tags'])
    return f'''<section class="open" id="opening" data-scene style="--len:2.2">
  <div class="open__pin">
    <p class="open__by">A case study by {esc(m["author"])}</p>
    <div class="scope">
      <video autoplay muted loop playsinline poster="{ASSETS}/img/still-hero-poster-sm.webp" aria-label="La La Land teaser, muted"><source src="{ASSETS}/video/trailer-loop.mp4" type="video/mp4"></video>
      <h1 class="open__t chunk">{esc(m["title"])}</h1>
    </div>
    <p class="open__s">{esc(m["subtitle"])}</p>
    <p class="open__m">{esc(tags)} <button class="open__a" data-about>About the project +</button></p>
  </div>
</section>'''


def coming_attractions():
    o = C.OPENING
    media = compare("old-first", "final-first", "Original page", "Redesigned page", 50, eager=False)
    return f'''<section class="attr">
  <p class="slate slate--in">Coming attractions</p>
  <div class="attr__f">{media}</div>
  <p class="attr__cap"><a href="#" class="link" {zoom_attrs("old-full", "Original page, full length", True)}>Original, full page</a> <a href="#" class="link" {zoom_attrs("final-full", "Redesigned page, full length", True)}>Redesign, full page</a> <span>Drag to compare, same 1440×900 frame.</span></p>
  <div class="attr__t"><p class="big">{esc(o["headline"])}</p><p class="big big--q">{esc(o["question"])}</p></div>
</section>'''


def reel_1():
    d = C.DISCONNECT
    themes = ''
    for t in d['themes']:
        themes += f'<article class="blurb reveal">{icon(t["icon"], "", "blurb__i")}<h4 class="blurb__t">{esc(t["title"])}</h4><p class="blurb__b">{esc(t["body"])}</p>{evidence(t["evidence"])}</article>'
    films = ''
    for b in d['builders']:
        films += f'<li><a href="{esc(b["url"])}" target="_blank" rel="noopener"><b>{b["year"]}</b><span>{esc(b["name"])}</span></a></li>'
    i1, i2, i3 = d['issues']
    pins = ''.join(f'<div class="fpin fpin--{n}" style="left:{pct(b[0], 1440)};top:{pct(b[1], 900)};width:{pct(b[2], 1440)};height:{pct(b[3], 900)}"></div>' for n, b, _ in FIRST_PINS)
    audit = f'<div class="annot">{img("old-first", "First screen of the original page")}{pins}</div>'
    subs = [(f'<b>{esc(i1["title"])}.</b> {esc(i1["body"])} {esc(i1["detail"])}', '1'),
            (f'<b>{esc(i2["title"])}.</b> {esc(i2["body"])} {esc(i2["detail"])}', '2'),
            (f'<b>{esc(i3["title"])}.</b> {esc(i3["body"])} {esc(i3["detail"])}', '3')]
    return f'''{card("Reel 1", "Is " + rotten_tomatoes_chunk() + " actually broken?", esc(d["lead"]), "disconnect", "card--red")}
<section class="sect" data-theme="dark">
  <p class="slate slate--in">{esc(d["voices_label"])}</p>
  <div class="blurbs">{themes}</div>
  <p class="small sect__n">{esc(d["voices_note"])}</p>
</section>
<section class="quote-cut">{pull_quote()}</section>
<section class="sect">
  <div class="films"><div><p class="slate slate--in">Filmography</p><h3 class="big">{esc(d["builders_label"])}</h3><p class="small" style="margin-top:var(--s3)">{esc(d["builders_note"])}</p></div><ol>{films}</ol></div>
</section>
{scene(audit, subs, 3.2, "scene--audit", label=esc(d["audit_label"]))}
<section class="sect sect--tight"><p class="small sect__n">{esc(d["audit_note"])}</p></section>
<section class="cut"><p class="cut__t">{esc(d["conclusion"])}</p></section>'''


def ticket():
    seg = ''
    for i, s in enumerate(C.REALITY['context']['journey']):
        seg += f'<li class="{"on" if s["on"] else ""}"><span class="tk__a">Admit {i + 1}</span><span class="tk__s chunk">{s["step"]}</span><span class="tk__q">{esc(s["q"])}</span></li>'
    return f'<ol class="ticket">{seg}</ol>'


def reel_2():
    r = C.REALITY
    b, c, t = r['business'], r['context'], r['ratings']
    a, dist = b['paths']
    return f'''<section class="inter" id="reality">
  <p class="card__n">Reel 2</p>
  <h2 class="inter__t chunk">Intermission</h2>
  <p class="inter__s">{esc(r["headline"])}</p>
</section>
<section class="sect" data-theme="dark" style="--bg:var(--tint-deep)">
  <p class="big sect__lead">{esc(r["lead"])}</p>
  <div class="row3"><h3 class="big">{esc(b["title"])}</h3><p>{esc(b["body"])}</p></div>
  <div class="bill2">
    <div class="pane reveal"><span class="slate slate--in">Pre-show</span><h4 class="chunk pane__t">{a["name"]}</h4><p>{esc(a["body"])}</p><div class="pane__m">{img(a["image"], "Advertising in the redesigned page")}</div></div>
    <div class="pane reveal"><span class="slate slate--in">Box office</span><h4 class="chunk pane__t">{dist["name"]}</h4><p>{esc(dist["body"])}</p><div class="pane__m">{img(dist["image"], "Where to Watch in the redesigned page")}</div></div>
  </div>
  <div class="row3"><h3 class="big">{esc(c["title"])}</h3><p>{esc(c["body"])}</p></div>
  {ticket()}
  <div class="row3"><h3 class="big">{esc(t["title"])}</h3><p>{esc(t["body"])}</p></div>
  <div class="double">{meters()}</div>
</section>
<section class="cut"><p class="cut__t">{esc(r["conclusion"])}</p></section>'''


def reel_3():
    a = C.ARCHITECTURE
    rows = ''
    for t in a['tiers']:
        names = ''.join(f'<span>{esc(i)}</span>' for i in t['items'])
        rows += f'<div class="bb bb--{t["id"]} reveal"><p class="bb__r">{t["bill"]}<em>{t["id"]} {esc(t["name"])}</em></p><p class="bb__n">{names}</p></div>'
    return f'''{card("Reel 3", esc(a["headline"]), esc(a["lead"]), "architecture")}
<section class="billing"><p class="slate slate--in">Billing order</p>{rows}</section>
<section class="sect"><div class="chart"><h3 class="label">{esc(a["chart_label"])}</h3>{slope()}<p class="small">{esc(a["chart_note"])}</p></div></section>'''


def take(d, media, n):
    return f'''<article class="take" id="{d["id"]}">
  <header class="take__h"><p class="slate slate--in">Scene {d["n"]}</p><h3 class="take__t">{esc(d["title"])}</h3></header>
  {media}
  {pido(d)}
  <p class="take__s">{esc(d["statement"])}</p>
</article>'''


def reel_4():
    D = C.DECISIONS
    I = D['items']
    m1 = f'<div class="wide">{compare("old-first", "final-first", "Original first screen", "Redesigned first screen", 38, eager=False)}</div><div class="two"><div class="dark-plate">{img("final-scores-crop", "Ratings in the hero")}</div><div class="dark-plate">{img("final-cta-crop", "Actions in the hero")}</div></div>'
    out = ''.join(f'<li>{plate(n, l + " exploration", cap=l)}</li>' for n, l in [('x-critics-cards', 'Cards'), ('x-aud-cards', 'Side by side'), ('x-thecritics', 'Broadsheet'), ('x-news1', 'Pull quote'), ('x-news2', 'Front page'), ('x-news4', 'Wire')])
    m2 = f'<p class="slate slate--in slate--pad">Outtakes</p><ul class="outtakes">{out}</ul><div class="wide">{plate("final-critics", "Final Critics Reviews", cls="plate--tint")}</div><div class="two two--a"><div>{plate("final-audience", "Final Audience Reviews", cls="plate--tint")}</div><div class="voices">{voices(I[1])}</div></div>'
    m3 = f'<div class="two">{plate("drawer-critics", "Expanded Critics Reviews drawer")}{plate("drawer-audience", "Expanded Audience Reviews drawer")}</div><div class="voices voices--2 pad">{voices(I[2])}</div>'
    m4 = f'<div class="wide">{video("clip-watch", "Pressing Rent scrolls to Where to Watch")}</div><div class="wide">{plate("final-where", "Where to Watch row", cls="plate--tint")}</div>'
    takes = ''.join(take(d, m, i) for i, (d, m) in enumerate(zip(I, [m1, m2, m3, m4])))
    return f'''{card("Reel 4", "Four decisions, from problem to outcome.", "", "decisions")}{takes}'''


def reel_5():
    e, m = C.EXPERIENCE, C.META
    subs = [(esc(s['name']), str(s['y'])) for s in e['sections']]
    media = f'<div class="screen"><div class="screen__p">{img("final-full", "The complete redesigned La La Land page")}</div></div>'
    ints = ''.join(f'<figure class="fig">{video(i["video"], i["name"])}<figcaption class="cap"><span><b>{esc(i["name"])}.</b> {esc(i["body"])}</span></figcaption></figure>' for i in e['interactions'])
    details = ''.join(plate(s['image'], s['name'], s['name'], cls='plate--tint') for s in e['sections'] if s['image'] != 'final-where')
    return f'''{card("Reel 5", esc(e["headline"]), esc(e["lead"]), "experience")}
{scene(media, subs, 6, "scene--feature", label="Now showing")}
<section class="sect"><p class="slate slate--in">In detail</p><div class="details">{details}</div></section>
<section class="sect"><p class="slate slate--in">Interactions</p><div class="ints">{ints}</div>
<p class="small sect__n">{esc(e["interactions_note"])} {esc(m["prototype_note"])} <a class="link arrow" href="{m["prototype"]}" target="_blank" rel="noopener">Open the prototype</a></p>
<p class="small sect__n">{esc(m["placeholders"])}</p></section>'''


def credits():
    R, m = C.REFLECTION, C.META
    para = ''.join(f'<p>{esc(p)}</p>' for p in R['closing'])
    blocks = ''
    for c in R['columns']:
        items = ''.join(f'<li>{esc(i)}</li>' for i in c['items'])
        blocks += f'<div class="cr__b"><h3>{esc(c["title"])}</h3><ul>{items}</ul></div>'
    return f'''<section class="credits" id="reflection">
  <div class="credits__bg">{img("still-end-still", "")}</div>
  <div class="credits__roll">
    <p class="card__n">End credits</p>
    <h2 class="credits__t chunk">{esc(R["headline"])}</h2>
    <div class="cr__p">{para}</div>
    {blocks}
    <div class="cr__b cr__names">
      <h3>Written, researched and designed by</h3><p class="cr__name">{esc(m["author"])}</p>
      <h3>Made for</h3><p>{esc(m["context"])}</p>
      <h3>Featuring</h3><p>{esc(m["example"])}, as the example film</p>
      <h3>Released</h3><p>{esc(m["date"])}</p>
    </div>
    <p class="small cr__d">{esc(m["disclaimer"])}</p>
  </div>
</section>'''


def player():
    ticks = ''.join(f'<a href="#{c[2]}" data-tick title="{esc(c[1])}"><span>{esc(c[1])}</span></a>' for c in C.CHAPTERS)
    return f'''<nav class="player" data-nav aria-label="Chapters">
  <span class="player__now">Opening</span>
  <div class="player__tl"><div class="player__fill"></div>{ticks}</div>
  <span class="player__t"><b>0:00</b> / 6:00</span>
</nav>'''


def page():
    return head(f'{C.META["title"]} Feature Presentation', 'feature.css', theme_attr='dark') + f'''
<body class="v-feature">
<main>
{cold_open()}
{coming_attractions()}
{reel_1()}
{reel_2()}
{reel_3()}
{reel_4()}
{reel_5()}
{credits()}
</main>
{player()}
{about_panel()}
<script src="../shared/site.js"></script>
<script src="feature.js"></script>
</body></html>'''
