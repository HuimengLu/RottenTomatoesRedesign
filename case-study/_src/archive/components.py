"""Reusable HTML components shared by the three versions."""
import html
import os
from functools import lru_cache

from PIL import Image

import content as C

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = '../assets'

esc = html.escape


@lru_cache(maxsize=None)
def size(name):
    with Image.open(os.path.join(ROOT, 'assets', 'img', name + '.webp')) as im:
        return im.size


def src(name):
    return f'{ASSETS}/img/{name}.webp'


def img(name, alt='', cls='', eager=False):
    w, h = size(name)
    load = 'eager' if eager else 'lazy'
    c = f' class="{cls}"' if cls else ''
    return f'<img{c} src="{src(name)}" width="{w}" height="{h}" alt="{esc(alt)}" loading="{load}" decoding="async">'


def icon(name, alt='', cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<img{c} src="{ASSETS}/svg/{name}.svg" alt="{esc(alt)}" width="96" height="96">'


def zoom_attrs(name, title, tall=False):
    fit = ' data-fit="tall"' if tall else ''
    return f'data-zoom="{src(name)}" data-title="{esc(title, quote=True)}"{fit} role="button" tabindex="0" aria-label="View larger: {esc(title, quote=True)}"'


def plate(name, alt, tag=None, tag_red=False, cls='', cap=None, zoom=True, tall=False, eager=False, title=None):
    """An image tile. Click opens the lightbox."""
    t = f'<span class="plate__tag{" plate__tag--red" if tag_red else ""}">{esc(tag)}</span>' if tag else ''
    z = (' zoomable', zoom_attrs(name, title or alt, tall)) if zoom else ('', '')
    fig = f'<div class="plate{z[0]} {cls}" {z[1]}>{t}{img(name, alt, eager=eager)}</div>'
    if cap:
        return f'<figure class="fig">{fig}<figcaption class="cap"><span>{cap}</span></figcaption></figure>'
    return fig


def video(name, label, cls=''):
    return (f'<div class="vid {cls}"><video data-inview muted loop playsinline preload="none" '
            f'poster="{ASSETS}/img/poster-{name}.jpg" aria-label="{esc(label, quote=True)}" width="1440" height="900">'
            f'<source src="{ASSETS}/video/{name}.mp4" type="video/mp4"></video></div>')


def compare(before, after, before_alt, after_alt, start=50, eager=True):
    return f'''<div class="cmp" style="--x:{start}%">
  {img(before, before_alt, eager=eager)}
  <div class="cmp__after">{img(after, after_alt, eager=eager)}</div>
  <span class="cmp__tag cmp__tag--a">Original</span><span class="cmp__tag cmp__tag--b">Redesign</span>
  <div class="cmp__bar"><div class="cmp__knob" aria-hidden="true">↔</div></div>
  <input type="range" min="0" max="100" value="{start}" aria-label="Drag to compare the original page and the redesign">
</div>'''


def pct(v, of):
    return f'{v / of * 100:.3f}%'


def pin(n, box, page=(1440, 900), inside=False):
    x, y, w, h = box
    pw, ph = page
    return (f'<div class="pin{" pin--in" if inside else ""}" style="left:{pct(x, pw)};top:{pct(y, ph)};'
            f'width:{pct(w, pw)};height:{pct(h, ph)}"><b>{n}</b></div>')


# The three issues pinned on the first screen of the original page
FIRST_PINS = [
    (1, (186, 706, 728, 192), False),
    (2, (235, 5, 970, 90), True),
    (2, (186, 552, 1084, 136), True),
    (2, (561, 816, 317, 60), False),
    (3, (194, 371, 345, 103), False),
]


def annotated_first():
    pins = ''.join(pin(n, b, inside=i) for n, b, i in FIRST_PINS)
    return f'<div class="annot">{img("old-first", "First screen of the original page with numbered annotations")}{pins}</div>'


def page_map(cls=''):
    """The whole original page with its ads, videos and recommendations marked, measured from Figma."""
    z = ''
    for kind, boxes in C.ZONES_OLD.items():
        for x, y, w, h in boxes:
            z += f'<i class="zone zone--{kind}" style="left:{pct(x, 1440)};top:{pct(y, 6074)};width:{pct(w, 1440)};height:{pct(h, 6074)}"></i>'
    return f'<div class="annot pagemap {cls}">{img("old-full-sm", "The full original page with ads, video modules and recommendations marked in colour")}{z}</div>'


LEGEND = ('<div class="legend"><span><i style="background:var(--red)"></i>Ads</span>'
          '<span><i style="background:var(--yellow)"></i>Video</span>'
          '<span><i style="background:var(--green)"></i>Recommendations</span>'
          '<span><i style="outline:1.5px solid #000;outline-offset:-1.5px"></i>Movie information</span></div>')


def evidence_item(e):
    q = f'<p class="evi__q">“{esc(e["quote"])}”</p>' if e.get('quote') else ''
    return (f'<li>{q}<p class="evi__s">{esc(e["says"])}</p>'
            f'<span class="evi__m"><a href="{esc(e["url"])}" target="_blank" rel="noopener">{esc(e["who"])}, {esc(e["source"])}</a> · {esc(e["date"])}</span></li>')


def evidence(items):
    return '<ul class="evi">' + ''.join(evidence_item(e) for e in items) + '</ul>'


def theme(t, n=None):
    return f'''<article class="theme">
  <h4 class="theme__t">{esc(t["title"])}</h4>
  <p class="theme__b">{esc(t["body"])}</p>
  {evidence(t["evidence"])}
</article>'''


def pull_quote():
    p = C.DISCONNECT['pull']
    return (f'<blockquote class="pull"><span class="hang">“…</span>{esc(p["text"])}”'
            f'<cite><a class="link" href="{esc(p["url"])}" target="_blank" rel="noopener">{esc(p["who"])}, {esc(p["source"])}</a> · {esc(p["date"])}</cite></blockquote>')


def pido(d):
    L = C.DECISIONS['labels']
    hyp = f'<p class="pido__hyp">{esc(d["hypothesis"])}</p>' if d.get('hypothesis') else ''
    note = f'<p class="pido__hyp">{esc(d["note"])}</p>' if d.get('note') else ''
    return f'''<div class="pido">
  <div><span class="label">{L[0]}</span><p>{esc(d["problem"])}</p></div>
  <div><span class="label">{L[1]}</span><p>{esc(d["insight"])}</p></div>
  <div><span class="label">{L[2]}</span><p>{esc(d["decision"])}</p></div>
  <div><span class="label label--red">{L[3]}</span><p>{esc(d["outcome"])}</p>{hyp}{note}</div>
</div>'''


def voices(d):
    out = ''
    for v in d.get('voices', []):
        pts = ''.join(f'<li>{esc(p)}</li>' for p in v['points'])
        out += f'<div class="voice"><h4 class="voice__n">{esc(v["name"])}</h4><p class="voice__d">{esc(v["dir"])}</p><ul>{pts}</ul></div>'
    return out


def journey():
    li = ''
    for s in C.REALITY['context']['journey']:
        li += f'<li class="{"on" if s["on"] else ""}"><span class="journey__s">{s["step"]}</span><span class="journey__q">{esc(s["q"])}</span></li>'
    return f'<ol class="journey">{li}</ol>'


def meters():
    o = ''
    for m in C.REALITY['ratings']['meters']:
        o += f'''<article class="meter">
  <div class="meter__top">{icon(m["icon"], m["name"] + " icon", "meter__icon")}<span class="small">{esc(m["count"])}</span></div>
  <div><div class="meter__score">{m["score"]}</div>
  <h4 class="meter__name" style="margin-top:var(--s4)">{m["name"]}</h4><p class="meter__def">{esc(m["def"])}</p><p class="meter__ask">{esc(m["asks"])}</p></div>
</article>'''
    return o


def hierarchy():
    li = ''
    for t in C.ARCHITECTURE['tiers']:
        items = ''.join(f'<span>{esc(i)}</span>' for i in t['items'])
        li += f'<li class="t" data-t="{t["id"]}"><span class="hier__id">{t["id"]}</span><div><p class="hier__n">{esc(t["name"])}</p><div class="hier__i">{items}</div></div></li>'
    return f'<ol class="hier">{li}</ol>'


def slope(cls=''):
    """Slope chart of where each element sits on the two pages. One accent, labels on every line."""
    a = C.ARCHITECTURE
    W, H, L, R, T = 780, 760, 196, 584, 34
    k = (H - T - 28) / a['page_old']
    Y = lambda v: T + v * k
    color = {'P0': 'var(--red)', 'P1': 'var(--fg)', 'P3': 'var(--fg-3)'}
    stroke = {'P0': 3, 'P1': 2, 'P3': 2}
    tier_name = {t['id']: t['name'] for t in a['tiers']}

    def spread(vals, gap=17):
        """Push labels apart so none collide, keeping their order."""
        ys = sorted(((Y(v), i) for i, v in enumerate(vals)))
        out = {}
        prev = -99
        for y, i in ys:
            y = max(y, prev + gap)
            out[i] = y
            prev = y
        return out

    ly = spread([m[2] for m in a['moves']])
    ry = spread([m[3] for m in a['moves']])
    parts = [f'<svg class="slope {cls}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(a["chart_label"], quote=True)}. Ratings move from 706 to 228 pixels, the full synopsis from 4,376 to 1,097.">']
    parts.append(f'<text x="{L}" y="14" text-anchor="middle" class="sl-h">Original</text><text x="{R}" y="14" text-anchor="middle" class="sl-h">Redesign</text>')
    parts.append(f'<line x1="{L}" x2="{L}" y1="{T}" y2="{Y(a["page_old"])}" class="sl-axis"/><line x1="{R}" x2="{R}" y1="{T}" y2="{Y(a["page_new"])}" class="sl-axis"/>')
    fy = Y(C.FOLD)
    parts.insert(1, f'<rect x="0" y="{T}" width="{W}" height="{fy - T}" class="sl-band"/><text x="8" y="{T + 16}" class="sl-note">First screen, 900px</text>')
    order = sorted(range(len(a['moves'])), key=lambda i: {'P3': 0, 'P1': 1, 'P0': 2}[a['moves'][i][1]])
    for i in order:
        name, tier, y0, y1 = a['moves'][i]
        c = color[tier]
        title = f'{name} ({tier}, {tier_name[tier]}): {y0:,}px to {y1:,}px'
        parts.append(f'<g class="sl-row" tabindex="0"><title>{esc(title)}</title>'
                     f'<line x1="{L}" x2="{R}" y1="{Y(y0)}" y2="{Y(y1)}" stroke="transparent" stroke-width="16"/>'
                     f'<line x1="{L}" x2="{R}" y1="{Y(y0)}" y2="{Y(y1)}" stroke="{c}" stroke-width="{stroke[tier]}" stroke-linecap="round"/>'
                     f'<circle cx="{L}" cy="{Y(y0)}" r="4.5" fill="{c}" stroke="var(--chart-bg,var(--bg))" stroke-width="2"/>'
                     f'<circle cx="{R}" cy="{Y(y1)}" r="4.5" fill="{c}" stroke="var(--chart-bg,var(--bg))" stroke-width="2"/>'
                     f'<text x="{L - 14}" y="{ly[i] + 4}" text-anchor="end" class="sl-l"><tspan class="sl-v">{y0:,}</tspan>  {esc(name)}</text>'
                     f'<text x="{R + 14}" y="{ry[i] + 4}" class="sl-l">{esc(name)}  <tspan class="sl-v">{y1:,}</tspan></text></g>')
    parts.append('</svg>')
    legend = ('<div class="legend sl-legend"><span><i style="background:var(--red)"></i>P0 Core</span>'
              '<span><i style="background:var(--fg)"></i>P1 Decision support</span>'
              '<span><i style="background:var(--fg-3)"></i>P3 Discovery</span></div>')
    rows = ''.join(f'<tr><th scope="row">{esc(m[0])}</th><td>{m[1]}</td><td>{m[2]:,}</td><td>{m[3]:,}</td></tr>' for m in a['moves'])
    table = (f'<details class="sl-table"><summary class="small">View as table</summary><table><thead><tr><th>Element</th><th>Tier</th>'
             f'<th>Original (px)</th><th>Redesign (px)</th></tr></thead><tbody>{rows}</tbody></table></details>')
    return legend + ''.join(parts) + table


def about_panel():
    m = C.META
    return f'''<aside class="about" aria-hidden="true" aria-label="About the project">
  <button class="chip about__x" aria-label="Close">Close ×</button>
  <span class="label">About the project</span>
  <p class="lead" style="margin-top:var(--s4);padding-right:var(--s7)">{esc(m["project"])}, using {esc(m["example"])} as the example.</p>
  <dl>
    <dt>Designer</dt><dd>{esc(m["author"])}</dd>
    <dt>Context</dt><dd>{esc(m["context"])}</dd>
    <dt>Scope</dt><dd>{esc(m["scope"])}</dd>
    <dt>Date</dt><dd>{esc(m["date"])}</dd>
    <dt>Method</dt><dd>Community research, heuristic evaluation, information architecture, four design directions, interactive prototype</dd>
  </dl>
  <p class="small" style="margin-top:var(--s6)">{esc(m["placeholders"])}</p>
  <p class="small" style="margin-top:var(--s3)">{esc(m["disclaimer"])}</p>
</aside>'''


def head(title, css, desc=None, theme_attr='light', extra=''):
    d = esc(desc or C.META['subtitle'], quote=True)
    return f'''<!doctype html>
<html lang="en" data-theme="{theme_attr}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{d}">
<link rel="icon" href="{ASSETS}/svg/tomato.svg" type="image/svg+xml">
<link rel="preload" href="{ASSETS}/fonts/instrument-sans-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{ASSETS}/fonts/outfit-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="../shared/system.css">
<link rel="stylesheet" href="{css}">
{extra}
</head>'''


def rotten_tomatoes_chunk():
    """The wordmark's trick applied to live type: a splat in Rotten, a tomato in Tomatoes."""
    return ('<span class="nb">R<span class="o-splat"><i></i></span>tten</span> '
            '<span class="nb">Tomat<i class="glyph glyph--tomato"></i>es</span>')
