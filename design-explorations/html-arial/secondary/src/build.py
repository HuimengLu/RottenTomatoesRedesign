"""Build one secondary-screen set: python3 sec/build.py critics|audience|media|cast"""
import os, sys, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base import annotate, cap, doc

SCREENS = {'critics': 'Critics Reviews', 'audience': 'Audience Reviews', 'media': 'Videos & Photos', 'cast': 'Cast & Crew'}


def build(key):
    mod = importlib.import_module(key)
    caps = ''
    for i, (fn, kind, title, idea, why) in enumerate(mod.VARIANTS, 1):
        name = f'{SCREENS[key]} · {i:02d} · {title}'
        caps += cap(name, annotate(SCREENS[key], i, title, kind, idea, why), fn())
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'{key}.html')
    open(out, 'w').write(doc(caps, SCREENS[key]))
    print(out, os.path.getsize(out) // 1024, 'KB')


if __name__ == '__main__':
    for k in sys.argv[1:]:
        build(k)
