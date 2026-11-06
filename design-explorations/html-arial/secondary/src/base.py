"""Shared light-theme tokens and components for the secondary screens (Arial · B system, light surfaces for long reading)."""
import os, sys, io, base64
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'ex'))
from PIL import Image
import kit
from kit import icon as I, img_uri as IMG
from arial import full_color_logo
from data import CRITICS, AUDIENCE, CAST, CONSENSUS, TOMATO, TOMATO_REVIEWS, FRESH, ROTTEN, CRITIC_AVG, POP, POP_RATINGS, POP_AVG, PHOTOS, MORE

# ---------------------------------------------------------------- tokens
BG = '#F4F4F4'        # Gray 100: page
SURF = '#FFFFFF'      # cards, panels
INK = '#000000'
INK2 = '#1A1A1A'
G7 = '#4D4D4D'
G6 = '#666666'        # muted text, 5.2:1 on Gray 100
G3 = '#BFBFBF'
G2 = '#D9D9D9'        # rules
G15 = '#E6E6E6'
RED = '#FA320A'       # brand: logo, icons, data bars (no small text)
ARED = '#D42A07'      # filled controls with text, red text on light
GREEN = '#0AC855'
AMBER = '#B37A00'     # stars on light
TINT = '#222646'      # B poster tint: continuity band with the film page
TINT2 = '#1D203C'
TOPBG = '#FFEDE8'
FONT = 'font-family:Arial,Helvetica,sans-serif;'

CSS = """
*{box-sizing:border-box;margin:0;padding:0;border:0 solid #D9D9D9}
img,svg{display:block;max-width:none}
body{font-family:Arial,Helvetica,sans-serif;-webkit-font-smoothing:antialiased;background:#FFFFFF;color:#000}
.row{display:flex;flex-direction:row}
.col{display:flex;flex-direction:column}
.nw{white-space:nowrap}
.cap{display:flex;flex-direction:column;gap:28px;width:1440px}
"""

# ---------------------------------------------------------------- data
CRIT = [dict(name=c[0], pub=c[1], date=c[2], fresh=c[3], score=c[4], q=c[5].replace("'", '’'), top=c[6]) for c in CRITICS]
AUD = [dict(name=a[0], date=a[1], stars=a[2], text=a[3].replace("'", '’'), helpful=h, verified=True)
       for a, h in zip(AUDIENCE, ['1.2K', '856', '431', '310', '214', '198', '120'])]
VIDEOS = [  # titles and running times as listed on the RT page; thumbnails are matching stills
    ('hero_650', 'La La Land: Official Trailer', '2:08', 'Trailer'),
    ('video_1211', 'La La Land: ‘Start a Fire’ Trailer', '1:13', 'Trailer'),
    ('video_3259', 'La La Land: TV Spot - 7 Golden Globe Wins', '0:30', 'TV Spot'),
    ('video_1979', 'Official Clip - Audition (The Fools Who Dream)', '3:34', 'Clip'),
    ('video_2747', 'Official Clip - I’m Not Good Enough', '3:34', 'Clip'),
    ('video_3771', 'Official Clip - I Ran', '3:34', 'Clip'),
    ('video_2235', 'Official Clip - This is Not Your Dream', '3:58', 'Clip'),
    ('video_1723', 'Official Clip - You’re Fired', '3:34', 'Clip'),
    ('video_699', 'La La Land vs Singin’ in the Rain', '21:53', 'Featurette'),
    ('video_4027', 'Top 10 Greatest Movies About Hollywood', '25:06', 'Featurette'),
]
STILLS = [  # (image, caption)
    ('photo_2250', 'Emma Stone and Ryan Gosling'), ('photo_2506', 'Ryan Gosling and Emma Stone'), ('photo_1482', 'John Legend and Ryan Gosling'),
    ('photo_1226', 'Rosemarie DeWitt and Ryan Gosling'), ('photo_714', 'Ryan Gosling and Emma Stone'), ('photo_970', 'Ryan Gosling and Emma Stone'),
    ('photo_1738', 'Ryan Gosling'), ('photo_1994', 'Emma Stone and Ryan Gosling'), ('video_3003', 'Emma Stone and Ryan Gosling'),
    ('video_3259', 'Emma Stone, Callie Hernandez, Jessica Rothe and Sonoya Mizuno'), ('video_2491', 'Opening number on the freeway'),
    ('video_3515', 'Ryan Gosling and Emma Stone'), ('photo_458', 'Theatrical poster'), ('photo_202', 'Teaser poster'),
]
CAST_FULL = [  # (image or None, name, character)
    ('cast_324', 'Ryan Gosling', 'Sebastian'), ('cast_445', 'Emma Stone', 'Mia'), ('cast_566', 'John Legend', 'Keith'),
    ('cast_687', 'Rosemarie DeWitt', 'Laura'), ('cast_808', 'J.K. Simmons', 'Boss'), (None, 'Finn Wittrock', 'Greg'),
    (None, 'Callie Hernandez', 'Tracy'), (None, 'Jessica Rothe', 'Alexis'), (None, 'Sonoya Mizuno', 'Caitlin'), (None, 'Josh Pence', 'Josh'),
]
CREW = [  # (role, [names])
    ('Director', ['Damien Chazelle']), ('Screenwriter', ['Damien Chazelle']),
    ('Producers', ['Fred Berger', 'Jordan Horowitz', 'Marc Platt', 'Gary Gilbert']),
    ('Original Music', ['Justin Hurwitz']), ('Lyrics', ['Benj Pasek', 'Justin Paul']), ('Cinematographer', ['Linus Sandgren']),
    ('Film Editor', ['Tom Cross']), ('Production Design', ['David Wasco']), ('Costume Design', ['Mary Zophres']), ('Choreographer', ['Mandy Moore']),
]
STAR_LABEL = ['', 'Hated it', 'Didn’t like it', 'It was OK', 'Really liked it', 'Loved it']
DIST = [(5, 52), (4, 24), (3, 12), (2, 6), (1, 6)]   # illustrative split consistent with a 4.1 average


