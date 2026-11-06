"""Figma design-context JSX (React + Tailwind) -> static HTML with inline CSS.

Only the Tailwind vocabulary Figma's codegen emits is supported; unknown classes raise so nothing is silently dropped.
"""
import os, re, subprocess, html

TW_FONT = {'Bold': ('700', 'normal'), 'Regular': ('400', 'normal'), 'Medium': ('500', 'normal'),
           'Italic': ('400', 'italic'), 'Bold Italic': ('700', 'italic'), 'Semi Bold': ('600', 'normal')}
FRAC = {'1/4': '25%', '1/2': '50%', '3/4': '75%', '1/3': '33.333%', '2/3': '66.667%'}
DIRS = {'t': 'to top', 'b': 'to bottom', 'l': 'to left', 'r': 'to right'}


def arb(t):
    m = re.search(r'\[(.*)\]$', t)
    return m.group(1).replace('_', ' ') if m else None


def is_len(v):
    return bool(re.match(r'^-?[\d.]+(px|%|em|rem)?$', v)) or v == '0'


def tw(cls):
    css = {}
    grad = {}
    for t in cls.split():
        v = arb(t)
        if t in ('relative', 'absolute', 'fixed', 'sticky'): css['position'] = t
        elif t == 'shrink-0': css['flex-shrink'] = '0'
        elif t == 'content-stretch': css['align-content'] = 'stretch'
        elif t == 'flex': css['display'] = 'flex'
        elif t == 'block': css['display'] = 'block'
        elif t == 'contents': css['display'] = 'contents'
        elif t == 'flex-col': css['flex-direction'] = 'column'
        elif t.startswith('items-'): css['align-items'] = {'start': 'flex-start', 'end': 'flex-end', 'center': 'center', 'baseline': 'baseline', 'stretch': 'stretch'}[t[6:]]
        elif t.startswith('justify-'): css['justify-content'] = {'start': 'flex-start', 'end': 'flex-end', 'center': 'center', 'between': 'space-between'}[t[8:]]
        elif t == 'self-stretch': css['align-self'] = 'stretch'
        elif t.startswith('flex-[') and v: css['flex'] = v
        elif t.startswith('gap-[') and v: css['gap'] = v
        elif t == 'w-full': css['width'] = '100%'
        elif t == 'h-full': css['height'] = '100%'
        elif t == 'size-full': css['width'] = css['height'] = '100%'
        elif t == 'w-px': css['width'] = '1px'
        elif t == 'h-px': css['height'] = '1px'
        elif t == 'min-w-px': css['min-width'] = '1px'
        elif t == 'max-w-none': css['max-width'] = 'none'
        elif t.startswith('w-[') and v: css['width'] = v
        elif t.startswith('h-[') and v: css['height'] = v
        elif t.startswith('size-[') and v: css['width'] = css['height'] = v
        elif t.startswith('aspect-[') and v: css['aspect-ratio'] = v
        elif t == 'inset-0': css['inset'] = '0'
        elif t.startswith('inset-[') and v: css['inset'] = v
        elif re.match(r'^(left|right|top|bottom)-', t):
            side, val = t.split('-', 1)
            css[side] = v if v else ('0' if val == '0' else FRAC.get(val) or {'px': '1px'}[val])
        elif t.startswith('text-['):
            if is_len(v): css['font-size'] = v
            else: css['color'] = v
        elif t == 'text-white': css['color'] = '#ffffff'
        elif t == 'text-black': css['color'] = '#000000'
        elif t.startswith('font-[') and v:
            fam, _, sty = v.strip("'").partition(':')
            fam = 'Arial' if fam in ('Arimo', 'Arial') else fam
            css['font-family'] = f"'{fam}', Arial, Helvetica, sans-serif"
            wgt, it = TW_FONT[sty]
            css['font-weight'] = wgt
            css['font-style'] = it
        elif t == 'font-normal': css['font-weight'] = '400'
        elif t == 'font-bold': css['font-weight'] = '700'
        elif t == 'not-italic': css['font-style'] = 'normal'
        elif t == 'italic': css['font-style'] = 'italic'
        elif t.startswith('leading-[') and v: css['line-height'] = v
        elif t.startswith('tracking-[') and v: css['letter-spacing'] = v
        elif t == 'whitespace-nowrap': css['white-space'] = 'nowrap'
        elif t == 'uppercase': css['text-transform'] = 'uppercase'
        elif t == 'text-center': css['text-align'] = 'center'
        elif t == 'text-right': css['text-align'] = 'right'
        elif t == 'underline': css['text-decoration'] = 'underline'
        elif t.startswith('[') and v and ':' in v:
            k, _, val = v.partition(':'); css[k] = val
        elif t == 'overflow-clip': css['overflow'] = 'hidden'
        elif t == 'overflow-hidden': css['overflow'] = 'hidden'
        elif t.startswith('rounded-[') and v: css['border-radius'] = v
        elif re.match(r'^rounded-(tl|tr|bl|br)-\[', t):
            c = {'tl': 'top-left', 'tr': 'top-right', 'bl': 'bottom-left', 'br': 'bottom-right'}[t[8:10]]
            css[f'border-{c}-radius'] = v
        elif t.startswith('bg-gradient-to-'): grad['dir'] = DIRS[t[-1]]
        elif t.startswith('from-[') and v: grad['from_pos' if is_len(v) else 'from'] = v
        elif t.startswith('via-[') and v: grad['via_pos' if is_len(v) else 'via'] = v
        elif t.startswith('to-[') and v: grad['to_pos' if is_len(v) else 'to'] = v
        elif t.startswith('bg-[') and v: css['background-color'] = v
        elif t == 'bg-black': css['background-color'] = '#000000'
        elif t == 'bg-white': css['background-color'] = '#ffffff'
        elif t == 'border': css['border-width'] = '1px'
        elif re.match(r'^border-\d+$', t): css['border-width'] = t.split('-')[1] + 'px'
        elif t in ('border-b', 'border-t', 'border-l', 'border-r'):
            css[{'b': 'border-bottom-width', 't': 'border-top-width', 'l': 'border-left-width', 'r': 'border-right-width'}[t[-1]]] = '1px'
        elif t == 'border-solid': css['border-style'] = 'solid'
        elif t == 'border-dashed': css['border-style'] = 'dashed'
        elif t == 'border-white': css['border-color'] = '#ffffff'
        elif t.startswith('border-[') and v: css['border-color'] = v
        elif re.match(r'^(p|px|py|pt|pb|pl|pr)-\[', t):
            k = t.split('-')[0]
            sides = {'p': ['top', 'right', 'bottom', 'left'], 'px': ['left', 'right'], 'py': ['top', 'bottom'],
                     'pt': ['top'], 'pb': ['bottom'], 'pl': ['left'], 'pr': ['right']}[k]
            for sd in sides: css[f'padding-{sd}'] = v
        elif t.startswith('shadow-[') and v: css['box-shadow'] = v
        elif t.startswith('drop-shadow-[') and v: css['filter'] = f'drop-shadow({v})'
        elif t == 'object-cover': css['object-fit'] = 'cover'
        elif t == 'object-contain': css['object-fit'] = 'contain'
        elif t == 'pointer-events-none': css['pointer-events'] = 'none'
        elif re.match(r'^opacity-\d+$', t): css['opacity'] = str(int(t.split('-')[1]) / 100)
        else:
            raise ValueError('unsupported class: ' + t)
    if grad:
        stops = []
        for k in ('from', 'via', 'to'):
            if k in grad:
                pos = grad.get(k + '_pos', {'from': '0%', 'via': '50%', 'to': '100%'}[k])
                stops.append(f"{grad[k]} {pos}")
        css['background-image'] = f"linear-gradient({grad.get('dir', 'to bottom')}, {', '.join(stops)})"
    return css


