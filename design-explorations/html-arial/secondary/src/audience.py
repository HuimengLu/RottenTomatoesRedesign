"""All Audience Reviews: five presentations."""
from base import *

TABS = ['Overview', 'Where to Watch', 'Reviews', 'Cast', 'Media', 'More']


def av(a, i, size=36):
    return avatar(a['name'][0].upper(), size, AV_COLORS[i % len(AV_COLORS)])


def meta(a, i, size=36):
    return row(av(a, i, size) + T(a['name'], 15, 18, 700, INK, nw=True) + verified() + stars(a['stars'], 14) + T(a['date'], 13, 16, 400, G6, nw=True), 10)


def helpful(a):
    return row(row(I('thumbs-up', 17, G7, 1.8) + T(a['helpful'], 14, 16, 700, G7, nw=True), 6) + T('Helpful?', 14, 16, 400, G6, nw=True), 16, name='Helpful')


def popcorn_card(w=320):
    bars = ''
    for s, pct in DIST:
        tw = w - 48 - 36 - 44
        bars += row(T(f'{s}★', 13, 16, 700, INK, 'width:28px', nw=True) + f'<div style="width:{tw}px;height:8px;border-radius:4px;background:{G15};overflow:hidden"><div style="width:{round(tw * pct / 100)}px;height:8px;background:{AMBER}"></div></div>'
                    + T(f'{pct}%', 13, 16, 400, G6, 'width:36px;text-align:right', nw=True), 8)
    return f'''<div data-name="Popcornmeter summary" class="col" style="width:{w}px;padding:24px;border-radius:16px;background:{SURF};gap:18px">
  {row(I('popcorn', 50) + col(T(f'{POP}%', 56, 52, 700, INK, 'letter-spacing:-1.5px', nw=True) + label('Popcornmeter', G6), 6), 14)}
  {T(f'{POP_RATINGS} verified ratings', 14, 20, 400, G7)}
  {row(T(POP_AVG, 30, 32, 700, INK, nw=True) + col(stars(4, 16) + T('average rating', 13, 16, 400, G6, nw=True), 4), 12)}
  {col(bars, 8, name='Distribution')}</div>'''


def composer(w, title='What did you think of La La Land?', big=False):
    st = ''.join(I('star', 26 if big else 24, G3, 1.6) for _ in range(5))
    return (f'<div data-name="Rate &amp; review composer" class="row" style="width:{w}px;padding:16px 20px;border-radius:12px;background:{SURF};border:1px solid {G2};align-items:center;justify-content:space-between">'
            f'{T(title, 16, 20, 700, INK, nw=True)}{row(st, 4, name="Star input")}</div>')


def toggle(on=True):
    return f'<div data-name="Toggle" style="width:40px;height:24px;border-radius:12px;background:{INK if on else G3};position:relative;flex:none"><div style="position:absolute;top:3px;left:{19 if on else 3}px;width:18px;height:18px;border-radius:9px;background:#fff"></div></div>'


def review_card(a, i, w=776, text=None, extra_top=''):
    t = text or a['text']
    return f'''<div data-name="Audience review · {a['name']}" class="col" style="width:{w}px;padding:24px;border-radius:16px;background:{SURF};gap:14px">
  {extra_top}{row(meta(a, i) + I('more', 20, G6, 2.2), 0, justify='space-between')}
  {T(t, 18, 28, 400, INK2, w=w - 48)}
  {helpful(a)}</div>'''


# ---------------------------------------------------------------- 01 · full page
def a1():
    side = col(popcorn_card() + composer(320, 'Rate it') .replace('width:320px;padding:16px 20px', 'width:320px;padding:16px 18px')
               + row(T('Verified ticket holders only', 14, 18, 700, INK, nw=True) + toggle(True), 0, justify='space-between', extra=f'width:320px;padding:14px 18px;border-radius:12px;background:{SURF}'), 16, 'width:320px', 'Sidebar')
    chips_ = row(chip('Most helpful', True) + chip('Newest') + chip('5★') + chip('4★') + chip('3★ & below'), 8)
    cards = ''.join(review_card(a, i) for i, a in enumerate(AUD))
    more = row(btn('Load more reviews', 'secondary') + T(f'Showing 7 of {POP_RATINGS}', 14, 16, 400, G6, nw=True), 16, extra='padding-top:8px')
    body = row(side + col(chips_ + cards + more, 16, 'width:776px', 'Review list'), 24, 'flex-start', extra='width:1120px;padding:8px 0 80px')
    title = page_title('Reviews', 'Audience Reviews', f'{POP_RATINGS} verified ratings from Fandango ticket buyers', segmented(['Critics', 'Audience'], 1, G15))
    return screen('Audience reviews · Full page', header_light() + film_bar('Reviews', TABS) + '<div style="height:40px"></div>' + title + '<div style="height:28px"></div>' + body)


