"""Videos & Photos: five presentations."""
from base import *
from PIL import Image as _Im

TABS = ['Overview', 'Where to Watch', 'Reviews', 'Cast', 'Media', 'More']
TRAILERS = [v for v in VIDEOS if v[3] in ('Trailer', 'TV Spot')]
CLIPS = [v for v in VIDEOS if v[3] == 'Clip']
FEATS = [v for v in VIDEOS if v[3] == 'Featurette']


def aspect(name):
    p = os.path.join(ROOT, 'assets', 'hi', name + '.jpg')
    w, h = _Im.open(p).size
    return w / h


def duration(d, size=12):
    return f'<div class="nw" style="{FONT}position:absolute;right:8px;bottom:8px;font-size:{size}px;line-height:14px;font-weight:700;color:#fff;padding:4px 7px;border-radius:5px;background:rgba(0,0,0,.72)">{d}</div>'


def kind_tag(k):
    return f'<div class="nw" style="{FONT}position:absolute;left:8px;top:8px;font-size:11px;line-height:12px;font-weight:700;letter-spacing:.6px;text-transform:uppercase;color:#2A1A00;padding:4px 7px;border-radius:5px;background:#F0A400">{k}</div>'


def play_btn(size=56):
    return (f'<div style="position:absolute;left:50%;top:50%;margin:-{size // 2}px 0 0 -{size // 2}px;width:{size}px;height:{size}px;border-radius:{size // 2}px;border:2px solid #fff;background:rgba(0,0,0,.28);'
            f'display:flex;align-items:center;justify-content:center;padding-left:{size // 14}px">{I("play", round(size * .42), "#fff")}</div>')


def thumb(v, w, h, r=10, tag=True, play=False):
    name, title, d, k = v
    return (f'<div data-name="Thumb · {title}" style="position:relative;width:{w}px;height:{h}px;flex:none;border-radius:{r}px;overflow:hidden">{img(name, w, h, 0)}'
            f'{kind_tag(k) if tag else ""}{duration(d)}{play_btn(min(56, h // 3)) if play else ""}</div>')


def video_card(v, w=262):
    h = round(w * 9 / 16)
    return col(thumb(v, w, h) + T(v[1], 15, 20, 700, INK, 'display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden', w=w) + T(f'{v[3]} · {v[2]}', 13, 16, 400, G6, nw=True), 8, f'width:{w}px', f'Video · {v[1]}')


def player(v, w, h, t='0:42', frac=0.33, playing=True):
    name, title, d, k = v
    ctl = I('pause-fill' if playing else 'play', 18, '#fff')
    return f'''<div data-name="Player" style="position:relative;width:{w}px;height:{h}px;flex:none;border-radius:14px;overflow:hidden;background:#000">{img(name, w, h, 0)}
  <div style="position:absolute;left:0;right:0;bottom:0;height:120px;background:linear-gradient(rgba(0,0,0,0),rgba(0,0,0,.72))"></div>
  {"" if playing else play_btn(72)}
  <div class="col" style="position:absolute;left:20px;right:20px;bottom:16px;gap:12px">
    <div style="height:4px;border-radius:2px;background:rgba(255,255,255,.3)"><div style="width:{round((w - 40) * frac)}px;height:4px;border-radius:2px;background:{RED}"></div></div>
    {row(row(ctl + I('volume-x', 18, '#fff', 2) + T(f'{t} / {d}', 13, 16, 700, '#fff', nw=True), 16) + row(I('cc', 18, '#fff', 2) + I('maximize', 18, '#fff', 2), 16), 0, justify='space-between')}</div></div>'''


def upnext(items, w, tw=128, current=None):
    out = ''
    for v in items:
        on = v is current
        out += row(thumb(v, tw, round(tw * 9 / 16), 8, tag=False) + col(T(v[1], 14, 19, 700, INK, 'display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden', w=w - tw - 14 - 16)
                   + T(('Now playing · ' if on else '') + f'{v[3]} · {v[2]}', 13, 16, 700 if on else 400, ARED if on else G6, nw=True), 4), 14, 'flex-start',
                   extra=f'padding:8px;border-radius:10px;{"background:" + BG if on else ""}')
    return out


