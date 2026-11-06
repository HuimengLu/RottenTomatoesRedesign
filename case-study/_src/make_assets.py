"""Cuts the Figma exports in _src/figma into the web images used by the case study.

Coordinates are Figma 1x page coordinates; final-full.png and old-full.png are 2x.
Run: python3 case-study/_src/make_assets.py
"""
import os
import shutil
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIG = os.path.join(HERE, 'figma')
OUT = os.path.join(ROOT, 'assets', 'img')
PROTO = os.path.join(os.path.dirname(ROOT), 'interactive', 'assets')
HEUR = os.path.join(os.path.dirname(ROOT), 'heuristic-evaluation', 'img')

os.makedirs(OUT, exist_ok=True)


def save(im, name, width=None, q=84):
    im = im.convert('RGB')
    if width and im.width != width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    path = os.path.join(OUT, name + '.webp')
    im.save(path, 'WEBP', quality=q, method=6)
    print(f'{name}.webp {im.size} {os.path.getsize(path) // 1024}KB')


final = Image.open(os.path.join(FIG, 'final-full.png')).convert('RGB')
old = Image.open(os.path.join(FIG, 'old-full.png')).convert('RGB')


def cut(src, x, y, w, h, scale=2):
    return src.crop((x * scale, y * scale, (x + w) * scale, (y + h) * scale))


# Whole pages
save(final, 'final-full', 2160, 82)
save(old, 'old-full', 2160, 82)
save(final, 'final-full-sm', 900, 78)
save(old, 'old-full-sm', 900, 78)

# First viewport at the same 1440x900 frame, the fair before/after comparison
save(cut(final, 0, 0, 1440, 900), 'final-first')
save(cut(old, 0, 0, 1440, 900), 'old-first')

# Redesign sections
SECTIONS_NEW = {
    'final-hero': (0, 164, 1440, 800),
    'final-hero-tight': (32, 172, 1376, 760),
    'final-where': (160, 964, 1120, 93),
    'final-overview': (160, 964, 1120, 308),
    'final-critics': (160, 1320, 1120, 816),
    'final-critics-lead': (160, 1320, 1120, 500),
    'final-audience': (160, 2184, 796, 831),
    'final-audience-ad': (160, 2184, 1120, 831),
    'final-ad-leader': (0, 3015, 1440, 158),
    'final-cast': (160, 3173, 1120, 317),
    'final-media': (160, 3490, 1120, 400),
    'final-related': (160, 3890, 1120, 458),
    'final-credits': (0, 4348, 1440, 800),
    'final-scores-crop': (64, 196, 520, 200),
    'final-cta-crop': (64, 776, 520, 124),
}
for name, box in SECTIONS_NEW.items():
    save(cut(final, *box), name)

# Original page modules, used for the crops and the long-take sort
SECTIONS_OLD = {
    'old-hero': (170, 226, 1100, 480),
    'old-chrome': (170, 0, 1100, 226),
    'old-scorecard': (186, 706, 728, 250),
    'old-nav': (186, 956, 728, 70),
    'old-where': (186, 1026, 728, 239),
    'old-know': (186, 1265, 728, 242),
    'old-ad1': (186, 1507, 728, 142),
    'old-critics': (186, 1649, 728, 388),
    'old-audience': (186, 2037, 728, 322),
    'old-rating': (186, 2359, 728, 255),
    'old-cast': (186, 2615, 728, 260),
    'old-clips': (186, 2875, 728, 310),
    'old-more': (186, 3185, 728, 482),
    'old-videos': (186, 3667, 728, 310),
    'old-photos': (186, 3977, 728, 257),
    'old-ad2': (186, 4234, 728, 142),
    'old-info': (186, 4376, 728, 1276),
    'old-synopsis': (186, 4376, 728, 280),
    'old-side': (954, 722, 300, 605),
    'old-mpu': (954, 1327, 300, 290),
    'old-score-area': (170, 706, 1100, 330),
    'old-reviews': (170, 1649, 760, 710),
}
for name, box in SECTIONS_OLD.items():
    save(cut(old, *box), name)

# Drawers and sticky header
save(Image.open(os.path.join(FIG, 'drawer-critics.png')), 'drawer-critics')
save(Image.open(os.path.join(FIG, 'drawer-audience.png')), 'drawer-audience')
save(Image.open(os.path.join(FIG, 'sticky.png')), 'sticky-bar')

# Early explorations: four directions, first viewport and full page
for name, f in {'x-a': 'x-a-reel', 'x-b': 'x-b-tint', 'x-c': 'x-c-verdict', 'x-d': 'x-d-broadsheet',
                'it-1': 'it-1', 'it-2': 'it-2'}.items():
    im = Image.open(os.path.join(FIG, f + '.png')).convert('RGB')
    save(im.crop((0, 0, 1440, 900)), name + '-first', 1440, 82)
    save(im, name + '-full', 1200, 76)

for f in ['x-critics-cards', 'x-aud-cards', 'x-thecritics', 'x-news1', 'x-news2', 'x-news4',
          'theme-system', 'm-first', 'm-sheet', 'old-takeover']:
    save(Image.open(os.path.join(FIG, f + '.png')), f, None, 86)

# Real captures from the live page
for f in ['score-modal', 'duplicate-videos', 'audience-reviews', 'section-nav-truncated', 'cta-styles']:
    src = os.path.join(HEUR, f + '.jpg')
    if os.path.exists(src):
        save(Image.open(src), 'live-' + f, None, 84)

# Stills from the prototype
for f in ['hero-poster.jpg', 'end-still.jpg']:
    src = os.path.join(PROTO, f)
    if os.path.exists(src):
        save(Image.open(src), 'still-' + f.split('.')[0], None, 84)
save(Image.open(os.path.join(PROTO, 'hero-poster.jpg')), 'still-hero-poster-sm', 1000, 78)

print('done')