# ---------------------------------------------------------------- 02 · drawer
def a2():
    items = ''
    for i, a in enumerate(AUD[:5]):
        items += f'''<div data-name="Audience review · {a['name']}" class="col" style="gap:10px;padding:20px 0;border-bottom:1px solid {G15}">
  {row(row(av(a, i, 28) + T(a['name'], 14, 16, 700, INK, nw=True) + stars(a['stars'], 13) + T(a['date'], 13, 16, 400, G6, nw=True), 8) + I('more', 18, G6, 2.2), 0, justify='space-between')}
  {T(a['text'], 16, 25, 400, INK2, 'display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden', w=496)}
  {row(row(I('thumbs-up', 15, G7, 1.8) + T(a['helpful'], 13, 16, 700, G7, nw=True), 6) + verified(), 16)}</div>'''
    panel = f'''<div data-name="Drawer · Audience reviews" class="col" style="position:absolute;right:0;top:0;width:560px;height:900px;background:{SURF};box-shadow:-24px 0 60px rgba(0,0,0,.35)">
  <div class="col" style="padding:24px 32px 18px;gap:16px;border-bottom:1px solid {G15}">
    {row(T('Audience Reviews', 26, 30, 700, INK, nw=True) + icon_btn('x', 40), 0, 'center', 'space-between')}
    {row(I('popcorn', 30) + col(row(T(f'{POP}%', 22, 24, 700, INK, nw=True) + T('Popcornmeter', 14, 16, 400, G6, nw=True), 8) + T(f'{POP_RATINGS} verified ratings · average {POP_AVG}', 13, 16, 400, G6, nw=True), 2), 10)}
    {row(chip('Most helpful', True) + chip('Newest') + chip('5★') + chip('4★') + chip('More', icon=None) .replace('More<', 'More ▾<'), 6)}</div>
  <div class="col" style="padding:0 32px;flex:1;overflow:hidden">{items}</div>
  <div data-name="Pinned composer" class="col" style="padding:16px 32px 20px;gap:10px;border-top:1px solid {G15};background:#FAFAFA">
    {row(T('What did you think of La La Land?', 16, 20, 700, INK, nw=True) + row(''.join(I('star', 26, G3, 1.6) for _ in range(5)), 4), 0, 'center', 'space-between')}
    {T('Tap a star to rate. A written review is optional.', 13, 16, 400, G6, nw=True)}</div>
</div>'''
    return overlay('Audience reviews · Drawer', 'audience', panel)


# ---------------------------------------------------------------- 03 · fan wall
def wall_card(a, i, w=352, big=False, badge=''):
    if big:
        return f'''<div data-name="Audience review · {a['name']}" class="col" style="width:{w}px;padding:28px 26px;border-radius:16px;background:{SURF};gap:18px">
  {badge}{stars(a['stars'], 20, gap=3)}
  {T('“' + a['text'] + '”', 26, 34, 700, INK, 'letter-spacing:-0.3px', w=w - 52)}
  {row(av(a, i, 32) + T(a['name'], 15, 18, 700, INK, nw=True) + verified(), 8)}</div>'''
    return f'''<div data-name="Audience review · {a['name']}" class="col" style="width:{w}px;padding:24px;border-radius:16px;background:{SURF};gap:14px">
  {badge}{row(av(a, i, 32) + col(T(a['name'], 15, 18, 700, INK, nw=True) + T(a['date'], 13, 16, 400, G6, nw=True), 2), 10)}
  {stars(a['stars'], 15)}
  {T(a['text'], 17, 27, 400, INK2, w=w - 48)}
  {row(row(I('thumbs-up', 15, G7, 1.8) + T(a['helpful'], 13, 16, 700, G7, nw=True), 6) + verified(), 16)}</div>'''


