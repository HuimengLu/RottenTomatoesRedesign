"""Version B, The Long Take: one unbroken shot. A fixed stage holds both pages; scrolling moves the camera."""
import json

import content as C
from components import *

NEW_X = 1700  # the redesign sits to the right of the original in world space
SORT = (-560, 1980)  # top-left of the sorted layout, in the original page's coordinates


def rect_new(x, y, w, h):
    return [x + NEW_X, y, w, h]


# Modules that lift off the original page. (image, from box, tier, column, slot height handled below)
BLOCKS = [
    ('old-hero', (170, 226, 1100, 480), 'P0'),
    ('old-scorecard', (186, 706, 728, 250), 'P0'),
    ('old-synopsis', (186, 4376, 728, 280), 'P0'),
    ('old-where', (186, 1026, 728, 239), 'P1'),
    ('old-know', (186, 1265, 728, 242), 'P1'),
    ('old-critics', (186, 1649, 728, 388), 'P1'),
    ('old-audience', (186, 2037, 728, 322), 'P1'),
    ('old-rating', (186, 2359, 728, 255), 'P2'),
    ('old-cast', (186, 2615, 728, 260), 'P3'),
    ('old-clips', (186, 2875, 728, 310), 'P3'),
    ('old-more', (186, 3185, 728, 482), 'P3'),
    ('old-videos', (186, 3667, 728, 310), 'P3b'),
    ('old-photos', (186, 3977, 728, 257), 'P3b'),
    ('old-side', (954, 722, 300, 605), 'P3b'),
    ('old-ad1', (186, 1507, 728, 142), 'AD'),
    ('old-ad2', (186, 4234, 728, 142), 'AD'),
    ('old-mpu', (954, 1327, 300, 290), 'AD'),
]
COLS = {'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3, 'P3b': 4, 'AD': 5}
COL_W = 330
GAP = 40
TOP = 96


def sorted_layout():
    """Stack each tier in a column, in world coordinates of the original page."""
    x0, y0 = SORT
    cursor = {k: y0 + TOP for k in COLS}
    out = []
    for name, box, tier in BLOCKS:
        x, y, w, h = box
        s = COL_W / w
        if w < 400:
            s = (COL_W * .62) / w
        tx = x0 + COLS[tier] * (COL_W + GAP)
        ty = cursor[tier]
        cursor[tier] += h * s + 14
        out.append({'name': name, 'from': box, 'tier': tier, 'tx': round(tx, 1), 'ty': round(ty, 1), 's': round(s, 4)})
    return out


SORT_RECT = [SORT[0] - 70, SORT[1] - 280, 6 * COL_W + 5 * GAP + 140, 1420]


def blocks_html():
    h = ''
    for b in sorted_layout():
        x, y, w, hh = b['from']
        h += (f'<div class="blk" style="left:{x}px;top:{y}px;width:{w}px;height:{hh}px" '
              f'data-t="{b["tx"] - x},{b["ty"] - y},{b["s"]}">{img(b["name"], "", eager=True).replace("decoding=\"async\"", "decoding=\"sync\"")}</div>')
    for tier, n in [('P0', 'Core movie information'), ('P1', 'Decision support'), ('P2', 'Engagement'), ('P3', 'Discovery'), ('AD', 'What must remain')]:
        x = SORT[0] + COLS[tier] * (COL_W + GAP)
        label = 'Ads' if tier == 'AD' else tier
        h += f'<div class="tier" data-tier style="left:{x}px;top:{SORT[1]}px;width:{COL_W}px"><b class="chunk">{label}</b><span>{esc(n)}</span></div>'
    return h


def zones_html():
    z = ''
    for kind, boxes in C.ZONES_OLD.items():
        for x, y, w, h in boxes:
            z += f'<i class="wz wz--{kind}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"></i>'
    # distribution: the actions and modules that lead to watching
    for x, y, w, h in [(186, 1026, 728, 239), (372, 866, 730, 64)]:
        z += f'<i class="wz wz--dist" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"></i>'
    for n, b, i in FIRST_PINS:
        x, y, w, h = b
        z += f'<div class="wp" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><b>{n}</b></div>'
    # the route a reader takes between the things they need
    stops = [('Ratings', 706), ('Where to Watch', 1026), ('Critics', 1649), ('Audience', 2037), ('Full synopsis', 4376)]
    pts = ' '.join(f'{(1090 if i % 2 else 110)},{y + 40}' for i, (n, y) in enumerate(stops))
    route = f'<svg class="route" viewBox="0 0 1440 6074" width="1440" height="6074"><polyline points="{pts}" fill="none" stroke="#FA320A" stroke-width="14" stroke-linejoin="round"/>'
    for i, (n, y) in enumerate(stops):
        cx = 1090 if i % 2 else 110
        route += f'<circle cx="{cx}" cy="{y + 40}" r="30" fill="#FA320A"/><text x="{cx}" y="{y + 52}" text-anchor="middle" fill="#fff" font-size="36" font-weight="700">{i + 1}</text>'
    route += '</svg>'
    return z + route


def step(body, cam, mode='side', fx='', bg='gray', cls='', pid='', hold=None, ch=None, page=None):
    data = {'cam': cam, 'mode': mode, 'fx': fx, 'bg': bg}
    if page:
        data['page'] = page
    id_attr = f' id="{pid}"' if pid else ''
    h = f' style="--hold:{hold}"' if hold else ''
    chap = f' data-ch="{ch}"' if ch else ''
    return f'<section class="step step--{mode} {cls}"{id_attr}{h}{chap} data-step=\'{json.dumps(data)}\'><div class="panel">{body}</div></section>'


def head_block(n, name, title):
    return f'<p class="label label--red">{n} · {esc(name)}</p><h2 class="st-h">{title}</h2>'


def steps():
    m, o, d, r, a, D, e, R = C.META, C.OPENING, C.DISCONNECT, C.REALITY, C.ARCHITECTURE, C.DECISIONS, C.EXPERIENCE, C.REFLECTION
    tags = ''.join(f'<span class="tag">{t}</span>' for t in m['tags'])
    wide = [-120, -60, NEW_X + 1440 + 240, 6200]
    S = []
    # 00
    S.append(step(f'''<h1 class="lt-title">{esc(m["title"])}</h1><p class="lead">{esc(m["subtitle"])}</p><div class="tags">{tags}</div>
      <button class="chip" data-about style="margin-top:var(--s4)">About the project <span aria-hidden="true">+</span></button>
      <p class="small lt-hint">One continuous shot. Scroll to move the camera.</p>''', [-420, -40, NEW_X + 1440 + 480, 6240], 'wide', 'labels', pid='opening', ch='00'))
    S.append(step(f'<p class="st-b">{esc(o["headline"])}</p><p class="st-b st-q">{esc(o["question"])}</p>', [0, 0, 1440, 900], page='Original'))
    # 01
    S.append(step(head_block('01', 'The Disconnect', esc(d['headline'])) + f'<p class="st-p">{esc(d["lead"])}</p>', [170, 226, 1100, 690], pid='disconnect', ch='01', page='Original'))
    cams = [[200, 690, 700, 300], [170, 1640, 760, 730], [186, 706, 240, 180], [170, 722, 1100, 560]]
    for i, t in enumerate(d['themes']):
        lbl = f'<p class="label">A. {esc(d["voices_label"])}</p>' if i == 0 else ''
        S.append(step(f'{lbl}<h3 class="st-t">{esc(t["title"])}</h3><p class="st-p">{esc(t["body"])}</p>{evidence(t["evidence"])}', cams[i], page='Original'))
    builders = ''.join(f'<li><a href="{esc(b["url"])}" target="_blank" rel="noopener"><b>{b["year"]}</b> {esc(b["name"])}</a></li>' for b in d['builders'])
    S.append(step(f'{pull_quote()}<h3 class="st-t" style="margin-top:var(--s7)">{esc(d["builders_label"])}</h3><p class="st-p">{esc(d["builders_note"])}</p><ul class="st-list">{builders}</ul><p class="small" style="margin-top:var(--s4)">{esc(d["voices_note"])}</p>', [170, 722, 1100, 560], page='Original'))
    i1, i2, i3 = d['issues']
    S.append(step(f'<p class="label">B. {esc(d["audit_label"])}</p><h3 class="st-t"><span class="n-b">1</span>{esc(i1["title"])}</h3><p class="st-p">{esc(i1["body"])}</p><p class="small">{esc(i1["detail"])}</p><p class="small" style="margin-top:var(--s4)">{esc(d["audit_note"])}</p>', [0, 0, 1440, 900], fx='pins', page='Original'))
    S.append(step(f'<h3 class="st-t"><span class="n-b">2</span>{esc(i2["title"])}</h3><p class="st-p">{esc(i2["body"])}</p><p class="small">{esc(i2["detail"])}</p>{LEGEND}', [-200, -40, 1840, 6160], fx='zones', page='Original'))
    S.append(step(f'<h3 class="st-t"><span class="n-b">3</span>{esc(i3["title"])}</h3><p class="st-p">{esc(i3["body"])}</p><p class="small">{esc(i3["detail"])}</p>', [-200, -40, 1840, 6160], fx='route', page='Original'))
    S.append(step(f'<p class="lt-state">{esc(d["conclusion"])}</p>', [-200, -40, 1840, 6160], 'full', 'dim'))
    # 02
    b, cx, t = r['business'], r['context'], r['ratings']
    S.append(step(head_block('02', 'The Product Reality', esc(r['headline'])) + f'<p class="st-p">{esc(r["lead"])}</p><h3 class="st-t" style="margin-top:var(--s6)">{esc(b["title"])}</h3><p class="st-p">{esc(b["body"])}</p>'
                  f'<div class="pathrow"><b class="chunk">{b["paths"][0]["name"]}</b><p>{esc(b["paths"][0]["body"])}</p></div>', [-200, -40, 1840, 6160], fx='ads', pid='reality', ch='02', page='Original'))
    S.append(step(f'<div class="pathrow"><b class="chunk">{b["paths"][1]["name"]}</b><p>{esc(b["paths"][1]["body"])}</p></div>', [170, 706, 1100, 590], fx='dist', page='Original'))
    S.append(step(f'<h3 class="st-t">{esc(cx["title"])}</h3><p class="st-p">{esc(cx["body"])}</p><div class="lt-j">{journey()}</div>', [170, 226, 1100, 800], page='Original'))
    S.append(step(f'<h3 class="st-t">{esc(t["title"])}</h3><p class="st-p">{esc(t["body"])}</p><div class="lt-m">{meters()}</div>', [356, 730, 660, 124], page='Original'))
    S.append(step(f'<p class="lt-state">{esc(r["conclusion"])}</p>', [356, 730, 660, 124], 'full', 'dim'))
    # 03
    S.append(step(head_block('03', 'Information Architecture', esc(a['headline'])) + f'<p class="st-p">{esc(a["lead"])}</p>', SORT_RECT, 'full', 'sort', 'gray', 'step--sort', pid='architecture', ch='03', hold=2.4))
    S.append(step(f'<h3 class="label">{esc(a["chart_label"])}</h3>{slope()}<p class="small" style="margin-top:var(--s2)">{esc(a["chart_note"])}</p>', SORT_RECT, 'wide', 'sorted'))
    # 04
    S.append(step(head_block('04', 'Key Design Decisions', esc(D['lead'])).replace('label--red', 'label--on-dark').replace('st-h', 'lt-state'), rect_new(-200, -60, 1840, 1150), 'full', 'dim', 'tint', pid='decisions', ch='04'))

    def dec(d, extra=''):
        L = D['labels']
        hyp = f'<p class="small">{esc(d["hypothesis"])}</p>' if d.get('hypothesis') else ''
        note = f'<p class="small">{esc(d["note"])}</p>' if d.get('note') else ''
        return (f'<p class="label label--red">Decision {d["n"]}</p><h3 class="st-h st-h--sm">{esc(d["title"])}</h3>'
                f'<dl class="lt-p"><dt>{L[0]}</dt><dd>{esc(d["problem"])}</dd><dt>{L[1]}</dt><dd>{esc(d["insight"])}</dd>'
                f'<dt>{L[2]}</dt><dd>{esc(d["decision"])}</dd><dt>{L[3]}</dt><dd>{esc(d["outcome"])}</dd></dl>{hyp}{note}{extra}')

    I = D['items']
    say = lambda x: f'<p class="lt-say">{esc(x["statement"])}</p>'
    S.append(step(dec(I[0]) + say(I[0]), rect_new(0, 0, 1440, 900), fx='pip', bg='tint', page='Redesign'))
    strip = ''.join(f'<div class="zoomable" {zoom_attrs(n, l)}>{img(n, l + " exploration")}</div>' for n, l in [('x-critics-cards', 'Cards'), ('x-thecritics', 'Broadsheet'), ('x-news1', 'Pull quote'), ('x-news4', 'Wire')])
    S.append(step(dec(I[1]) + f'<p class="label" style="margin-top:var(--s5)">Early explorations</p><div class="lt-x">{strip}</div>', rect_new(160, 1310, 1120, 836), bg='tint', page='Redesign'))
    S.append(step(voices(I[1]) + say(I[1]), rect_new(160, 2170, 1120, 860), bg='tint', page='Redesign', cls='step--voices'))
    S.append(step(dec(I[2]) + voices({'voices': I[2]['voices'][:1]}), rect_new(0, 1360, 1440, 900), fx='drawer-c', bg='tint', page='Redesign', cls='step--voices'))
    S.append(step(voices({'voices': I[2]['voices'][1:]}) + say(I[2]), rect_new(0, 1360, 1440, 900), fx='drawer-a', bg='tint', page='Redesign', cls='step--voices'))
    S.append(step(dec(I[3]) + say(I[3]), rect_new(160, 776, 1120, 500), bg='tint', page='Redesign'))
    # 05
    S.append(step(head_block('05', 'The Redesigned Experience', esc(e['headline'])) + f'<p class="st-p">{esc(e["lead"])}</p>', rect_new(-60, 0, 1560, 975), 'side', 'travel', 'tint', 'step--travel', pid='experience', ch='05', hold=4, page='Redesign'))
    ints = ''.join(f'<figure class="fig">{video(i["video"], i["name"])}<figcaption class="cap"><span><b>{esc(i["name"])}.</b> {esc(i["body"])}</span></figcaption></figure>' for i in e['interactions'][:2])
    ints2 = ''.join(f'<figure class="fig">{video(i["video"], i["name"])}<figcaption class="cap"><span><b>{esc(i["name"])}.</b> {esc(i["body"])}</span></figcaption></figure>' for i in e['interactions'][2:])
    S.append(step(f'<p class="label">Interactions</p>{ints}', rect_new(0, 1360, 1440, 900), fx='drawer-c', bg='tint', page='Redesign', cls='step--voices'))
    S.append(step(f'{ints2}<p class="small">{esc(e["interactions_note"])} {esc(m["prototype_note"])} <a class="link arrow" href="{m["prototype"]}" target="_blank" rel="noopener">Open the prototype</a></p><p class="small" style="margin-top:var(--s2)">{esc(m["placeholders"])}</p>', rect_new(160, 776, 1120, 500), bg='tint', page='Redesign', cls='step--voices'))
    # 06
    cols = ''
    for c in R['columns']:
        items = ''.join(f'<li>{esc(i)}</li>' for i in c['items'])
        cols += f'<div class="lt-rc"><h4>{esc(c["title"])}</h4><ul>{items}</ul></div>'
    para = ''.join(f'<p class="st-p">{esc(p)}</p>' for p in R['closing'])
    S.append(step(head_block('06', 'Reflection', esc(R['headline'])) + para, [-420, -40, NEW_X + 1440 + 480, 6240], 'wide', 'labels', 'gray', pid='reflection', ch='06'))
    S.append(step(f'{cols}<p class="small" style="margin-top:var(--s5)">{esc(m["author"])}. {esc(m["context"])}, {esc(m["date"])}.</p><p class="small" style="margin-top:var(--s2)">{esc(m["disclaimer"])}</p>', [-420, -40, NEW_X + 1440 + 480, 6240], 'wide', 'labels', 'gray', 'step--end'))
    return ''.join(S)


def chapter_bar():
    ticks = ''.join(f'<a href="#{c[2]}" title="{esc(c[1])}" data-tick="{c[0]}"><span>{c[0]}</span><em>{esc(c[1])}</em></a>' for c in C.CHAPTERS)
    return f'<nav class="bar" data-nav aria-label="Chapters"><div class="bar__p"><i></i></div><div class="bar__t">{ticks}</div></nav>'


def page():
    return head(f'{C.META["title"]} The Long Take', 'longtake.css') + f'''
<body class="v-longtake">
<div class="stage" aria-hidden="true" data-bg="gray">
  <div class="world">
    <div class="pg pg--old">{img("old-full", "", eager=True)}{zones_html()}{blocks_html()}<span class="pg__l">Original</span></div>
    <div class="pg pg--new" style="left:{NEW_X}px">{img("final-full", "", eager=True)}
      <div class="dw dw--c" style="top:1360px">{img("drawer-critics", "")}</div>
      <div class="dw dw--a" style="top:1360px">{img("drawer-audience", "")}</div>
      <span class="pg__l">Redesign</span>
    </div>
  </div>
  <div class="pip">{img("old-first", "")}<span>Original, same frame</span></div>
  <div class="dimmer"></div>
</div>
{chapter_bar()}
<main class="steps">{steps()}</main>
{about_panel()}
<script src="../shared/site.js"></script>
<script src="longtake.js"></script>
</body></html>'''
