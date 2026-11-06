"""Critics and Audience review drawers (Figma 187:1356 and 187:1053): light panels over the film page."""
import html as _h

CRITICS = [  # name, outlet, date, fresh, score, quote, top critic (real RT reviews)
    ('Mark Kermode', 'Observer (UK)', 'Jan 16, 2017', True, '5/5', "It is simply a splendid continuation of cinema’s ever-evolving love affair with song and dance.", True),
    ('Linda Holmes', 'NPR', 'Jan 30, 2017', True, '', "It’s just gorgeous, like a flipbook made of dreamy vintage postcards that are somehow about contemporary life in Los Angeles.", True),
    ('Ian Freer', 'Empire Magazine', 'Jan 8, 2017', True, '5/5', "Audacious, retro, funny and heartfelt, La La Land is the latest great musical for people who don’t like musicals.", True),
    ('Nigel Andrews', 'Financial Times', 'Jan 12, 2017', True, '4/5', 'If it were any more enchanting, the musical romantic comedy La La Land ... would break your heart.', True),
    ('Soraya Nadia McDonald', 'Andscape', 'Sep 26, 2017', False, '', 'It makes it more difficult to just let something like La La Land just passively wash over you when, however well-intentioned, the film hearkens back to a time when black humanity onscreen was deliberately hamstrung.', True),
    ('Erika Balsom', 'Sight & Sound', 'Jan 20, 2017', True, '', 'La La Land remembers when movies were magical and fun, blending nostalgia and contemporaneity in a candy-sweet love letter to cinema.', True),
    ('Angie Han', 'Slashfilm', 'Jun 13, 2017', True, '8.5/10', "It’s a story as old as Hollywood and jazz, and Ryan Gosling and Emma Stone feel like a pairing for the ages.", False),
    ('Christina Newland', 'Little White Lies', 'Jan 9, 2017', True, '4/5', 'Open-hearted gushy romanticism in CinemaScope. What’s not to love?', False),
    ('Candice Frederick', 'Reel Talk Online', 'Mar 22, 2017', True, 'B-', "Don’t get me wrong, LA LA LAND is fun and cutesy... But there’s one distinct difference between good movie musicals and great movie musicals.", False),
]
AUDIENCE = [  # name, date, stars, text, helpful votes, avatar colour
    ('First L', 'Aug 22, 2026', 5, 'I was thrilled that they brought this masterpiece back to Dolby Cinema for 10th Anniversary. It was every bit as powerful and emotional as the first time that I saw it 10 years ago. Ryan & Emmas chemistry is legendary!', 1200, '#5B6CC9'),
    ('Venus', 'Aug 27, 2026', 5, "One of THE BEST movies of all time with musical scores, acting, and story line. Doesn’t matter how many times I have seen this movie, it breaks me every time (and I don’t even care for musicals I’m extremely picky!)", 856, '#C96B8B'),
    ('Zaahir', 'Aug 27, 2026', 4, 'Amazing cinematography and seeing it in Dolby made me appreciate this film more. Ryan Gosling was a standout, some of the songs dragged on a bit but overall great movie and certainly lived up to the hype.', 431, '#4E9C8F'),
    ('Isamara', 'Aug 22, 2026', 5, 'Loved rewatching it in theaters and crying because I knew what was coming in the end. Overall such a great film i think anyone can enjoy.', 310, '#B7894A'),
    ('Luis', 'Aug 31, 2026', 5, 'Worth a watch every few months. Damien Chazelle nailed it with this one in every category.', 214, '#7D64B8'),
    ('sonny', 'Aug 22, 2026', 5, 'Saddest most beautiful piece of art I’ve seen in person', 198, '#C25F4E'),
    ('Melanie V', 'Aug 25, 2026', 5, 'Now I get what everyone has been saying for the past decade about the film', 120, '#5E8FB8'),
]
DIST = [(5, '52%', 100), (4, '24%', 46), (3, '12%', 23), (2, '6%', 12), (1, '6%', 12)]   # widths as drawn (illustrative split)