def section(title, items, total=None):
    head = row(row(T(title, 24, 28, 700, INK, nw=True) + T(str(total or len(items)), 15, 18, 400, G6, nw=True), 10, 'baseline') + row(T('See all', 14, 16, 700, INK, nw=True) + I('chevron-right', 16, INK, 2), 4), 0, 'center', 'space-between', 'width:1120px')
    return col(head + row(''.join(video_card(v) for v in items[:4]), 24, 'flex-start'), 16, 'width:1120px', title)


# ---------------------------------------------------------------- 01 · media hub
def m1():
    cur = VIDEOS[0]
    feat = row(col(player(cur, 736, 414, '0:00', 0.0, False) + row(col(T(cur[1], 24, 28, 700, INK, nw=True) + T(f'{cur[3]} · {cur[2]} · Lionsgate', 14, 18, 400, G6, nw=True), 6) + row(btn('Share', 'secondary', 'share', 40), 8), 0, 'flex-end', 'space-between', 'width:736px'), 16)
               + col(label('Up next', G6) + upnext(VIDEOS[1:5], 360), 8, f'width:360px;padding:16px 8px;border-radius:16px;background:{SURF}'), 24, 'flex-start', extra='width:1120px', name='Featured')
    body = col(feat + '<div style="height:24px"></div>' + section('Trailers & TV spots', TRAILERS) + section('Clips', CLIPS) + section('Featurettes', FEATS), 40, 'width:1120px;padding-bottom:80px')
    title = page_title('Media', 'Videos & Photos', '2,122 videos and photos', segmented(['Videos', 'Photos'], 0, G15))
    return screen('Videos & photos · Media hub', header_light() + film_bar('Media', TABS) + '<div style="height:40px"></div>' + title + '<div style="height:28px"></div>' + body)


# ---------------------------------------------------------------- 02 · theater modal
def m2():
    cur = VIDEOS[0]
    left = col(player(cur, 852, 479, '0:42', 0.33, True) + row(col(T(cur[1], 22, 26, 700, INK, nw=True) + T(f'{cur[3]} · {cur[2]}', 14, 18, 400, G6, nw=True), 6)
               + row(btn('Copy link', 'secondary', 'external', 40) + btn('Share', 'secondary', 'share', 40), 8), 0, 'center', 'space-between', 'width:852px'), 18, 'width:852px')
    right = col(row(T('Up next', 17, 20, 700, INK, nw=True) + T('Autoplay on', 13, 16, 400, G6, nw=True), 0, justify='space-between', extra='padding:0 8px')
                + upnext(VIDEOS[:7], 316, 120, current=cur), 6, 'width:316px;overflow:hidden')
    modal = f'''<div data-name="Modal · Theater" class="col" style="position:absolute;left:100px;top:56px;width:1240px;height:788px;border-radius:20px;background:{SURF};overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.45)">
  {row(row(T('Videos & Photos', 22, 26, 700, INK, nw=True) + segmented(['Videos', 'Photos'], 0, BG), 16) + icon_btn('x', 40), 0, 'center', 'space-between', f'height:72px;padding:0 24px;border-bottom:1px solid {G15}')}
  <div class="row" style="gap:24px;padding:24px;align-items:flex-start">{left}{right}</div></div>'''
    return overlay('Videos & photos · Theater modal', 'media', modal, 0.66)