def a3():
    fl, ve, za, isa, lu, so, me = AUD
    badge = f'<div class="row nw" style="{FONT}align-self:flex-start;gap:6px;height:24px;padding:0 10px;border-radius:12px;background:{TOPBG};color:{ARED};font-size:12px;font-weight:700;align-items:center">{I("thumbs-up", 13, ARED, 2)}Most helpful</div>'
    c1 = col(wall_card(fl, 0, badge=badge) + wall_card(so, 5, big=True) + wall_card(isa, 3), 24)
    c2 = col(wall_card(me, 6, big=True) + wall_card(ve, 1) + composer(352, 'Seen it? Rate it', False).replace('justify-content:space-between', 'justify-content:space-between;flex-direction:column;align-items:flex-start;gap:12px'), 24)
    c3 = col(wall_card(za, 2) + wall_card(lu, 4, big=True), 24)
    mast = col(label('Reviews · Audience', ARED) + T('What audiences are saying', 64, 64, 700, INK, 'letter-spacing:-2px', nw=True)
               + row(row(I('popcorn', 26) + T(f'{POP}% Popcornmeter', 17, 20, 700, INK, nw=True) + T(f'· {POP_RATINGS} verified ratings', 17, 20, 400, G7, nw=True), 8)
                     + row(chip('All', True) + chip('Loved it') + chip('Mixed') + chip('Re-release'), 8), 0, 'center', 'space-between', 'width:1120px'), 14, 'width:1120px;padding:48px 0 32px')
    wall = row(c1 + c2 + c3, 32, 'flex-start', extra='width:1120px;padding-bottom:80px', name='Wall')
    return screen('Audience reviews · Wall', header_light() + film_bar('Reviews', TABS) + mast + wall)


# ---------------------------------------------------------------- 04 · topics
def mark(t):
    return f'<span style="background:rgba(255,215,0,.38);border-radius:3px;padding:0 2px">{t}</span>'


def a4():
    topics = [('Seeing it in theaters', 'Mostly positive', 92, True), ('Ryan & Emma', 'Mostly positive', 95, False), ('The music', 'Mostly positive', 90, False),
              ('Cinematography', 'Mostly positive', 94, False), ('The ending', 'Mixed', 58, False), ('Pacing', 'Mixed', 46, False)]
    cards = ''
    for name, sent, pos, on in topics:
        bw = 140
        cards += f'''<div data-name="Topic · {name}" class="col" style="width:170px;padding:16px;border-radius:12px;gap:10px;{"background:#000;" if on else "background:" + SURF + ";"}">
  {T(name, 15, 18, 700, '#fff' if on else INK, w=138)}
  <div style="width:{bw}px;height:6px;border-radius:3px;background:{"rgba(255,255,255,.2)" if on else G15};overflow:hidden"><div style="width:{round(bw * pos / 100)}px;height:6px;background:{AMBER if not on else "#FFD700"}"></div></div>
  {T(sent, 13, 16, 400, 'rgba(255,255,255,.75)' if on else G6, nw=True)}</div>'''
    fl, ve, za, isa = AUD[0], AUD[1], AUD[2], AUD[3]
    hits = [
        (fl, 0, 'I was thrilled that they ' + mark('brought this masterpiece back to Dolby Cinema') + ' for 10th Anniversary. It was every bit as powerful and emotional as the first time that I saw it 10 years ago. Ryan &amp; Emmas chemistry is legendary!'),
        (za, 2, 'Amazing cinematography and ' + mark('seeing it in Dolby') + ' made me appreciate this film more. Ryan Gosling was a standout, some of the songs dragged on a bit but overall great movie and certainly lived up to the hype.'),
        (isa, 3, 'Loved ' + mark('rewatching it in theaters') + ' and crying because I knew what was coming in the end. Overall such a great film i think anyone can enjoy.'),
    ]
    results = ''.join(review_card(a, i, 1120, t) for a, i, t in hits)
    head = row(col(T('3 reviews mention <b>seeing it in theaters</b>', 20, 26, 400, INK, nw=True) + row(I('sparkle', 15, G6, 1.8) + T('Topics are generated from review text and update as new reviews arrive.', 13, 16, 400, G6, nw=True), 6), 6)
               + row(T('Sort', 14, 16, 400, G6, nw=True) + row(T('Most helpful', 14, 16, 700, INK, nw=True) + I('chevron-down', 16, INK, 2), 6, extra=f'height:36px;padding:0 12px;border-radius:8px;background:{SURF};border:1px solid {G2}'), 10), 0, 'flex-end', 'space-between', 'width:1120px')
    title = page_title('Reviews · Audience', 'What people talk about', f'{POP}% Popcornmeter · {POP_RATINGS} verified ratings', segmented(['Critics', 'Audience'], 1, G15))
    return screen('Audience reviews · Topics', header_light() + film_bar('Reviews', TABS) + '<div style="height:40px"></div>' + title + '<div style="height:28px"></div>'
                  + row(cards, 20, 'stretch', extra='width:1120px', name='Topics') + '<div style="height:36px"></div>' + head + '<div style="height:18px"></div>'
                  + col(results, 16, 'width:1120px;padding-bottom:80px'))


