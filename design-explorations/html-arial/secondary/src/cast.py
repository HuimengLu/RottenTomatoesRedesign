"""Cast & Crew: five presentations."""
from base import *

TABS = ['Overview', 'Where to Watch', 'Reviews', 'Cast', 'Media', 'More']


def portrait(imgname, name, w, h, r=12):
    if imgname:
        return img(imgname, w, h, r, 0.5, 0.25)
    return (f'<div data-name="No photo" style="width:{w}px;height:{h}px;border-radius:{r}px;background:{G15};display:flex;align-items:center;justify-content:center;flex:none">'
            f'{T(initials(name), round(w * .22), round(w * .22), 700, G6, nw=True)}</div>')


def person_card(imgname, name, role, w=208):
    return col(portrait(imgname, name, w, round(w * 4 / 3)) + col(T(name, 16, 20, 700, INK, nw=True) + T(role, 14, 18, 400, G6, nw=True), 4), 12, f'width:{w}px', f'Person · {name}')


# ---------------------------------------------------------------- 01 · full page
def p1():
    director = f'''<div data-name="Director" class="row" style="width:1120px;padding:24px;border-radius:16px;background:{SURF};gap:24px;align-items:center">
  {img('cast_203', 120, 150, 12, 0.5, 0.25)}
  {col(label('Director & screenwriter', G6) + T('Damien Chazelle', 34, 38, 700, INK, 'letter-spacing:-.4px', nw=True) + T('Writer-director of Whiplash and La La Land.', 16, 24, 400, G7, nw=True), 8)}</div>'''
    cast_grid = row(''.join(person_card(i, n, r) for i, n, r in CAST_FULL), 20, 'flex-start', extra='flex-wrap:wrap;width:1120px;row-gap:28px')
    crew_cols = [CREW[2:5], CREW[5:8], CREW[8:] + CREW[1:2]]
    crew = row(''.join(col(''.join(col(label(r, G6, 11, 14, 1.4) + col(''.join(T(n, 16, 22, 700, INK, nw=True) for n in names), 2), 8, f'padding:16px 0;border-top:1px solid {G2}') for r, names in grp), 0, 'width:357px') for grp in crew_cols), 24, 'flex-start', extra='width:1120px')

    def head(t, c):
        return row(row(T(t, 24, 28, 700, INK, nw=True) + T(c, 15, 18, 400, G6, nw=True), 10, 'baseline'), 0, extra='width:1120px')
    body = col(director + head('Cast', '') + cast_grid + head('Crew', '') + crew, 28, 'width:1120px;padding-bottom:80px')
    title = page_title('Cast & Crew', 'Cast & Crew', '66 people', search('Search cast and crew', 300, 40))
    return screen('Cast & crew · Full page', header_light() + film_bar('Cast', TABS) + '<div style="height:40px"></div>' + title + '<div style="height:28px"></div>' + body)


# ---------------------------------------------------------------- 02 · drawer
def p2():
    def prow(imgname, name, role):
        av = img(imgname, 52, 52, 26, 0.5, 0.22) if imgname else avatar(initials(name), 52, G15, G6)
        return row(row(av + col(T(name, 16, 20, 700, INK, nw=True) + T(role, 14, 18, 400, G6, nw=True), 3), 14) + I('chevron-right', 18, G3, 2), 0, 'center', 'space-between', f'padding:12px 0;border-bottom:1px solid {G15}')
    starring = ''.join(prow(i, n, r) for i, n, r in CAST_FULL[:2])
    supporting = ''.join(prow(i, n, r) for i, n, r in CAST_FULL[2:8])
    panel = f'''<div data-name="Drawer · Cast &amp; crew" class="col" style="position:absolute;right:0;top:0;width:520px;height:900px;background:{SURF};box-shadow:-24px 0 60px rgba(0,0,0,.35)">
  <div class="col" style="padding:24px 32px 18px;gap:16px;border-bottom:1px solid {G15}">
    {row(T('Cast &amp; Crew', 26, 30, 700, INK, nw=True) + icon_btn('x', 40), 0, 'center', 'space-between')}
    {search('Search 66 people', 456, 40)}{segmented(['Cast', 'Crew'], 0, BG)}</div>
  <div class="col" style="padding:8px 32px 0;overflow:hidden;flex:1">
    {label('Starring', G6, 11, 14, 1.4).replace('<div', '<div style="padding:14px 0 2px" ', 1) if False else T('STARRING', 11, 14, 700, G6, 'letter-spacing:1.4px;padding:14px 0 2px', nw=True)}{starring}
    {T('SUPPORTING', 11, 14, 700, G6, 'letter-spacing:1.4px;padding:22px 0 2px', nw=True)}{supporting}</div></div>'''
    return overlay('Cast & crew · Drawer', 'cast', panel)


