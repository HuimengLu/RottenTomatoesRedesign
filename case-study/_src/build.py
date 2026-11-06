"""Renders the case study from content.py. Run: python3 case-study/_src/build.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import v_plates

REDIRECT = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Rotten Tomatoes Redesign</title>
<meta http-equiv="refresh" content="0; url=plates/">
<link rel="canonical" href="plates/">
</head><body><a href="plates/">Rotten Tomatoes Redesign</a></body></html>
'''


def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf8') as f:
        f.write(text)
    print(rel, len(text) // 1024, 'KB')


write('plates/index.html', v_plates.page())
write('index.html', REDIRECT)
