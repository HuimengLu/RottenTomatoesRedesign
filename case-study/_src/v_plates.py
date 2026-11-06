"""The case study page, from Figma "Case Study" → A · Plates (292:1290)."""
import content as C
from components import *


def nav():
    links = ''.join(f'<a href="#{slug}" data-label="{esc(name, quote=True)}">{esc(name)}</a>' for name, slug in C.NAV)
    return f'''<header class="top wrap">
  <a class="top__me" href="#intro">{esc(C.META["author"])}</a>
  <nav class="top__nav" data-nav aria-label="Chapters">{links}</nav>
</header>'''


def out(key):
    return f'href="{esc(C.LINKS[key], quote=True)}" target="_blank" rel="noopener"'


def button(label, key, primary):
    tone = 'white' if primary else 'dark'
    return (f'<a class="chip{" chip--red" if primary else ""}" {out(key)}>{esc(label)}'
            f'<img src="{ASSETS}/svg/arrow-elbow-right-{tone}.svg" width="22" height="22" alt=""></a>')


def chapter_plate(ch, title, variant, media=''):
    return f'''<div class="plates"><header class="chp chp--{variant}">
  {media}
  <div class="chp__meta"><span>{ch["n"]}</span><span>{esc(ch["label"])}</span></div>
  <h2 class="chp__t chunk">{title}</h2>
</header></div>'''


def photo(name):
    return f'<div class="chp__bg">{img(name)}</div>'


def row(block):
    return f'''<div class="row">
  <h3 class="row__h reveal">{esc(block["title"])}</h3>
  <p class="row__b reveal">{esc(block["body"])}</p>
</div>'''


def intro():
    i = C.INTRO
    buttons = ''.join(button(*b) for b in i['buttons'])
    links = ''.join(f'<a class="link" {out(key)}>{esc(label)}</a>' for label, key in i['caption_links'])
    return f'''<section id="intro">
  <div class="wrap intro">
    <h1 class="intro__t">{esc(C.META["title"])}</h1>
    <div class="intro__row">
      <p class="lead intro__s">{esc(i["body"])}</p>
      <div class="intro__btns">{buttons}</div>
    </div>
  </div>
  <div class="wipe wrap" data-wipe>
    <div class="wipe__pin">
      <figure class="wipe__fig">
        {wipe(i["original"], i["redesign"])}
        <figcaption class="cap cap--end">{links}</figcaption>
      </figure>
    </div>
  </div>
  <div class="grid wrap open-text">
    <div class="open-text__b reveal">
      <p class="pull">{esc(i["statement"])}</p>
      <p class="pull open-q">{esc(i["question"])}</p>
    </div>
  </div>
</section>'''


def quote(q):
    by = (f'<a href="{esc(q["url"], quote=True)}" target="_blank" rel="noopener">{esc(q["by"])}</a>'
          if q['url'] else esc(q['by']))
    return f'''<li class="q">
  <blockquote class="q__b"><span class="q__m" aria-hidden="true">“</span><p>{esc(q["text"])}</p></blockquote>
  <cite class="q__by">{by}</cite>
</li>'''


def research():
    r = C.RESEARCH
    h, c = r['heuristic'], r['community']
    issues = ''.join(f'<div class="issue reveal"><span class="issue__n">{n}</span><p>{esc(t)}</p></div>'
                     for n, t in enumerate(h['issues'], 1))
    crops = ''.join(plate(name, alt) for name, alt in h['images'])
    cards = ''
    for card in c['cards']:
        quotes = ''.join(quote(q) for q in card['quotes'])
        cards += f'<article class="card reveal"><h4 class="card__t">{esc(card["title"])}</h4><ul>{quotes}</ul></article>'
    title = 'Is ' + rotten_tomatoes_chunk() + ' actually broken?'
    return f'''<section id="research">
  {chapter_plate(r, title, "red")}
  <div class="grid wrap sect-lead"><p class="lead reveal">{esc(r["lead"])}</p></div>
  {row(h)}
  <div class="grid wrap pair issues">{issues}</div>
  <div class="grid wrap pair">{crops}</div>
  {row(c)}
  <div class="grid wrap pair cards">{cards}</div>
</section>'''


def limitations():
    l = C.LIMITATIONS
    steps = ''.join(f'<li class="{"on" if s["on"] else ""}"><span class="jr__s">{esc(s["step"])}</span><span class="jr__q">{esc(s["q"])}</span></li>'
                    for s in l['journey'])
    icons = ''.join(icon(n, cls='icons__i') for n in l['icons'])
    return f'''<section id="limitations">
  {chapter_plate(l, esc(l["title"]), "gray")}
  {row(l["decision"])}
  <ol class="wide jr">{steps}</ol>
  {row(l["business"])}
  {row(l["value"])}
  <div class="wide"><div class="icons">{icons}</div></div>
</section>'''


def decision_row(r):
    text = ''.join(f'<p>{esc(t)}</p>' for t in r['text'])
    if r.get('video'):
        media = video_plate(r['video'], r['alt'], 'dec__m')
    else:
        media = plate(r['image'], r['alt'], r['tag'], 'dec__m dec__m--tile' if r.get('tile') else 'dec__m')
    return f'''<div class="dec__row">
  {media}
  <div class="dec__x reveal">{text}</div>
</div>'''


def decisions():
    d = C.DECISIONS
    items = ''
    for it in d['items']:
        rows = ''.join(decision_row(r) for r in it['rows'])
        items += f'''<article class="dec">
  <header class="dec__h"><span class="dec__n">{it["n"]}</span><h3 class="dec__t">{esc(it["title"])}</h3></header>
  {rows}
</article>'''
    return f'''<section id="decisions">
  {chapter_plate(d, esc(d["title"]), "photo", photo(d["image"]))}
  {items}
</section>'''


def reflection():
    r = C.REFLECTION
    text = ''.join(f'<p>{esc(t)}</p>' for t in r['text'])
    return f'''<section id="reflection">
  {chapter_plate(r, esc(r["title"]), "photo chp--faces", photo(r["image"]))}
  <div class="grid wrap closing"><div class="closing__b lead reveal">{text}</div></div>
</section>'''


def footer():
    m = C.META
    return f'''<footer class="foot wrap">
  <p>{esc(m["author"])}<br><span class="small">{esc(m["context"])}</span></p>
  <p class="small foot__d">{esc(m["disclaimer"])}</p>
  <a class="chip" href="#intro">Back to top</a>
</footer>'''


def page():
    return head(C.META['title'], 'plates.css', C.INTRO['body']) + f'''
<body class="v-plates">
{nav()}
<main>
{intro()}
{research()}
{limitations()}
{decisions()}
{reflection()}
</main>
{footer()}
<script src="{versioned("shared/site.js")}"></script>
</body></html>'''
