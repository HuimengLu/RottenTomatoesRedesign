"""Turns the frozen snapshots into self-contained HTML for Figma's html_to_figma.

Viewport units become fixed 1440×900 px, media queries are dropped, and fonts and images are inlined.
Usage: python3 case-study/_src/figma_export.py <snapshot dir>
"""
import base64
import io
import os
import re
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SNAP = sys.argv[1]
VW, VH = 1440, 900
MAX_W = 1800
Image.MAX_IMAGE_PIXELS = None


def num(tok):
    tok = tok.strip()
    m = re.fullmatch(r'(-?[\d.]+)(px|vw|vh)?', tok)
    if not m:
        return None
    v = float(m.group(1))
    return v * VW / 100 if m.group(2) == 'vw' else v * VH / 100 if m.group(2) == 'vh' else v


def px_units(css):
    def clamp(m):
        a, b, c = (num(m.group(i)) for i in (1, 2, 3))
        if None in (a, b, c):
            return m.group(0)
        return f'{min(max(a, b), c):.2f}px'
    css = re.sub(r'clamp\(([^(),]+),([^(),]+),([^(),]+)\)', clamp, css)
    css = re.sub(r'(-?[\d.]+)vw\b', lambda m: f'{float(m.group(1)) * VW / 100:.2f}px', css)
    css = re.sub(r'(-?[\d.]+)d?vh\b', lambda m: f'{float(m.group(1)) * VH / 100:.2f}px', css)
    return css


def drop_media(css):
    out, i = [], 0
    while True:
        j = css.find('@media', i)
        if j < 0:
            out.append(css[i:])
            return ''.join(out)
        out.append(css[i:j])
        k = css.index('{', j)
        depth, k = 1, k + 1
        while depth:
            depth += {'{': 1, '}': -1}.get(css[k], 0)
            k += 1
        i = k


def read(rel):
    with open(os.path.join(ROOT, rel), encoding='utf8') as f:
        return f.read()


def data_uri(path, fallback_q=84):
    ext = os.path.splitext(path)[1].lower()
    if ext == '.svg':
        with open(path, 'rb') as f:
            return 'data:image/svg+xml;base64,' + base64.b64encode(f.read()).decode()
    im = Image.open(path)
    has_alpha = im.mode in ('RGBA', 'LA') or 'transparency' in im.info
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    if has_alpha:
        im.convert('RGBA').save(buf, 'PNG', optimize=True)
        return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()
    im.convert('RGB').save(buf, 'JPEG', quality=fallback_q, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


def font(rel, fmt='woff2'):
    with open(os.path.join(ROOT, rel), 'rb') as f:
        return f'url(data:font/woff2;base64,{base64.b64encode(f.read()).decode()}) format("{fmt}")'


FRAME_CSS = '''
html,body{margin:0;padding:0;width:1440px;background:#fff;overflow:visible!important}
body{padding:0!important}
.ff-root{display:block;width:1440px}
.ff{position:relative;display:block;width:1440px;overflow:hidden;background:var(--bg)}
.js .reveal{opacity:1;transform:none}
.cmp__knob,.cmp__bar{display:block}
.top{position:static!important;backdrop-filter:none}
.plate__tag,.bar__t a{backdrop-filter:none}
.crops .plate{aspect-ratio:auto}
.crops .plate img{height:auto;object-fit:fill;margin:0}
.crops .crops__nav img{width:100%;margin:0}
/* Long take storyboard */
.ff-b{height:900px;min-height:900px;background:#F4F4F4}
.ff-stage{position:absolute;left:0;top:0;width:1440px;height:900px;object-fit:cover;display:block}
.ff-b .step{position:relative;min-height:0!important;height:auto}
.ff-b .step .panel{min-height:900px}
.ff-b--full .step{height:900px;display:grid;place-items:center}
.ff-b--full .step .panel{min-height:0}
.ff-b--sort .step{display:block}
.ff-b--sort .step .panel{position:relative;min-height:0;display:block;padding-top:72px}
.ff-b--sort .step .panel>*{max-width:900px}
.step--travel{min-height:0!important}
/* Feature pinned scenes */
.ff-c-pin{height:900px}
.ff-c-pin .scene,.ff-c-pin .open{height:900px!important}
.ff-c-pin .scene__pin,.ff-c-pin .open__pin{position:relative;height:900px}
.ff-c-pin .subs p{opacity:1}
.v-feature .screen__p{transform:translateY(calc(var(--p,0) * -3400px))}
.credits__bg{position:absolute;inset:0;height:auto;margin:0}
'''


def build(slug, css_rel, theme):
    html = read(os.path.relpath(os.path.join(SNAP, f'{slug}.raw.html'), ROOT))

    def repl(m):
        src = m.group(1)
        if src.startswith('data:'):
            return m.group(0)
        if src.startswith('stage/'):
            p = os.path.join(SNAP, src)
        else:
            p = os.path.join(ROOT, re.sub(r'^https?://[^/]+/case-study/', '', src).replace('../', ''))
        return f'src="{data_uri(p)}"'
    html = re.sub(r'src="([^"]+)"', repl, html)
    n = {'i': 0}

    def group(m):
        g = n['i'] // 16
        n['i'] += 1
        return f'class="ff ffg{g}{m.group(1)}'
    html = re.sub(r'class="ff( |")', lambda m: group(m), html)
    html = re.sub(r'poster="[^"]*"', '', html)
    html = re.sub(r'\s(srcset|data-zoom|data-title|data-fit|tabindex|role|data-step)=("[^"]*"|\'[^\']*\')', '', html)

    css = drop_media(read('shared/system.css')) + drop_media(read(css_rel))
    css = re.sub(r'@font-face\{[^}]*\}', '', css)
    css = px_units(css).replace('../assets/svg/', 'assets/svg/')
    faces = (f'@font-face{{font-family:"Instrument Sans";src:{font("assets/fonts/instrument-sans-latin-wght-normal.woff2")};font-weight:400 700;font-style:normal}}'
             f'@font-face{{font-family:"Outfit";src:{font("assets/fonts/outfit-latin-wght-normal.woff2")};font-weight:100 900;font-style:normal}}')
    doc = (f'<!doctype html><html lang="en" data-theme="{theme}"><head><meta charset="utf-8">'
           f'<meta name="viewport" content="width=1440"><title>{slug}</title>'
           f'<style>{faces}{css}{FRAME_CSS}</style></head><body class="js">{html}</body></html>')
    out = os.path.join(HERE, 'figma', f'export-{slug}.html')
    with open(out, 'w', encoding='utf8') as f:
        f.write(doc)
    print(slug, os.path.getsize(out) >> 20, 'MB', n['i'], 'frames', 'groups', n['i'] // 16 + 1)


build('plates', 'plates/plates.css', 'light')
build('long-take', 'long-take/longtake.css', 'light')
build('feature', 'feature/feature.css', 'dark')