# ---------------------------------------------------------------- 03 · justified photo grid
def justified(items, width=1120, target=250, gap=8):
    rows_, cur = [], []
    for it in items:
        cur.append(it)
        ar = sum(aspect(n) for n, _ in cur)
        if (width - gap * (len(cur) - 1)) / ar < target:
            rows_.append(cur); cur = []
    if cur: rows_.append(cur)
    out = ''
    for ri, r in enumerate(rows_):
        ar = sum(aspect(n) for n, _ in r)
        h = round((width - gap * (len(r) - 1)) / ar) if ri < len(rows_) - 1 or len(r) > 2 else target
        tiles = ''
        for j, (n, cap_) in enumerate(r):
            w = round(h * aspect(n))
            hover = ri == 0 and j == 1
            ov = ''
            if hover:
                ov = (f'<div style="position:absolute;left:0;right:0;bottom:0;height:96px;background:linear-gradient(rgba(0,0,0,0),rgba(0,0,0,.7))"></div>'
                      f'<div class="row" style="position:absolute;left:14px;right:14px;bottom:12px;justify-content:space-between;align-items:flex-end">{T(cap_, 14, 18, 700, "#fff", nw=True)}{row(icon_btn("maximize", 32, "#000", "#fff", False) + icon_btn("share", 32, "#000", "#fff", False), 6)}</div>')
            tiles += f'<div data-name="Photo · {cap_}" style="position:relative;width:{w}px;height:{h}px;flex:none;border-radius:8px;overflow:hidden">{img(n, w, h, 0)}{ov}</div>'
        out += row(tiles, gap, 'flex-start')
    return col(out, gap, f'width:{width}px', 'Justified grid')


def m3():
    tools = row(row(chip('All', True) + chip('Stills') + chip('Posters'), 8) + row(T('Sort', 14, 16, 400, G6, nw=True) + row(T('Most viewed', 14, 16, 700, INK, nw=True) + I('chevron-down', 16, INK, 2), 6, extra=f'height:36px;padding:0 12px;border-radius:8px;background:{SURF};border:1px solid {G2}'), 10), 0, 'center', 'space-between', 'width:1120px')
    items = [(n, c) for n, c in STILLS]
    title = page_title('Media', 'Photos', '2,122 videos and photos', segmented(['Videos', 'Photos'], 1, G15))
    return screen('Videos & photos · Photo grid', header_light() + film_bar('Media', TABS) + '<div style="height:40px"></div>' + title + '<div style="height:24px"></div>' + tools + '<div style="height:20px"></div>'
                  + justified(items) + '<div style="height:28px"></div>' + btn('Load more photos', 'secondary') + '<div style="height:80px"></div>')


# ---------------------------------------------------------------- 04 · light lightbox
def m4():
    sel = 2
    n, cap_ = STILLS[sel]
    iw, ih = 984, 656
    strip = ''.join(f'<div style="flex:none;border-radius:8px;padding:2px;{"border:2px solid #000" if i == sel else "border:2px solid transparent;opacity:.75"}">{img(m, 88, 58, 5)}</div>' for i, (m, _) in enumerate(STILLS[:12]))
    viewer = f'''<div data-name="Lightbox" class="col" style="width:1440px;height:900px;background:{BG};align-items:center;flex:none">
  {row(row(img('poster_186', 28, 42, 3, 0.5, 0.3) + col(T('La La Land', 16, 18, 700, INK, nw=True) + T('Photos', 13, 16, 400, G6, nw=True), 2), 10)
       + T(f'{sel + 1} / 2,122', 15, 18, 700, INK, nw=True) + row(btn('Share', 'secondary', 'share', 40) + icon_btn('x', 40), 8), 0, 'center', 'space-between', f'width:1440px;height:72px;padding:0 32px;background:{SURF};border-bottom:1px solid {G15}')}
  <div class="row" style="flex:1;width:1440px;align-items:center;justify-content:space-between;padding:0 40px">
    {icon_btn('chevron-left', 52, INK, SURF, True)}
    <div class="col" style="gap:14px;align-items:center">{img(n, iw, ih, 12)}{row(T(cap_ + ' in <i>La La Land</i> (2016)', 15, 20, 400, INK2, nw=True), 0)}</div>
    {icon_btn('chevron-right', 52, INK, SURF, True)}</div>
  {row(strip, 6, extra=f'width:1440px;height:96px;padding:0 32px;justify-content:center;background:{SURF};border-top:1px solid {G15}')}</div>'''
    return viewer


