"""Prepares the uploads in assets/video for the web. They stay untouched.

Recordings are remuxed so they can start before they finish downloading, with no re-encoding,
and each gets a poster from its first frame. Screenshots get their red boxes and become
.webp in assets/img.
Run: python3 case-study/_src/make_media.py
"""
import io
import os
import subprocess

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
UPLOADS = os.path.join(ROOT, 'assets', 'video')
OUT = os.path.join(UPLOADS, 'web')
IMG = os.path.join(ROOT, 'assets', 'img')

# uploaded file → name used in content.py
VIDEOS = {
    'RT Hero': 'rt-hero',
    'RT Hero Interactions': 'hero-interactions',
    'RT ads': 'ads',
    'Critics Reviews': 'critics-reviews',
    'Area': 'audience-reviews',
    'Rating Ratio': 'rating-ratio',
    'Hover Explanations': 'hover-explanations',
}
# uploaded file → name used in content.py, and the problem areas in the upload's pixels (left, top, right, bottom)
IMAGES = {
    'Old RT First Screen Unclear Hierarchy': ('old-hierarchy', [(752, 1462, 1806, 1648)]),
    'Old RT Ads Mixed with Content': ('old-ads-mixed', [(1924, 226, 2552, 1388), (448, 866, 1872, 1062), (1138, 1488, 1804, 1636)]),
}
BOX_COLOR = '#FA320A'
BOX_WIDTH = 14


def save_webp(im, name, width):
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    path = os.path.join(IMG, name + '.webp')
    im.convert('RGB').save(path, quality=84, method=6)
    return os.path.getsize(path) >> 10


os.makedirs(OUT, exist_ok=True)
for upload, name in VIDEOS.items():
    src = os.path.join(UPLOADS, upload + '.mp4')
    dst = os.path.join(OUT, name + '.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-map', '0:v:0', '-c', 'copy', '-an',
                    '-movflags', '+faststart', dst], check=True)
    frame = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', src, '-frames:v', '1', '-c:v', 'png',
                            '-f', 'image2pipe', '-'], check=True, capture_output=True).stdout
    poster = save_webp(Image.open(io.BytesIO(frame)), f'poster-{name}', 1432)
    print(f'{name}: video {os.path.getsize(dst) >> 10} KB, poster {poster} KB')

for upload, (name, boxes) in IMAGES.items():
    im = Image.open(os.path.join(UPLOADS, upload + '.jpg')).convert('RGB')
    draw = ImageDraw.Draw(im)
    for box in boxes:
        draw.rectangle(box, outline=BOX_COLOR, width=BOX_WIDTH)
    print(f'{name}: {save_webp(im, name, 2200)} KB')