E = lambda s: _h.escape(s, quote=True)
STAR_PATH = 'M10.4 0.866664L13.325 6.93331L19.9333 7.90831L15.1666 12.5666L16.25 19.1749L10.4 16.0333L4.55001 19.1749L5.63334 12.5666L0.866689 7.90831L7.475 6.93331L10.4 0.866664Z'
THUMB = ('<svg viewBox="0 0 12.2128 12.0661" fill="none" stroke="currentColor" stroke-width="1.125" stroke-linecap="round" stroke-linejoin="round" style="display:block;width:100%;height:100%;overflow:visible">'
         '<path d="M3.0625 5.25332V11.5033H1.1875C1.02174 11.5033 0.862768 11.4375 0.745558 11.3203C0.628348 11.2031 0.5625 11.0441 0.5625 10.8783V5.87832C0.5625 5.71256 0.628348 5.55359 0.745558 5.43638C0.862768 5.31917 1.02174 5.25332 1.1875 5.25332H3.0625Z"/>'
         '<path d="M3.0625 5.25332L5.5625 0.565819C5.78584 0.550617 6.00964 0.587784 6.21607 0.674359C6.42251 0.760935 6.60587 0.894525 6.75155 1.06449C6.89724 1.23445 7.00121 1.43609 7.05519 1.65333C7.10918 1.87058 7.11168 2.09743 7.0625 2.31582L6.5625 4.62832H10.375C10.5625 4.62452 10.7484 4.66295 10.919 4.74077C11.0896 4.81858 11.2405 4.93378 11.3606 5.07783C11.4806 5.22189 11.5667 5.3911 11.6125 5.57294C11.6583 5.75479 11.6625 5.9446 11.625 6.12832L10.6875 10.5033C10.6291 10.7899 10.472 11.0469 10.2436 11.2297C10.0152 11.4124 9.72993 11.5092 9.4375 11.5033H3.0625"/></svg>')


def ico(f, size, outer='0', inner=None, alt=''):
    im = f'<img alt="{alt}" src="assets/{f}" style="position:absolute;inset:0;display:block;max-width:none;width:100%;height:100%">'
    if inner:
        im = f'<div style="position:absolute;inset:{inner}">{im}</div>'
    return f'<div class="ico" style="position:relative;overflow:hidden;flex:none;width:{size}px;height:{size}px"><div style="position:absolute;inset:{outer}">{im}</div></div>'


INFO = lambda tip: f'<span class="d-tip" tabindex="0" data-tip="{E(tip)}" aria-label="{E(tip)}">{ico("dc-749d2.svg", 18, "12.5%", "-4.86%")}</span>'
CLOSE = f'<button type="button" class="drw-x" aria-label="Close">{ico("dc-c8626.svg", 18, "25%", "-8.33%")}</button>'
ARROW = ico('dc-6557e.svg', 14, '29.17%', '-10%')
FRESH = ico('dc-ffd6f.svg', 18, '0.25% 1.98% -0.01% 1.66%', alt='Fresh')
ROTTEN = ico('dc-2280e.svg', 18, '1.74% 0.32% 1.53% 0', alt='Rotten')
CERT = ico('dc-2beb9.svg', 18, alt='Certified Fresh')
POPCORN = ico('da-425c2.svg', 18, '0.16% 12.87% 0 12.63%', alt='Popcornmeter')
STAR_IN = '10.83% 10.83% 14.17% 10.83%'


def stars(n, size, on='da-c13e8.svg', off='da-4d804.svg'):
    return f'<div class="d-row" style="gap:2px" aria-label="{n} out of 5 stars">' + ''.join(ico(on if k < n else off, size, STAR_IN) for k in range(5)) + '</div>'


def fmt(n):
    return f'{n / 1000:.1f}K' if n >= 1000 else str(n)


# ---------------------------------------------------------------- critics
def critic_item(c):
    name, outlet, date, fresh, score, quote, top = c
    tag = '<span class="d-top">TOP CRITIC</span>' if top else ''
    sc = f'<span class="d-b14">{E(score)}</span>' if score else ''
    return f'''<article class="d-item" data-name="Review · {E(outlet)}">
  <div class="d-row d-between"><div class="d-row" style="gap:8px">{FRESH if fresh else ROTTEN}<span class="d-outlet">{E(outlet)}</span>{tag}</div>{sc}</div>
  <p class="d-quote">“{E(quote)}”</p>
  <div class="d-row d-between"><span class="d-meta">{E(name)} · {E(date)}</span><a href="#" class="d-full" data-outlet="{E(outlet)}">Full review{ARROW}</a></div>
</article>'''