def css_str(d):
    return ';'.join(f'{k}:{v}' for k, v in d.items())


def assets(src, tag, out_dir, rel):
    os.makedirs(out_dir, exist_ok=True)
    prefix = re.search(r'const assetPathPrefix = "([^"]+)"', src).group(1)
    mp = {}
    for name, f in re.findall(r'const (\w+) = `\$\{assetPathPrefix\}/([^`]+)`;', src):
        local = f'{tag}-{f}'
        path = os.path.join(out_dir, local)
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            subprocess.run(['curl', '-s', '-f', '-L', '-o', path, f'{prefix}/{f}'], check=True)
        mp[name] = f'{rel}/{local}'
    return mp


def jsx_to_html(src, amap):
    body = src[src.index('return (') + len('return ('):src.rindex(');')]

    def attr_class(m):
        return f'style="{html.escape(css_str(tw(m.group(1))), quote=True)}"'
    body = re.sub(r'className="([^"]*)"', attr_class, body)
    body = re.sub(r'src=\{(\w+)\}', lambda m: f'src="{amap[m.group(1)]}"', body)
    # style={{ backgroundImage: "..." }} merged into the style attribute that precedes or follows
    def merge_style(m):
        return f'data-bg="{html.escape(m.group(1), quote=True)}"'
    body = re.sub(r'style=\{\{\s*backgroundImage:\s*"([^"]+)"\s*\}\}', merge_style, body)
    body = re.sub(r'style="([^"]*)"([^>]*?)data-bg="([^"]*)"', lambda m: f'style="{m.group(1)};background-image:{m.group(3)}"{m.group(2)}', body)
    body = re.sub(r'data-bg="([^"]*)"([^>]*?)style="([^"]*)"', lambda m: f'{m.group(2)}style="{m.group(3)};background-image:{m.group(1)}"', body)
    # template-literal text
    body = re.sub(r'\{`([^`]*)`\}', lambda m: html.escape(m.group(1), quote=False), body)
    # self-closing non-void elements
    body = re.sub(r'<(div|p|span)(\s[^<>]*?)?\s*/>', lambda m: f'<{m.group(1)}{m.group(2) or ""}></{m.group(1)}>', body)
    # JSX whitespace: drop indentation-only text between tags, trim text lines
    body = re.sub(r'>\s*\n\s*', '>', body)
    body = re.sub(r'\s*\n\s*<', '<', body)
    if '{' in re.sub(r'"[^"]*"', '', body):
        raise ValueError('unconverted JSX expression left')
    return body.strip()


def convert(jsx_path, tag, out_dir, rel='assets'):
    src = open(jsx_path).read()
    amap = assets(src, tag, os.path.join(out_dir, rel), rel)
    return jsx_to_html(src, amap)