# ---------------------------------------------------------------- 03 · end credits
def leaders(pairs, w=720):
    out = ''
    for a, b in pairs:
        out += (f'<div class="row" style="width:{w}px;align-items:baseline;gap:10px">{T(a, 17, 30, 400, G7, nw=True)}'
                f'<div style="flex:1;border-bottom:2px dotted {G3};transform:translateY(-6px)"></div>{T(b, 17, 30, 700, INK, nw=True)}</div>')
    return col(out, 2, f'width:{w}px')


def p3():
    def block(lbl, names, size=34):
        return col(label(lbl, G6, 12, 14, 2.4) + col(''.join(T(n, size, size + 6, 700, INK, 'letter-spacing:-.3px;text-align:center', nw=True) for n in names), 4, align='center'), 12, align='center')
    credits = col(
        T('LA LA LAND', 14, 16, 700, RED, 'letter-spacing:6px', nw=True)
        + block('Written and directed by', ['Damien Chazelle'], 44)
        + block('Starring', ['Ryan Gosling', 'Emma Stone'], 40)
        + block('With', ['John Legend', 'Rosemarie DeWitt', 'J.K. Simmons'], 24)
        + rule(G2, 1, 'width:120px;align-self:center')
        + col(label('Cast', G6, 12, 14, 2.4) + leaders([(r, n) for _, n, r in CAST_FULL]), 18, align='center')
        + rule(G2, 1, 'width:120px;align-self:center')
        + col(label('Crew', G6, 12, 14, 2.4) + leaders([(r, ', '.join(ns)) for r, ns in CREW[2:]]), 18, align='center')
        + T('Lionsgate · Summit Entertainment · Gilbert Films · Marc Platt Productions', 14, 20, 400, G6, nw=True),
        48, 'width:1440px;padding:72px 0 96px', align='center')
    bar = film_bar('Cast', TABS)
    return screen('Cast & crew · End credits', header_light() + bar + credits, bg=SURF)


# ---------------------------------------------------------------- 04 · person modal
def p4():
    known = [('Easy A', '2010'), ('Birdman', '2014'), ('The Favourite', '2018'), ('Poor Things', '2023')]
    films = row(''.join(col(f'<div style="width:118px;height:64px;border-radius:8px;background:{BG};display:flex;align-items:center;justify-content:center">{I("film", 22, G3, 1.6)}</div>'
                            + T(t, 14, 18, 700, INK, nw=True) + T(y, 13, 16, 400, G6, nw=True), 6, 'width:118px') for t, y in known), 16, 'flex-start')
    strip = row(''.join(f'<div style="border-radius:24px;padding:2px;{"border:2px solid #000" if n == "Emma Stone" else "border:2px solid transparent"}">{img(i, 40, 40, 20, 0.5, 0.22) if i else avatar(initials(n), 40, G15, G6)}</div>' for i, n, r in CAST_FULL[:8]), 2)
    info = col(row(label('Cast · 2 of 66', G6) + row(icon_btn('chevron-left', 36) + icon_btn('chevron-right', 36) + icon_btn('x', 36), 8), 0, 'center', 'space-between')
               + col(T('Emma Stone', 48, 50, 700, INK, 'letter-spacing:-1.2px', nw=True) + T('as Mia', 20, 26, 400, G7, nw=True), 6)
               + row(I('award', 22, AMBER, 1.8) + T('Academy Award, Best Actress, for <i>La La Land</i>', 16, 20, 700, INK, nw=True), 10, extra=f'padding:12px 14px;border-radius:10px;background:#FFF7E0;align-self:flex-start')
               + col(label('Known for', G6) + films, 12)
               + row(btn('View full profile', 'dark', 'arrow-right', 44), 10)
               + rule(G15) + col(label('More cast', G6) + strip, 10), 22, 'flex:1;padding:28px 32px')
    modal = f'''<div data-name="Modal · Person" class="row" style="position:absolute;left:200px;top:110px;width:1040px;height:680px;border-radius:20px;background:{SURF};overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.45)">
  {img('cast_445', 400, 680, 0, 0.5, 0.25)}{info}</div>'''
    return overlay('Cast & crew · Person modal', 'cast', modal, 0.62)