def critics_drawer():
    lists = {
        'top': [c for c in CRITICS if c[6]],
        'fresh': [c for c in CRITICS if c[3]],
        'rotten': [c for c in CRITICS if not c[3]],
    }
    tabs = ''.join(f'<button type="button" role="tab" class="d-tab{" on" if k == "top" else ""}" data-tab="{k}" aria-selected="{"true" if k == "top" else "false"}">{lbl}</button>'
                   for k, lbl in [('top', 'Top Critics'), ('fresh', 'Fresh'), ('rotten', 'Rotten')])
    panes = ''.join(f'<div class="d-pane" data-pane="{k}" role="tabpanel"{"" if k == "top" else " hidden"}>{"".join(critic_item(c) for c in items)}</div>' for k, items in lists.items())
    return f'''<div id="drwCritics" class="drw" role="dialog" aria-modal="true" aria-labelledby="drwCriticsTitle" hidden>
<div class="drw-scrim"></div>
<aside class="drw-panel" data-name="Drawer · Critics reviews">
  <div class="drw-head">
    <div class="d-row d-between" style="align-items:flex-start">
      <div class="d-col" style="gap:8px">
        <div class="d-row" style="gap:8px"><h2 class="drw-title" id="drwCriticsTitle">Critics Reviews</h2>{INFO('Reviews from approved Tomatometer critics. Top Critics are a curated group of influential critics and outlets.')}</div>
        <div class="d-row" style="gap:6px">{CERT}<span class="d-b14">91% Tomatometer</span><span class="d-r14">472 reviews</span></div>
      </div>{CLOSE}</div>
    <div class="d-row d-between"><div class="d-seg" role="tablist" aria-label="Filter critics reviews">{tabs}</div></div>
  </div>
  <div class="drw-list">{panes}</div>
</aside></div>'''


# ---------------------------------------------------------------- audience
def audience_item(a):
    name, date, n, text, votes, color = a
    return f'''<article class="d-item" data-name="Audience review · {E(name)}">
  <div class="d-row d-between"><div class="d-row" style="gap:8px"><span class="d-av" style="background:{color}">{E(name[0].upper())}</span><span class="d-b14">{E(name)}</span>{stars(n, 13)}<span class="d-meta">{E(date)}</span></div>
    <button type="button" class="d-more" aria-label="More options">{ico("da-c9e5a.svg", 18, "45% 17.92%", "-45.83% -7.14%")}</button></div>
  <p class="d-text">{E(text)}</p>
  <div class="d-row" style="gap:16px"><button type="button" class="d-help" aria-pressed="false" data-n="{votes}" aria-label="Helpful"><span class="d-thumb">{THUMB}</span><span class="d-help-n">{fmt(votes)}</span></button>
    <div class="d-row" style="gap:4px">{ico("da-59758.svg", 14, "11.67% 15%", "-4.89% -5.36%")}<span class="d-meta">Verified</span></div></div>
</article>'''


def light_composer(cstars):
    return f'''<div data-name="Pinned composer" id="composerDrawer" class="composer light">
  <div class="c-row"><p class="c-title">What did you think of La La Land?</p>
    <div class="c-right"><span class="c-label" aria-live="polite"></span><div class="c-stars" role="radiogroup" aria-label="Rate La La Land">{cstars}</div></div></div>
  <div class="c-more" hidden>
    <textarea class="c-text" aria-label="Your review (optional)" placeholder="What stood out? The music, the performances, that ending… (optional)"></textarea>
    <div class="c-foot"><div class="c-ticket"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#666" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8.5V6a1 1 0 0 1 1-1h16a1 1 0 0 1 1 1v2.5a3.5 3.5 0 0 0 0 7V18a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1v-2.5a3.5 3.5 0 0 0 0-7z"/><path d="M14 5v14" stroke-dasharray="2 2.5"/></svg>Add your Fandango ticket to show <b>✓ Verified</b></div>
      <div class="c-actions"><button type="button" class="c-cancel">Cancel</button><button type="button" class="c-post" disabled>Post review</button></div></div>
  </div>
</div>'''