def initials(name):
    p = name.replace('.', '').split()
    return (p[0][0] + p[-1][0]).upper()


# ---------------------------------------------------------------- primitives
def T(text, size, lh, weight=400, color=INK, extra='', w=None, nw=False, name=None):
    wd = f'width:{w}px;' if w else ''
    dn = f' data-name="{name}"' if name else ''
    return f'<div{dn} class="{"nw" if nw else ""}" style="{FONT}{wd}font-size:{size}px;line-height:{lh}px;font-weight:{weight};color:{color};{extra}">{text}</div>'


def label(text, color=G6, size=12, lh=14, ls=1.6, name=None):
    return T(text.upper(), size, lh, 700, color, f'letter-spacing:{ls}px', nw=True, name=name)


def row(inner, gap=0, align='center', justify='flex-start', extra='', name=None):
    dn = f' data-name="{name}"' if name else ''
    return f'<div{dn} class="row" style="gap:{gap}px;align-items:{align};justify-content:{justify};{extra}">{inner}</div>'


def col(inner, gap=0, extra='', name=None, align='stretch'):
    dn = f' data-name="{name}"' if name else ''
    return f'<div{dn} class="col" style="gap:{gap}px;align-items:{align};{extra}">{inner}</div>'


def rule(color=G2, h=1, extra=''):
    return f'<div style="height:{h}px;background:{color};flex:none;align-self:stretch;{extra}"></div>'


def vrule(color=G2, extra=''):
    return f'<div style="width:1px;background:{color};flex:none;align-self:stretch;{extra}"></div>'


def img(name, w, h, r=0, fx=0.5, fy=0.5, opts='', extra='', alt=''):
    return f'<img alt="{alt}" src="{IMG(name, w, h, fx, fy, opts)}" style="width:{w}px;height:{h}px;border-radius:{r}px;object-fit:cover;flex:none;{extra}">'


def png_uri(path, w=None, q=80):
    im = Image.open(path).convert('RGB')
    if w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=q)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


# ---------------------------------------------------------------- controls (light)
def chip(text, on=False, count=None, icon=None):
    c = f'<span style="color:{"rgba(255,255,255,.7)" if on else G6};font-weight:400;margin-left:6px">{count}</span>' if count else ''
    ic = I(icon, 16, '#fff' if on else INK, 1.9) if icon else ''
    st = f'background:{INK};color:#fff' if on else f'background:{SURF};color:{INK};border:1px solid {G2}'
    return f'<div data-name="Chip · {text}" class="row nw" style="{FONT}height:36px;padding:0 14px;border-radius:18px;align-items:center;gap:6px;font-size:14px;line-height:16px;font-weight:700;{st}">{ic}{text}{c}</div>'


