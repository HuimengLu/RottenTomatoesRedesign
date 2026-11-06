"""Chooser page: compares the three storytelling forms. Remove it once one version is picked."""
import content as C
from components import esc

VERSIONS = [
    ('plates', 'A', 'Plates', 'A monograph of image tiles',
     'Closest to the Pentagram project page. White canvas, tight gutters, chapter plates in red, grey and black. The story is told by the sequence of images, and text stays in captions and pull quotes.',
     'Best for a recruiter scanning in a few minutes.'),
    ('long-take', 'B', 'The Long Take', 'One unbroken shot',
     'The original page and the redesign sit in one world, and scrolling moves a single camera across them. Ads light up, the reader’s route is drawn on the page, then the modules lift off, sort themselves into P0 to P3, and the camera travels to the redesign.',
     'Best for walking someone through the reasoning live.'),
    ('feature', 'C', 'Feature Presentation', 'A screening in five reels',
     'The case study plays like a film, with a scope title card, subtitles, an intermission for the business constraints, a ticket for the journey, a billing block for the hierarchy and end credits for the reflection.',
     'Best for being remembered.'),
]


def page():
    m = C.META
    tiles = ''
    for slug, letter, name, sub, body, best in VERSIONS:
        tiles += f'''<a class="v" href="{slug}/">
  <div class="v__i"><img src="assets/img/cover-{slug}.webp" alt="{esc(name)} version" width="1440" height="900"></div>
  <div class="v__t"><span class="v__l">{letter}</span><h2>{name}</h2><p class="v__s">{sub}</p><p>{esc(body)}</p><p class="v__b">{esc(best)}</p></div>
</a>'''
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(m["title"])} Three versions</title>
<link rel="icon" href="assets/svg/tomato.svg" type="image/svg+xml">
<style>
@font-face{{font-family:"Instrument Sans";src:url(assets/fonts/instrument-sans-latin-wght-normal.woff2) format("woff2");font-weight:400 700;font-display:swap}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:"Instrument Sans",Arial,sans-serif;color:#1A1A1A;background:#fff;-webkit-font-smoothing:antialiased;padding:clamp(12px,1.67vw,24px);line-height:1.34}}
h1{{font-weight:400;font-size:clamp(40px,7vw,104px);line-height:1;letter-spacing:-.034em;margin:clamp(24px,5vw,72px) 0 12px}}
.s{{font-size:clamp(18px,1.66vw,24px);max-width:32em;margin-bottom:clamp(32px,4vw,56px)}}
.g{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(8px,.84vw,12px)}}
a{{color:inherit;text-decoration:none}}
.v{{display:flex;flex-direction:column;background:#F4F4F4;transition:background .2s}}
.v:hover{{background:#EBEBEB}}
.v__i{{overflow:hidden;aspect-ratio:1.6;background:#000}}
.v__i img{{display:block;width:100%;height:100%;object-fit:cover;transition:transform .9s cubic-bezier(.2,.7,.1,1)}}
.v:hover img{{transform:scale(1.02)}}
.v__t{{padding:16px 16px 20px;display:grid;gap:6px;font-size:16px}}
.v__l{{display:inline-grid;place-items:center;width:26px;height:26px;background:#FA320A;color:#fff;font-weight:700;font-size:14px;border-radius:3px}}
h2{{font-weight:400;font-size:clamp(24px,2.3vw,34px);letter-spacing:-.016em;line-height:1.1;margin-top:8px}}
.v__s{{color:#666}}
.v__b{{font-weight:500;margin-top:6px}}
.n{{margin-top:16px;font-size:14px;color:#666;max-width:60em}}
@media(max-width:860px){{.g{{grid-template-columns:minmax(0,1fr)}}}}
</style></head><body>
<h1>{esc(m["title"])}</h1>
<p class="s">Three storytelling forms for the same case study. They share one design system and one copy file, and differ only in how the story is told.</p>
<div class="g">{tiles}</div>
<p class="n">Edit the copy in _src/content.py, then run python3 _src/build.py to update all three.</p>
</body></html>'''