def audience_drawer():
    labels = ['Hated it', 'Didn’t like it', 'It was OK', 'Really liked it', 'Loved it']
    cstars = ''.join(f'<button type="button" class="cstar" role="radio" aria-checked="false" aria-label="{n} star{"s" if n > 1 else ""}, {labels[n - 1]}">'
                     f'<span style="position:absolute;inset:12.5% 13.33% 17.08% 13.33%"><span style="position:absolute;inset:-4.73% -4.55%"><svg viewBox="0 0 20.8 20.0416" fill="none" style="display:block;width:100%;height:100%;overflow:visible"><path d="{STAR_PATH}" stroke-width="1.73333" stroke-linecap="round" stroke-linejoin="round"/></svg></span></span></button>'
                     for n in range(1, 6))
    dist = ''.join(f'<div class="d-row" style="gap:8px"><span class="d-dl">{s}★</span><span class="d-track"><span style="width:{w}px"></span></span><span class="d-dp">{p}</span></div>' for s, p, w in DIST)
    big = '<div class="d-row" style="gap:2px" aria-label="4.1 out of 5 stars">' + ''.join(ico('da-e1325.svg' if k < 4 else 'da-a525c.svg', 16, STAR_IN) for k in range(5)) + '</div>'
    return f'''<div id="drwAudience" class="drw" role="dialog" aria-modal="true" aria-labelledby="drwAudienceTitle" hidden>
<div class="drw-scrim"></div>
<aside class="drw-panel" data-name="Drawer · Audience reviews">
  <div class="drw-head" style="padding-bottom:18px">
    <div class="d-row d-between" style="align-items:flex-start">
      <div class="d-col" style="gap:8px;flex:1">
        <div class="d-row" style="gap:8px"><h2 class="drw-title" id="drwAudienceTitle">Audience Reviews</h2>{INFO('Verified reviews come from people who bought a ticket through Fandango.')}</div>
        <div class="d-row" style="gap:6px">{POPCORN}<span class="d-b14">82% Popcornmeter</span><span class="d-r14">50,000+ verified ratings</span></div>
      </div>{CLOSE}</div>
    <div class="d-row" style="gap:24px;align-items:flex-start" data-name="Rating summary">
      <div class="d-col" style="gap:8px;align-items:center;justify-content:center"><span class="d-avg">4.1</span><div class="d-col" style="gap:2px">{big}<span class="d-meta">average rating</span></div></div>
      <div class="d-col" style="gap:4px" data-name="Distribution">{dist}</div></div>
  </div>
  <div class="drw-list">{"".join(audience_item(a) for a in AUDIENCE)}</div>
  {light_composer(cstars)}
</aside></div>'''