def segmented(items, active=0, bg=G15):
    t = ''.join(f'<div class="nw" style="{FONT}height:32px;padding:0 14px;border-radius:8px;display:flex;align-items:center;font-size:14px;line-height:16px;font-weight:700;'
                f'{"background:#fff;color:#000;box-shadow:0 1px 2px rgba(0,0,0,.12)" if i == active else "color:" + G6}">{x}</div>' for i, x in enumerate(items))
    return f'<div data-name="Segmented" class="row" style="padding:3px;border-radius:10px;background:{bg};gap:2px;align-self:flex-start">{t}</div>'


def btn(text, kind='primary', icon=None, h=44, w=None):
    pad = 18 if h >= 44 else 14
    if kind == 'primary': st, fg = f'background:{ARED};color:#fff', '#fff'
    elif kind == 'dark': st, fg = f'background:{INK};color:#fff', '#fff'
    elif kind == 'white': st, fg = f'background:#fff;color:{INK}', INK
    else: st, fg = f'background:{SURF};color:{INK};border:1px solid {G2}', INK
    ic = I(icon, 18 if h >= 44 else 16, fg, 2) if icon else ''
    wd = f'width:{w}px;justify-content:center;' if w else ''
    return f'<div data-name="Button · {text}" class="row nw" style="{FONT}{wd}height:{h}px;padding:0 {pad}px;border-radius:8px;align-items:center;gap:8px;font-size:{16 if h >= 44 else 14}px;line-height:18px;font-weight:700;{st}">{ic}{text}</div>'


def icon_btn(name, size=40, color=INK, bg=SURF, border=True, stroke=2):
    b = f'border:1px solid {G2};' if border else ''
    return f'<div data-name="Icon button · {name}" style="width:{size}px;height:{size}px;border-radius:{size // 2}px;background:{bg};{b}display:flex;align-items:center;justify-content:center;flex:none">{I(name, round(size * .45), color, stroke)}</div>'


def search(placeholder, w=320, h=40):
    return (f'<div data-name="Search" class="row" style="width:{w}px;height:{h}px;border-radius:{h // 2}px;background:{SURF};border:1px solid {G2};align-items:center;gap:10px;padding:0 14px">'
            f'{I("search", 17, G6, 2)}{T(placeholder, 14, 16, 400, G6, nw=True)}</div>')


def stars(n, size=14, color=AMBER, empty=G2, gap=2):
    return row(''.join(I('star-fill', size, color if k < n else empty) for k in range(5)), gap, name='Stars')


def tomato(fresh, size=16):
    return I('fresh' if fresh else 'rotten', size)


def top_tag(small=False):
    return f'<div data-name="Top critic" class="nw" style="{FONT}font-size:{10 if small else 11}px;line-height:12px;font-weight:700;letter-spacing:.6px;padding:3px 6px;border-radius:4px;background:{TOPBG};color:{ARED}">TOP CRITIC</div>'


def outlet(pub, size=13):
    return f'<div data-name="Outlet" class="nw" style="{FONT}font-size:{size}px;line-height:14px;font-weight:700;padding:5px 9px;border-radius:12px;background:{BG};color:{INK}">{pub}</div>'