# ---------------------------------------------------------------- 05 · rails
def rail(title, cards, count, w_item, gap=20):
    head = row(row(T(title, 24, 28, 700, INK, nw=True) + T(str(count), 15, 18, 400, G6, nw=True), 10, 'baseline') + row(icon_btn('chevron-left', 36) + icon_btn('chevron-right', 36), 8), 0, 'center', 'space-between', 'width:1120px')
    track = row(cards, gap, 'flex-start', extra='width:1280px;overflow:hidden')
    return col(head + track, 16, 'width:1280px;align-self:flex-start;margin-left:160px', title)


def m5():
    def still_card(n, c, w=340, h=226):
        return col(f'<div style="width:{w}px;height:{h}px;border-radius:10px;overflow:hidden;flex:none">{img(n, w, h, 0)}</div>' + T(c, 14, 18, 400, G7, w=w), 8, f'width:{w}px')
    vids = lambda items: ''.join(video_card(v, 340) for v in items)
    posters = ''.join(col(img(n, 180, 270, 10) + T(c, 14, 18, 400, G7, nw=True), 8) for n, c in [('photo_458', 'Theatrical poster'), ('photo_202', 'Teaser poster'), ('poster_186', 'Key art')])
    stills = ''.join(still_card(n, c) for n, c in STILLS[:6])
    feature = f'''<div data-name="Feature" class="row" style="width:1120px;height:360px;border-radius:20px;overflow:hidden;background:{TINT};align-items:stretch">
  <div style="position:relative;width:640px;height:360px;flex:none">{img('video_3003', 640, 360, 0)}{play_btn(72)}</div>
  {col(label('Featured', 'rgba(255,255,255,.7)') + T('La La Land: Official Trailer', 34, 38, 700, '#fff', 'letter-spacing:-.4px', w=400) + T('Trailer · 2:08', 15, 18, 400, 'rgba(255,255,255,.7)', nw=True) + '<div style="height:10px"></div>' + btn('Play trailer', 'white', 'play', 44), 12, 'padding:40px;justify-content:center;flex:1')}</div>'''
    body = col(feature + rail('Trailers & TV spots', vids(TRAILERS), len(TRAILERS), 300) + rail('Clips', vids(CLIPS), len(CLIPS), 300) + rail('Stills', stills, len(STILLS) - 2, 300)
               + rail('Posters', posters, 3, 180) + rail('Featurettes', vids(FEATS), len(FEATS), 300), 44, 'width:1440px;align-items:center;padding-bottom:80px')
    title = page_title('Media', 'Videos & Photos', 'Browse by type. Every row scrolls sideways.', segmented(['Rows', 'Grid'], 0, G15))
    return screen('Videos & photos · Rails', header_light() + film_bar('Media', TABS) + '<div style="height:40px"></div>' + title + '<div style="height:28px"></div>' + body)


VARIANTS = [
    (m1, 'Full page', 'Media hub', 'A player with Up next, then videos grouped into Trailers & TV spots, Clips and Featurettes. Photos live behind the same toggle.',
     'The most familiar pattern: the newest trailer plays first, groups make 2,122 items navigable. Video titles and running times are RT’s own.'),
    (m2, 'Modal', 'Theater', 'Watch without leaving the film page: a large modal with the player, share actions and an Up next list.',
     'Keeps people on the film page and its Rent button. Chrome is light; only the video itself is dark, as it should be.'),
    (m3, 'Full page', 'Photo grid', 'A justified grid that keeps every photo’s real proportions. Hover shows the caption with expand and share.',
     'Best for browsing stills and posters together; no awkward crops. Filters separate stills, posters and behind the scenes.'),
    (m4, 'Full screen', 'Light lightbox', 'A full-screen viewer on Gray 100: one large image, caption, arrows and a thumbnail strip.',
     'Follows the light-surface brief. Dark lightboxes make photos pop; offer a dark toggle if testing shows people prefer it.'),
    (m5, 'Full page', 'Rails', 'A featured trailer, then one horizontally scrolling row per type: trailers, clips, stills, posters, featurettes.',
     'Shows the breadth of media in one screen and suits touch. Less efficient for finding a specific photo.'),
]