CSS = r'''
/* ---- review drawers (light panels for long reading) ---- */
html{scrollbar-gutter:stable}
.drw{position:fixed;inset:0;z-index:80}
.drw[hidden]{display:none}
.drw-scrim{position:absolute;inset:0;background:rgba(8,7,12,.58);opacity:0;transition:opacity 260ms ease}
.drw-panel{position:absolute;right:0;top:0;width:600px;height:calc(100vh / var(--z,1));zoom:var(--z,1);background:#fff;display:flex;flex-direction:column;
  filter:drop-shadow(-24px 0 30px rgba(0,0,0,.35));transform:translateX(100%);transition:transform 340ms cubic-bezier(.2,.7,.1,1);font-family:Arial,Helvetica,sans-serif;color:#000}
.drw.on .drw-scrim{opacity:1}
.drw.on .drw-panel{transform:none}
.drw-head{display:flex;flex-direction:column;gap:18px;padding:24px 32px 0;flex:none}
.drw-title{font:700 26px/30px Arial,Helvetica,sans-serif;margin:0;white-space:nowrap}
.drw-x{width:40px;height:40px;border-radius:20px;background:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer;flex:none;transition:background 140ms}
.drw-x:hover{background:#F4F4F4}
.drw-list{flex:1;min-height:0;overflow-y:auto;overscroll-behavior:contain;padding:0 32px}
.d-row{display:flex;align-items:center}
.d-col{display:flex;flex-direction:column;align-items:flex-start}
.d-between{justify-content:space-between;width:100%}
.d-b14{font:700 14px/16px Arial,Helvetica,sans-serif;color:#000;white-space:nowrap}
.d-r14{font:400 14px/16px Arial,Helvetica,sans-serif;color:#666;white-space:nowrap}
.d-meta{font:400 13px/16px Arial,Helvetica,sans-serif;color:#666;white-space:nowrap}
.d-seg{display:flex;gap:2px;border-radius:10px;background:rgba(102,102,102,.06)}
.d-tab{height:32px;padding:0 14px;border-radius:8px;border:1px solid transparent;background:transparent;font:500 14px/16px Arial,Helvetica,sans-serif;color:rgba(102,102,102,.6);cursor:pointer;white-space:nowrap;transition:color 140ms}
.d-tab:hover{color:#1b1c2a}
.d-tab.on{background:rgba(255,255,255,.92);border-color:rgba(0,0,0,.2);box-shadow:0 0 4px rgba(0,0,0,.05);color:#1b1c2a}
.d-item{display:flex;flex-direction:column;align-items:flex-start;gap:10px;padding:20px 0;border-bottom:1px solid #e6e6e6}
.d-outlet{font:700 15px/18px Arial,Helvetica,sans-serif;white-space:nowrap}
.d-top{font:700 10px/12px Arial,Helvetica,sans-serif;letter-spacing:.6px;color:#d42a07;background:#ffede8;padding:3px 6px;border-radius:4px;white-space:nowrap}
.d-quote{margin:0;font:400 17px/26px Arial,Helvetica,sans-serif;color:#1a1a1a;width:536px}
.d-text{margin:0;font:400 16px/25px Arial,Helvetica,sans-serif;color:#1a1a1a;width:100%}
.d-full{display:flex;align-items:center;gap:6px;font:700 13px/16px Arial,Helvetica,sans-serif;color:#000;text-decoration:none;white-space:nowrap}
.d-full:hover{text-decoration:underline;text-underline-offset:3px}
.d-av{width:28px;height:28px;border-radius:14px;display:flex;align-items:center;justify-content:center;font:700 10px/10px Arial,Helvetica,sans-serif;color:#fff;flex:none}
.d-more{width:18px;height:18px;padding:0;background:none;cursor:pointer;opacity:.9}
.d-more:hover{opacity:.6}
.d-help{display:flex;align-items:center;gap:6px;padding:0;background:none;cursor:pointer;color:#4d4d4d;font:700 13px/16px Arial,Helvetica,sans-serif}
.d-thumb{position:relative;width:15px;height:15px;display:block;flex:none}
.d-thumb svg{position:absolute;left:12.5%;top:12.48%;width:73.92% !important;height:72.94% !important}
.d-help:hover{color:#000}
.d-help.on{color:#d42a07}
.d-avg{font:700 30px/32px Arial,Helvetica,sans-serif;white-space:nowrap}
.d-dl{width:24px;text-align:right;font:700 12px/14px Arial,Helvetica,sans-serif;color:rgba(102,102,102,.6)}
.d-dp{width:32px;font:400 12px/14px Arial,Helvetica,sans-serif;color:rgba(102,102,102,.6)}
.d-track{display:block;width:192px;height:8px;border-radius:4px;background:rgba(102,102,102,.06);overflow:hidden}
.d-track span{display:block;height:8px;border-radius:4px;background:#ffb600}
.d-tip{position:relative;display:inline-flex;cursor:help;border-radius:9px}
.d-tip:hover::after,.d-tip:focus::after{content:attr(data-tip);position:absolute;left:50%;top:26px;transform:translateX(-50%);width:280px;padding:12px 14px;border-radius:12px;background:#0B0B0C;color:#F6F1E7;
  font:400 13px/19px Arial,Helvetica,sans-serif;box-shadow:0 12px 28px rgba(0,0,0,.3);z-index:5;white-space:normal}
.drw button:focus-visible,.drw a:focus-visible,.d-tip:focus-visible{outline:2px solid #000;outline-offset:3px}
.d-pane.fade{animation:fade 220ms ease both}
/* the pinned rate-first composer, light version of the page composer */
.composer.light{flex:none;background:#fafafa;border:0;border-top:1px solid #e6e6e6;border-radius:0;padding:16px 32px 20px}
.composer.light.open{gap:14px;padding-bottom:20px}
.composer.light .c-title{font:700 16px/20px Arial,Helvetica,sans-serif;color:#000}
.composer.light .c-stars{gap:4px}
.composer.light .cstar{position:relative;width:26px;height:26px}
.composer.light .cstar path{fill:transparent;stroke:#BFBFBF}
.composer.light .cstar.on path{fill:#FFB600;stroke:#FFB600}
.composer.light .c-label{color:#4d4d4d}
.composer.light .c-text{height:96px;background:#fff;border:1px solid #d9d9d9;color:#1a1a1a}
.composer.light .c-text::placeholder{color:#666}
.composer.light .c-text:focus{border-color:#000}
.composer.light .c-ticket{color:#666}
.composer.light .c-ticket b{color:#1a1a1a}
.composer.light .c-cancel{color:#4d4d4d}
.composer.light .c-cancel:hover{color:#000}
.composer.light .c-post{background:#d42a07;color:#fff}
.composer.light .cstar:focus-visible,.composer.light .c-cancel:focus-visible,.composer.light .c-post:focus-visible{outline-color:#000}
@media (prefers-reduced-motion: reduce){.drw-panel,.drw-scrim{transition:none!important}}
'''