def avatar(text, size=40, bg=TINT, fg='#fff', img_name=None, fy=0.3):
    if img_name:
        return img(img_name, size, size, size // 2, 0.5, fy)
    return f'<div data-name="Avatar" style="width:{size}px;height:{size}px;border-radius:{size // 2}px;background:{bg};display:flex;align-items:center;justify-content:center;flex:none">{T(text, round(size * .36), round(size * .36), 700, fg, nw=True)}</div>'


AV_COLORS = ['#5B6CC9', '#C96B8B', '#4E9C8F', '#B7894A', '#7D64B8', '#C25F4E', '#5E8FB8']


def verified():
    return row(I('verified', 14, G6, 1.8) + T('Verified', 13, 16, 400, G6, nw=True), 4, name='Verified')


def full_review(text='Full review', color=INK, size=14):
    return row(T(text, size, 16, 700, color, nw=True) + I('arrow-up-right', 14, color, 2), 6, name='Full review')


def score_inline(size=18, fs=15, color=INK):
    return row(I('certified-large', size) + T(f'{TOMATO}%', fs, fs + 2, 700, color, nw=True) + I('popcorn', size) + T(f'{POP}%', fs, fs + 2, 700, color, nw=True), 6, name='Scores')


# ---------------------------------------------------------------- page chrome
def header_light():
    nav = ''.join(T(t, 15, 18, 700, INK, nw=True) for t in ['Movies', 'TV Shows', 'News', 'Showtimes'])
    return f'''<div data-name="Global header" class="row" style="width:1440px;height:64px;padding:0 160px;align-items:center;justify-content:space-between;background:{SURF};border-bottom:1px solid {G15};flex:none">
  <div class="row" style="align-items:center;gap:40px"><img alt="Rotten Tomatoes" src="{full_color_logo(100)}" style="width:100px;height:31px">{row(nav, 28, name='Primary nav')}</div>
  <div class="row" style="align-items:center;gap:14px">{search('Search movies, TV, people', 280, 38)}{T('Sign in', 14, 16, 700, INK, nw=True)}</div></div>'''


def film_bar(section, tabs=None, dark=False, right=None):
    """Film context bar: back to the film page, poster, title, scores, optional section tabs."""
    fg, mute, bg, br = ('#fff', 'rgba(255,255,255,.65)', TINT, 'rgba(255,255,255,.08)') if dark else (INK, G6, SURF, G15)
    poster = img('poster_186', 36, 54, 4, 0.5, 0.3)
    left = row(I('chevron-left', 20, fg, 2.2) + poster + col(row(T('La La Land', 17, 20, 700, fg, nw=True) + T('2016', 15, 20, 400, mute, nw=True), 8)
               + row(I('certified-large', 16) + T(f'{TOMATO}%', 13, 16, 700, fg, nw=True) + I('popcorn', 16) + T(f'{POP}%', 13, 16, 700, fg, nw=True), 6), 4), 12, name='Back to film')
    t = ''
    if tabs:
        t = row(''.join(f'<div class="nw" style="{FONT}font-size:15px;line-height:18px;font-weight:700;color:{fg if x == section else mute};padding:25px 0 23px;{"border-bottom:2px solid " + RED if x == section else "border-bottom:2px solid transparent"}">{x}</div>' for x in tabs), 30, name='Section tabs')
    r = right if right is not None else btn('Rent from $3.99', 'primary', 'play', 40)
    return f'<div data-name="Film bar" class="row" style="width:1440px;height:72px;padding:0 160px;align-items:center;justify-content:space-between;background:{bg};border-bottom:1px solid {br};flex:none">{left}{t}{r}</div>'


def page_title(kicker, title, sub=None, right=''):
    s = T(sub, 16, 24, 400, G6) if sub else ''
    return row(col(label(kicker, ARED) + T(title, 44, 46, 700, INK, 'letter-spacing:-1px', nw=True) + s, 10) + right, 0, 'flex-end', 'space-between', 'width:1120px', name='Page title')


def screen(name, inner, h=None, bg=BG, w=1440):
    hh = f'height:{h}px;' if h else ''
    return f'<div data-name="{name}" class="col" style="width:{w}px;{hh}background:{bg};overflow:hidden;position:relative;flex:none;align-items:center">{inner}</div>'


def backdrop(ctx, dim=0.58):
    uri = png_uri(os.path.join(HERE, f'ctx_{ctx}.png'), 1440, 72)
    return (f'<img alt="" src="{uri}" style="position:absolute;left:0;top:0;width:1440px;height:900px">'
            f'<div data-name="Scrim" style="position:absolute;left:0;top:0;width:1440px;height:900px;background:rgba(8,7,12,{dim})"></div>')


def overlay(name, ctx, panel, dim=0.58):
    return f'<div data-name="{name}" style="position:relative;width:1440px;height:900px;overflow:hidden;flex:none">{backdrop(ctx, dim)}{panel}</div>'


def annotate(screen_name, no, title, kind, idea, why):
    return f'''<div data-name="Annotation" class="col" style="width:1120px;gap:12px">
  {label(f'{screen_name} · {no:02d} · {kind}', ARED)}
  {T(title, 40, 44, 700, INK, 'letter-spacing:-1px', nw=True)}
  {T(idea, 18, 27, 400, INK2, w=980)}
  {T(why, 15, 22, 400, G6, w=980)}</div>'''


def cap(name, ann, scr):
    return f'<div class="cap" data-name="{name}">{ann}{scr}</div>'


def doc(caps, title='Secondary screens'):
    return (f'<!doctype html><html><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head>'
            f'<body><div class="col" style="gap:140px;padding:40px;align-items:flex-start">{caps}</div></body></html>')