# ---------------------------------------------------------------- 05 · in-place expansion
def a5():
    cards = ''
    pairs = [(AUD[0], 0), (AUD[1], 1), (AUD[2], 2), (AUD[3], 3)]
    colA = col(''.join(review_card(a, i, 636) for a, i in pairs[0::2]), 16)
    colB = col(''.join(review_card(a, i, 636) for a, i in pairs[1::2]), 16)
    panel = f'''<div data-name="Expanded audience reviews" class="col" style="position:absolute;left:32px;top:96px;width:1376px;height:804px;border-radius:24px 24px 0 0;background:{BG};overflow:hidden;box-shadow:0 -12px 40px rgba(0,0,0,.35)">
  <div class="row" style="height:96px;padding:0 40px;align-items:center;justify-content:space-between;background:{SURF};border-bottom:1px solid {G15}">
    {row(T('Audience Reviews', 28, 32, 700, INK, nw=True) + row(I('popcorn', 26) + T(f'{POP}%', 20, 22, 700, INK, nw=True) + T(f'· {POP_RATINGS} ratings · average {POP_AVG}', 15, 18, 400, G6, nw=True), 8), 28)}
    {row(segmented(['Most helpful', 'Newest', 'Verified'], 0, G15) + btn('Collapse', 'secondary', 'chevron-up', 40), 12)}</div>
  <div class="col" style="padding:24px 40px 0;gap:16px">{composer(1296, 'What did you think of La La Land?', True)}{row(colA + colB, 24, 'flex-start')}</div>
  <div style="position:absolute;left:0;right:0;bottom:0;height:120px;background:linear-gradient(rgba(244,244,244,0),{BG})"></div>
</div>'''
    return overlay('Audience reviews · Expand in place', 'audience', panel, 0.0)


VARIANTS = [
    (a1, 'Full page', 'Ratings & reviews', 'Popcornmeter, star distribution and a rate-first entry on the left; filterable review cards with helpful votes on the right.',
     'The audience counterpart of the critics page: same frame, Critics / Audience toggle, so switching sides keeps your place. Distribution values are illustrative.'),
    (a2, 'Drawer', 'Read & rate', 'A drawer over the film page with the rate-first composer pinned to the bottom, so reading and rating happen in one place.',
     'Lowest effort to contribute: the prompt is always in reach while you read. Clamped to three lines per review.'),
    (a3, 'Full page', 'Fan wall', 'A masonry wall. Short, emphatic reviews become large quote cards; long ones read normally. A rate prompt lives inside the wall.',
     'Feels like a crowd, not a list: good for a re-release moment. Harder to sort or compare; keep it as an alternate view.'),
    (a4, 'Full page', 'Topics', 'Topic cards summarise what people discuss; picking one filters the reviews and highlights the matching phrase.',
     'Answers “what do people say about X?” without reading everything. Needs a text-analysis pipeline; topic shares here are illustrative.'),
    (a5, 'In place', 'Expand on the page', 'The audience card grows into a light panel right on the film page, with a Collapse control instead of navigation.',
     'No context switch at all. Best for a few more reviews; for thousands, link onward to the full page.'),
]
