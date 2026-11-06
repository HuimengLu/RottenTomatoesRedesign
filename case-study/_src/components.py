"""Reusable HTML components for the case study."""
import hashlib
import html
import os
from functools import lru_cache

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = 'assets'

esc = html.escape


@lru_cache(maxsize=None)
def size(name):
    with Image.open(os.path.join(ROOT, 'assets', 'img', name + '.webp')) as im:
        return im.size


@lru_cache(maxsize=None)
def versioned(url):
    """Adds a hash of the file to its URL, so a browser holding an older build fetches the new one."""
    with open(os.path.join(ROOT, url), 'rb') as f:
        return f'{url}?v={hashlib.sha256(f.read()).hexdigest()[:8]}'


def src(name):
    return versioned(f'{ASSETS}/img/{name}.webp')


def video_url(name):
    return versioned(f'{ASSETS}/video/web/{name}.mp4')


def img(name, alt='', cls='', eager=False):
    w, h = size(name)
    load = 'eager' if eager else 'lazy'
    c = f' class="{cls}"' if cls else ''
    return f'<img{c} src="{src(name)}" width="{w}" height="{h}" alt="{esc(alt)}" loading="{load}" decoding="async">'


def icon(name, alt='', cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<img{c} src="{ASSETS}/svg/{name}.svg" alt="{esc(alt)}" width="96" height="96">'


def zoom_attrs(name, title):
    return f'data-zoom="{src(name)}" data-title="{esc(title, quote=True)}" role="button" tabindex="0" aria-label="View larger: {esc(title, quote=True)}"'


def plate(name, alt, tag=None, cls=''):
    """An image tile. Click opens the lightbox."""
    t = f'<span class="plate__tag">{esc(tag)}</span>' if tag else ''
    return f'<div class="plate zoomable {cls}" {zoom_attrs(name, alt)}>{t}{img(name, alt)}</div>'


def video_tag(name, alt, attrs):
    return (f'<video {attrs} muted loop playsinline poster="{src("poster-" + name)}" width="1908" height="1080" '
            f'aria-label="{esc(alt, quote=True)}"><source src="{video_url(name)}" type="video/mp4"></video>')


def video_plate(name, alt, cls=''):
    """A looping video tile. It plays while on screen, and a click opens it larger."""
    return (f'<div class="plate zoomable {cls}" data-zoom="{video_url(name)}" data-kind="video" '
            f'data-title="{esc(alt, quote=True)}" role="button" tabindex="0" aria-label="View larger: {esc(alt, quote=True)}">'
            f'{video_tag(name, alt, "data-inview preload=none")}</div>')


def wipe(original, redesign):
    """Before/after frame. shared/site.js moves the divider as the reader scrolls, and plays the video."""
    return f'''<div class="cmp" style="--x:50%">
  {img(original["image"], original["alt"], eager=True)}
  <span class="cmp__tag cmp__tag--a">Original</span>
  <div class="cmp__after">{video_tag(redesign["video"], redesign["alt"], "preload=metadata")}<span class="cmp__tag cmp__tag--b">Redesign</span></div>
  <div class="cmp__bar"></div>
</div>'''


def head(title, css, desc):
    return f'''<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc, quote=True)}">
<link rel="icon" href="{ASSETS}/svg/tomato.svg" type="image/svg+xml">
<link rel="preload" href="{ASSETS}/fonts/instrument-sans-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{ASSETS}/fonts/outfit-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{versioned("shared/system.css")}">
<link rel="stylesheet" href="{versioned(css)}">
</head>'''


def rotten_tomatoes_chunk():
    """The wordmark's trick applied to live type: a splat in Rotten, a tomato in Tomatoes."""
    return ('<span class="nb">R<span class="o-splat"><i></i></span>tten</span> '
            '<span class="nb">Tomat<i class="glyph glyph--tomato"></i>es</span>')