# ---------------------------------------------------------------- 05 · character map
def p5():
    W, H = 1120, 660
    nodes = {  # key: (x, y, w, h, img, actor, character, relation, main)
        'mia': (160, 250, 320, 156, 'cast_445', 'Emma Stone', 'Mia', 'An aspiring actress working as a barista', True),
        'seb': (640, 250, 320, 156, 'cast_324', 'Ryan Gosling', 'Sebastian', 'A jazz pianist with dreams of his own club', True),
        'greg': (0, 40, 270, 100, None, 'Finn Wittrock', 'Greg', 'Mia’s boyfriend when the story begins', False),
        'room': (0, 520, 330, 100, None, 'Callie Hernandez · Jessica Rothe · Sonoya Mizuno', 'Tracy, Alexis, Caitlin', 'Mia’s roommates', False),
        'keith': (850, 40, 270, 100, 'cast_566', 'John Legend', 'Keith', 'Old classmate who invites him into his band', False),
        'boss': (430, 40, 270, 100, 'cast_808', 'J.K. Simmons', 'Boss', 'Owns the restaurant where Sebastian plays', False),
        'laura': (850, 520, 270, 100, 'cast_687', 'Rosemarie DeWitt', 'Laura', 'Sebastian’s sister', False),
    }
    links = [('mia', 'seb', 'Meet in Los Angeles'), ('greg', 'mia', ''), ('room', 'mia', ''), ('keith', 'seb', ''), ('boss', 'seb', ''), ('laura', 'seb', '')]

    def center(k):
        x, y, w, h = nodes[k][:4]
        return x + w / 2, y + h / 2
    lines = ''
    for a, b, lab in links:
        (x1, y1), (x2, y2) = center(a), center(b)
        lines += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{G3 if lab == "" else RED}" stroke-width="{1.5 if lab == "" else 2}" stroke-dasharray="{"5 5" if lab == "" else "none"}"/>'
    svg = f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute;left:0;top:0">{lines}</svg>'
    cards = ''
    for k, (x, y, w, h, im, actor, ch, rel, main) in nodes.items():
        ph = img(im, 96 if main else 64, 124 if main else 76, 10, 0.5, 0.22) if im else (
            '<div class="row" style="gap:0">' + ''.join(avatar(initials(n.strip()), 40, G15, G6).replace('flex:none', f'flex:none;margin-left:{-10 if j else 0}px;border:2px solid #fff') for j, n in enumerate(actor.split('·'))) + '</div>'
            if '·' in actor else portrait(None, actor, 64, 76, 10))
        cards += (f'<div data-name="Character · {ch}" class="row" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;padding:{14 if main else 12}px;gap:14px;align-items:center;'
                  f'border-radius:14px;background:{SURF};{"border:2px solid " + INK if main else "border:1px solid " + G2}">'
                  f'{ph}{col(T(ch, 22 if main else 16, 26 if main else 20, 700, INK, nw=True) + T(actor if "·" not in actor else "Three actors", 14 if main else 13, 18, 700 if main else 400, G7, nw=True) + T(rel, 14 if main else 13, 19, 400, G6, w=w - (96 if main else 64) - 50), 4)}</div>')
    (x1, y1), (x2, y2) = center('mia'), center('seb')
    pill = f'<div class="nw" style="{FONT}position:absolute;left:{(x1 + x2) / 2 - 80}px;top:{y1 - 15}px;width:160px;text-align:center;font-size:13px;line-height:16px;font-weight:700;color:{ARED};padding:7px 0;border-radius:15px;background:{TOPBG}">Meet in Los Angeles</div>'
    canvas = f'<div data-name="Character map" style="position:relative;width:{W}px;height:{H}px;flex:none">{svg}{cards}{pill}</div>'
    legend = row(row(f'<div style="width:28px;height:0;border-top:2px solid {RED}"></div>' + T('Central story', 13, 16, 400, G6, nw=True), 8) + row(f'<div style="width:28px;height:0;border-top:2px dashed {G3}"></div>' + T('Connected to', 13, 16, 400, G6, nw=True), 8)
                 + row(I('info', 15, G6, 1.8) + T('Spoiler-free: covers the first act only', 13, 16, 400, G6, nw=True), 6), 24, extra='width:1120px')
    title = page_title('Cast & Crew', 'Who’s who', 'The people around Mia and Sebastian', segmented(['Map', 'Grid', 'Credits'], 0, G15))
    return screen('Cast & crew · Character map', header_light() + film_bar('Cast', TABS) + '<div style="height:40px"></div>' + title + '<div style="height:28px"></div>'
                  + legend + '<div style="height:28px"></div>' + canvas + '<div style="height:80px"></div>')


VARIANTS = [
    (p1, 'Full page', 'Directory', 'The director up top, a photo grid of the cast with characters, and the crew grouped by department.',
     'The complete, searchable record. People without a photo get a neutral initials tile instead of a stock silhouette.'),
    (p2, 'Drawer', 'Quick list', 'A drawer with search and a Cast / Crew switch: starring first, then supporting, one tap into a person.',
     'Fast lookup of “who played…?” without leaving the trailer or reviews. Scales to all 66 names.'),
    (p3, 'Full page', 'End credits', 'The film’s own language: centred credits with dotted leaders, character to actor, department to crew.',
     'Distinctive and calm on white; the most cinematic option. Photos are left out on purpose, so it pairs with a grid toggle.'),
    (p4, 'Modal', 'Person', 'Selecting anyone opens a modal over the page: portrait, character, the La La Land award, known-for titles, and a strip to move between cast.',
     'Answers the follow-up question (“what else were they in?”) in place. Known-for titles are real; scores omitted until wired to data.'),
    (p5, 'Full page', 'Who’s who', 'A spoiler-free character map: Mia and Sebastian at the centre, the people around each of them, and how they connect.',
     'Helps first-time viewers; unique to story-driven titles. Needs editorial input per film, so treat it as a feature for big releases.'),
]