JS = r'''
/* ---------------- review drawers ---------------- */
const drawers = { critics: document.getElementById('drwCritics'), audience: document.getElementById('drwAudience') };
let openDrw = null, drwReturn = null;
function showDrawer(key) {
  const d = drawers[key]; if (!d || openDrw === d) return;
  if (openDrw) hideDrawer(true);
  drwReturn = document.activeElement; d.hidden = false; openDrw = d;
  document.documentElement.style.overflow = 'hidden';
  requestAnimationFrame(() => requestAnimationFrame(() => d.classList.add('on')));
  setTimeout(() => d.querySelector('.drw-x').focus({ preventScroll: true }), 60);
}
function hideDrawer(instant) {
  const d = openDrw; if (!d) return;
  openDrw = null; d.classList.remove('on'); document.documentElement.style.overflow = '';
  setTimeout(() => { if (openDrw !== d) d.hidden = true; }, instant || reduce ? 0 : 340);
  if (drwReturn && !instant) drwReturn.focus({ preventScroll: true });
}
Object.values(drawers).forEach(d => {
  d.querySelector('.drw-scrim').addEventListener('click', () => hideDrawer());
  d.querySelector('.drw-x').addEventListener('click', () => hideDrawer());
  d.addEventListener('keydown', e => {
    if (e.key === 'Escape') { e.preventDefault(); hideDrawer(); }
    if (e.key === 'Tab') {   // keep focus inside the drawer
      const f = [...d.querySelectorAll('button:not(:disabled), a[href], textarea, [tabindex="0"]')].filter(el => el.offsetParent !== null);
      const a = f[0], z = f[f.length - 1];
      if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus(); }
      else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus(); }
    }
  });
  d.querySelectorAll('.d-full').forEach(a => a.addEventListener('click', e => { e.preventDefault(); toast(`Opens the full review on ${a.dataset.outlet}`); }));
});
// critics tabs filter the list
const dTabs = [...drawers.critics.querySelectorAll('.d-tab')];
dTabs.forEach(t => t.addEventListener('click', () => {
  dTabs.forEach(o => { o.classList.toggle('on', o === t); o.setAttribute('aria-selected', String(o === t)); });
  drawers.critics.querySelectorAll('.d-pane').forEach(p => { const on = p.dataset.pane === t.dataset.tab; p.hidden = !on; if (on) { p.classList.remove('fade'); void p.offsetWidth; p.classList.add('fade'); } });
  drawers.critics.querySelector('.drw-list').scrollTop = 0;
}));
dTabs.forEach((t, i) => t.addEventListener('keydown', e => {
  const d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0; if (!d) return;
  e.preventDefault(); const n = dTabs[(i + d + dTabs.length) % dTabs.length]; n.focus(); n.click();
}));
// helpful votes
drawers.audience.querySelectorAll('.d-help').forEach(b => b.addEventListener('click', () => {
  const on = !b.classList.contains('on'); b.classList.toggle('on', on); b.setAttribute('aria-pressed', String(on));
  const n = +b.dataset.n + (on ? 1 : 0); b.querySelector('.d-help-n').textContent = n >= 1000 ? (n / 1000).toFixed(1) + 'K' : n;
}));
drawers.audience.querySelectorAll('.d-more').forEach(b => b.addEventListener('click', () => toast('Share or report this review')));
// entry points on the film page
const openOn = (texts, key) => $$('#stage p').filter(p => texts.includes(p.textContent.trim())).forEach(p => {
  let el = p;   // climb to the smallest wrapper that holds only this link (text plus its chevron)
  while (el.parentElement && el.parentElement.id !== 'stage' && el.parentElement.textContent.trim() === p.textContent.trim()) el = el.parentElement;
  ix(el, () => showDrawer(key), texts[0] === 'All 472' ? 'All critics reviews' : 'All audience reviews');
});
openOn(['All 472'], 'critics');
openOn(['All 50,000+', 'Read all audience reviews'], 'audience');
'''
