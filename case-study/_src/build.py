"""Renders the case study from content.py. Run: python3 case-study/_src/build.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import v_plates

def write(rel, text):
    path = os.path.join(ROOT, rel)
    with open(path, 'w', encoding='utf8') as f:
        f.write(text)
    print(rel, len(text) // 1024, 'KB')


write('index.html', v_plates.page())
