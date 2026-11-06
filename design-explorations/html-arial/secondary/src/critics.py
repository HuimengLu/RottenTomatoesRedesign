"""All Critics Reviews: five presentations."""
from base import *

TABS = ['Overview', 'Where to Watch', 'Reviews', 'Cast', 'Media', 'More']
BY_DATE = sorted(CRIT, key=lambda c: (c['date'][-4:], ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'].index(c['date'][:3]), int(c['date'].split()[1].rstrip(','))))


def split_bar(w, h=8):
    fw = round((w - 2) * FRESH / (FRESH + ROTTEN))
    return (f'<div class="col" style="gap:8px;width:{w}px">{row(f"<div style=\"width:{fw}px;height:{h}px;border-radius:{h // 2}px;background:{RED}\"></div><div style=\"width:{w - fw - 2}px;height:{h}px;border-radius:{h // 2}px;background:{GREEN}\"></div>", 2)}'
            f'{row(T(f"{FRESH} Fresh", 13, 16, 700, INK, nw=True) + T(f"{ROTTEN} Rotten", 13, 16, 700, G7, nw=True), 0, justify="space-between")}</div>')


def tomatometer_card(w=320):
    return f'''<div data-name="Tomatometer summary" class="col" style="width:{w}px;padding:24px;border-radius:16px;background:{SURF};gap:18px">
  {row(I('certified-large', 52) + col(row(T(f'{TOMATO}%', 56, 52, 700, INK, 'letter-spacing:-1.5px', nw=True), 0) + label('Tomatometer', G6), 6), 14)}
  {T(f'Certified Fresh · {TOMATO_REVIEWS} reviews · Average {CRITIC_AVG}', 14, 20, 400, G7)}
  {split_bar(w - 48)}
  {rule()}
  {label('Critics consensus', G6)}{T('<b>La La Land</b> ' + CONSENSUS, 15, 23, 400, INK2)}</div>'''


def critic_card(c, w=776):
    sc = T(c['score'], 15, 18, 700, INK, nw=True) if c['score'] else ''
    return f'''<div data-name="Critic review · {c['pub']}" class="col" style="width:{w}px;padding:24px;border-radius:16px;background:{SURF};gap:14px">
  {row(row(outlet(c['pub']) + (top_tag() if c['top'] else '') + T(c['name'], 14, 16, 400, G6, nw=True), 10) + row(tomato(c['fresh'], 20) + sc, 8), 0, justify='space-between')}
  {T('“' + c['q'] + '”', 19, 29, 400, INK2, w=w - 48)}
  {row(T(c['date'], 14, 16, 400, G6, nw=True) + full_review(), 0, justify='space-between')}</div>'''


# ---------------------------------------------------------------- 01 · full page
def c1():
    filters = col(label('Show', G6) + row(chip('All', True, '472') + chip('Top critics') + chip('Fresh', count='428') + chip('Rotten', count='44'), 8, extra='flex-wrap:wrap;width:320px'), 12)
    sort = row(T('Sort', 14, 16, 400, G6, nw=True) + row(T('Newest first', 14, 16, 700, INK, nw=True) + I('chevron-down', 16, INK, 2), 6, extra=f'height:36px;padding:0 12px;border-radius:8px;background:{SURF};border:1px solid {G2}'), 10)
    side = col(tomatometer_card() + filters + sort, 24, 'width:320px', 'Sidebar')
    cards = ''.join(critic_card(c) for c in BY_DATE[::-1])
    more = row(btn('Load more reviews', 'secondary', h=44) + T(f'Showing 9 of {TOMATO_REVIEWS}', 14, 16, 400, G6, nw=True), 16, extra='padding-top:8px')
    body = row(side + col(cards + more, 16, 'width:776px', 'Review list'), 24, 'flex-start', extra='width:1120px;padding:8px 0 80px')
    title = page_title('Reviews', 'Critics Reviews', f'{TOMATO_REVIEWS} reviews from approved Tomatometer critics', segmented(['Critics', 'Audience'], 0, G15))
    return screen('Critics reviews · Full page', header_light() + film_bar('Reviews', TABS) + f'<div style="height:40px"></div>' + title + '<div style="height:28px"></div>' + body)


# ---------------------------------------------------------------- 02 · drawer
def c2():
    tabs = row(''.join(f'<div class="nw" style="{FONT}font-size:15px;line-height:18px;font-weight:700;padding:0 0 12px;color:{INK if i == 0 else G6};border-bottom:2px solid {RED if i == 0 else "transparent"}">{t}</div>' for i, t in enumerate(['Top Critics', 'All', 'Fresh', 'Rotten'])), 24, 'flex-end')
    items = ''
    for c in [CRIT[0], CRIT[1], CRIT[2], CRIT[4], CRIT[3]]:
        sc = T(c['score'], 14, 16, 700, INK, nw=True) if c['score'] else ''
        items += f'''<div data-name="Review · {c['pub']}" class="col" style="gap:10px;padding:20px 0;border-bottom:1px solid {G15}">
  {row(row(tomato(c['fresh'], 18) + T(c['pub'], 15, 18, 700, INK, nw=True) + (top_tag(True) if c['top'] else ''), 8) + sc, 0, justify='space-between')}
  {T('“' + c['q'] + '”', 17, 26, 400, INK2, w=536)}
  {row(T(f"{c['name']} · {c['date']}", 13, 16, 400, G6, nw=True) + full_review(size=13), 0, justify='space-between')}</div>'''
    panel = f'''<div data-name="Drawer · Critics reviews" class="col" style="position:absolute;right:0;top:0;width:600px;height:900px;background:{SURF};box-shadow:-24px 0 60px rgba(0,0,0,.35)">
  <div class="col" style="padding:24px 32px 0;gap:18px;border-bottom:1px solid {G15}">
    {row(col(T('Critics Reviews', 26, 30, 700, INK, nw=True) + row(I('certified-large', 18) + T(f'{TOMATO}% Tomatometer', 14, 16, 700, INK, nw=True) + T(f'· {TOMATO_REVIEWS} reviews', 14, 16, 400, G6, nw=True), 6), 8) + icon_btn('x', 40), 0, 'flex-start', 'space-between')}
    {tabs}</div>
  <div class="col" style="padding:0 32px;flex:1;overflow:hidden">{items}</div>
  <div class="row" style="height:64px;padding:0 32px;align-items:center;justify-content:space-between;border-top:1px solid {G15};background:{SURF}">{T('Top Critics · newest first', 14, 16, 400, G6, nw=True)}{full_review('Open full page', INK, 14)}</div>
</div>'''
    return overlay('Critics reviews · Drawer', 'critics', panel)


# ---------------------------------------------------------------- 03 · editorial
def excerpt(c, w):
    sc = T(c['score'], 14, 16, 700, INK, nw=True) if c['score'] else ''
    top = T('·', 12, 14, 700, G6, nw=True) + label('Top critic', ARED) if c['top'] else ''
    return f'''<div data-name="Excerpt · {c['pub']}" class="col" style="width:{w}px;gap:14px">
  {row(label(c['pub'], INK) + top, 8)}
  {T('“' + c['q'] + '”', 19, 28, 400, INK2, w=w)}
  {row(T('— ' + c['name'], 14, 20, 700, INK, nw=True) + T(c['date'], 14, 20, 400, G6, nw=True), 8)}
  {row(row(tomato(c['fresh'], 16) + sc, 8) + full_review(color=G7), 0, justify='space-between', extra=f'width:{w}px')}</div>'''


def columns(items, w=341, gutter=48):
    out = ''
    for i, c in enumerate(items):
        if i: out += f'<div style="width:{gutter // 2 - 1}px;flex:none"></div>{vrule()}<div style="width:{gutter // 2}px;flex:none"></div>'
        out += excerpt(c, w)
    return row(out, 0, 'stretch')


def c3():
    lead = CRIT[0]
    jan = [c for c in BY_DATE if c['date'].startswith('Jan') and c is not lead]
    later = [c for c in BY_DATE if not c['date'].startswith('Jan')]
    lead_html = f'''<div data-name="Lead" class="row" style="gap:48px;align-items:flex-start;width:1120px">
  <div class="col" style="width:730px;gap:18px">{row(label(lead['pub'], INK) + T('·', 12, 14, 700, G6, nw=True) + label('Top critic', ARED), 8)}
    <div style="position:relative;width:64px;height:32px;overflow:hidden"><div class="nw" style="{FONT}position:absolute;left:-3px;top:-15px;font-size:120px;line-height:120px;font-weight:700;color:{RED}">“</div></div>
    {T(lead['q'], 40, 48, 700, INK, 'letter-spacing:-0.6px', w=730)}
    {row(T('— ' + lead['name'], 16, 24, 700, INK, nw=True) + T(lead['date'], 16, 24, 400, G6, nw=True) + vrule() + row(tomato(True, 18) + T(lead['score'], 16, 18, 700, INK, nw=True), 8) + vrule() + full_review(), 16)}</div>
  <div class="col" style="width:342px;gap:16px;padding-top:4px">{label('The verdict', G6)}{row(I('certified-large', 40) + T(f'{TOMATO}%', 48, 46, 700, INK, 'letter-spacing:-1px', nw=True), 12)}
    {T(f'{FRESH} of {TOMATO_REVIEWS} critics recommend it. Average {CRITIC_AVG}.', 16, 24, 400, INK2, w=342)}{split_bar(342, 6)}
    {T('<b>Consensus:</b> La La Land ' + CONSENSUS, 15, 23, 400, G7, w=342)}</div></div>'''

    def month(title, count):
        return row(T(title, 24, 28, 700, INK, nw=True) + T(count, 15, 18, 400, G6, nw=True), 0, 'flex-end', 'space-between', 'width:1120px')
    body = col(
        rule(INK, 3) + '<div style="height:36px"></div>' + lead_html + '<div style="height:48px"></div>'
        + month('January 2017', 'Opening month · 6 of 9 shown') + rule(INK, 2, 'margin-top:12px') + '<div style="height:28px"></div>'
        + columns(jan[:3]) + '<div style="height:28px"></div>' + rule() + '<div style="height:28px"></div>' + columns(jan[3:6])
        + '<div style="height:56px"></div>' + month('Later in 2017', 'Including the dissent') + rule(INK, 2, 'margin-top:12px') + '<div style="height:28px"></div>'
        + columns(later[:3]), 0, 'width:1120px;padding-bottom:80px')
    mast = col(label('Reviews · Critics', ARED) + T('What the critics said', 64, 64, 700, INK, 'letter-spacing:-2px', nw=True)
               + row(T(f'{TOMATO_REVIEWS} reviews · Certified Fresh', 17, 24, 400, G7, nw=True) + row(chip('All', True) + chip('Top critics') + chip('Fresh') + chip('Rotten'), 8), 0, 'center', 'space-between', 'width:1120px'), 14, 'width:1120px;padding:48px 0 28px')
    return screen('Critics reviews · Editorial', header_light() + film_bar('Reviews', TABS) + mast + body, bg=BG)


# ---------------------------------------------------------------- 04 · table
def c4():
    def tile(k, v, sub, icon=None):
        ic = I(icon, 28) if icon else ''
        return f'<div class="col" style="flex:1;padding:18px 20px;border-radius:12px;background:{SURF};gap:8px">{label(k, G6, 11, 14, 1.4)}{row(ic + T(v, 30, 32, 700, INK, "letter-spacing:-0.5px", nw=True), 8)}{T(sub, 13, 16, 400, G6, nw=True)}</div>'
    tiles = row(tile('Tomatometer', f'{TOMATO}%', 'Certified Fresh', 'certified-large') + tile('Fresh', str(FRESH), 'positive reviews', 'fresh') + tile('Rotten', str(ROTTEN), 'negative reviews', 'rotten')
                + tile('Average', CRITIC_AVG, 'across all critics') + tile('Reviews', TOMATO_REVIEWS, 'approved critics'), 12, 'stretch', extra='width:1120px')
    COLS = [('', 44), ('Critic', 250), ('Score', 76), ('Date', 116), ('Excerpt', 560), ('', 74)]
    head = row(''.join(f'<div style="width:{w}px;flex:none">{row(label(h, G6, 11, 14, 1.2) + (I("chevron-down", 14, INK, 2.2) if h == "Date" else ""), 4)}</div>' for h, w in COLS), 0, extra=f'height:44px;padding:0 20px;border-bottom:1px solid {G2}')
    rows_ = ''
    for i, c in enumerate(BY_DATE[::-1]):
        cells = [
            tomato(c['fresh'], 20),
            col(row(T(c['name'], 15, 18, 700, INK, nw=True) + (top_tag(True) if c['top'] else ''), 8) + T(c['pub'], 13, 16, 400, G6, nw=True), 3),
            T(c['score'] or '—', 15, 18, 700 if c['score'] else 400, INK if c['score'] else G3, nw=True),
            T(c['date'], 14, 18, 400, G7, nw=True),
            T('“' + c['q'] + '”', 14, 20, 400, INK2, 'display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden', w=540),
            row(T('Read', 14, 16, 700, INK, nw=True) + I('arrow-up-right', 14, INK, 2), 4),
        ]
        rows_ += row(''.join(f'<div style="width:{w}px;flex:none">{cell}</div>' for (h, w), cell in zip(COLS, cells)), 0, extra=f'height:72px;padding:0 20px;border-bottom:1px solid {G15};{"background:#FAFAFA;" if i % 2 else ""}')
    table = col(head + rows_, 0, f'width:1120px;border-radius:16px;background:{SURF};overflow:hidden', 'Review table')
    pager = row(T(f'1–9 of {TOMATO_REVIEWS}', 14, 16, 400, G6, nw=True) + row(''.join(f'<div class="nw" style="{FONT}width:36px;height:36px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;{"background:#000;color:#fff" if p == "1" else "color:#000"}">{p}</div>' for p in ['1', '2', '3', '…', '53']) + icon_btn('chevron-right', 36), 4), 0, 'center', 'space-between', 'width:1120px')
    toolbar = row(row(search('Search critics or outlets', 300, 40) + chip('All', True) + chip('Top critics') + chip('Fresh') + chip('Rotten'), 8) + row(btn('Columns', 'secondary', 'sliders', 40) + btn('Export', 'secondary', 'arrow-up-right', 40), 8), 0, 'center', 'space-between', 'width:1120px')
    title = page_title('Reviews · Research view', 'All critic reviews', 'Every review in one sortable table.', segmented(['Cards', 'Table'], 1, G15))
    return screen('Critics reviews · Table', header_light() + film_bar('Reviews', TABS) + '<div style="height:40px"></div>' + title + '<div style="height:24px"></div>'
                  + tiles + '<div style="height:24px"></div>' + toolbar + '<div style="height:16px"></div>' + table + '<div style="height:20px"></div>' + pager + '<div style="height:80px"></div>')


# ---------------------------------------------------------------- 05 · reader modal
def c5():
    sel = 1
    lst = ''
    for i, c in enumerate(BY_DATE[::-1][:8]):
        on = c is CRIT[sel]
        lst += f'''<div data-name="Item · {c['pub']}" class="row" style="gap:12px;align-items:flex-start;padding:14px 20px 14px {17 if on else 20}px;border-bottom:1px solid {G15};{"background:" + BG + ";border-left:3px solid " + RED if on else ""}">
  {tomato(c['fresh'], 18)}{col(row(T(c['pub'], 15, 18, 700, INK, nw=True) + (top_tag(True) if c['top'] else ''), 8) + T(f"{c['name']} · {c['date']}", 13, 16, 400, G6, nw=True), 4)}</div>'''
    c = CRIT[sel]
    reader = f'''<div data-name="Reading pane" class="col" style="flex:1;padding:44px 56px 0;gap:22px">
  {row(outlet(c['pub'], 14) + (top_tag() if c['top'] else ''), 10)}
  <div style="position:relative;width:64px;height:32px;overflow:hidden"><div class="nw" style="{FONT}position:absolute;left:-3px;top:-15px;font-size:120px;line-height:120px;font-weight:700;color:{RED}">“</div></div>
  {T(c['q'], 34, 44, 700, INK, 'letter-spacing:-0.4px', w=620)}
  {row(avatar(initials(c['name']), 44, TINT) + col(T(c['name'], 16, 20, 700, INK, nw=True) + T(f"{c['pub']} · {c['date']}", 14, 18, 400, G6, nw=True), 4) + vrule() + row(tomato(c['fresh'], 22) + T('Fresh', 15, 18, 700, INK, nw=True), 8), 16)}
  <div style="height:6px"></div>{row(btn('Read the full review at NPR', 'dark', 'arrow-up-right', 44) + btn('Share', 'secondary', 'share', 44), 10)}</div>'''
    foot = row(row(I('arrow-right', 16, G6, 2, ) .replace('<svg', '<svg style="transform:rotate(180deg)"') + T('Previous', 14, 16, 700, G7, nw=True), 6) + T(f'2 of {TOMATO_REVIEWS}', 14, 16, 400, G6, nw=True) + row(T('Next', 14, 16, 700, INK, nw=True) + I('arrow-right', 16, INK, 2), 6), 0, 'center', 'space-between', f'height:60px;padding:0 56px;border-top:1px solid {G15}')
    modal = f'''<div data-name="Modal · Critics reader" class="col" style="position:absolute;left:100px;top:60px;width:1240px;height:780px;border-radius:20px;background:{SURF};overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.45)">
  {row(row(T('Critics Reviews', 22, 26, 700, INK, nw=True) + row(I('certified-large', 18) + T(f'{TOMATO}% · {TOMATO_REVIEWS} reviews', 14, 16, 700, G7, nw=True), 6), 16) + row(segmented(['Top Critics', 'All', 'Fresh', 'Rotten'], 1, BG) + icon_btn('x', 40), 16), 0, 'center', 'space-between', f'height:72px;padding:0 24px;border-bottom:1px solid {G15}')}
  <div class="row" style="flex:1;align-items:stretch;overflow:hidden"><div data-name="List" class="col" style="width:380px;border-right:1px solid {G15};overflow:hidden">{lst}</div>
    <div class="col" style="flex:1;justify-content:space-between">{reader}{foot}</div></div></div>'''
    return overlay('Critics reviews · Reader modal', 'critics', modal, 0.62)


VARIANTS = [
    (c1, 'Full page', 'Ledger', 'A dedicated reviews page. A sticky summary on the left (score, Fresh/Rotten split, consensus, filters); readable cards on the right.',
     'Best default: the score stays in view while reading, filters sit where the eye starts, and the page can be linked and shared.'),
    (c2, 'Drawer', 'Quick read', 'A light drawer slides over the film page. Top Critics first, compact entries, a link to the full page at the bottom.',
     'For people checking a few opinions before deciding to watch. No navigation, the film page stays one click away.'),
    (c3, 'Full page', 'Press room', 'Continues the page’s pull-quote language on light newsprint: a lead quote with the verdict beside it, then ruled columns grouped by month.',
     'Turns 472 reviews into a story of the reception. Strongest editorial identity; less efficient for scanning everything.'),
    (c4, 'Full page', 'Research view', 'Stat tiles over a sortable table: verdict, critic, score, date, two-line excerpt. Search, filters, columns, export.',
     'For power users, journalists and critics. Highest density; quotes are clipped, so it pairs with the card view toggle.'),
    (c5, 'Modal', 'Reader', 'A large modal with a list on the left and one review at a time on the right, with previous / next.',
     'Focused reading of whole quotes with clear outbound links. Good for Top Critics; heavier than a drawer for quick checks.'),
]
