"""Interactive prototype of the Arial · B page (Figma 139:4722 + sticky header 139:6643, Leave-a-review option D as refined in 147:6789).

Markup is converted 1:1 from Figma's design context (convert.py); this file adds the interaction layer.
Run: python3 proto2/build.py
"""
import os, re, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from convert import convert
import drawers
import theater
from convert import jsx_to_html

STAR = '<path d="m12 2.8 2.84 5.76 6.36.92-4.6 4.49 1.09 6.33L12 17.31l-5.69 2.99 1.09-6.33-4.6-4.49 6.36-.92z"/>'
LABELS = ['Hated it', "Didn't like it", 'It was OK', 'Really liked it', 'Loved it']
CSTARS = ''.join(f'<button type="button" class="cstar" role="radio" aria-checked="false" aria-label="{n} star{'s' if n > 1 else ''}, {LABELS[n - 1]}"><svg viewBox="0 0 24 24">{STAR}</svg></button>' for n in range(1, 6))
TICKET = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,.75)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
          '<path d="M3 8.5V6a1 1 0 0 1 1-1h16a1 1 0 0 1 1 1v2.5a3.5 3.5 0 0 0 0 7V18a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1v-2.5a3.5 3.5 0 0 0 0-7z"/><path d="M14 5v14" stroke-dasharray="2 2.5"/></svg>')
COMPOSER = f'''<div data-name="Rate &amp; review composer · spacing" style="padding-top:22px;width:100%;flex-shrink:0">
<div data-name="Rate &amp; review composer" id="composer" class="composer">
  <div class="c-row"><p class="c-title">What did you think of La La Land?</p>
    <div class="c-right"><span class="c-label" aria-live="polite"></span><div class="c-stars" role="radiogroup" aria-label="Rate La La Land">{{STARS}}</div></div></div>
  <div class="c-more" hidden>
    <textarea class="c-text" aria-label="Your review (optional)" placeholder="What stood out? The music, the performances, that ending… (optional)"></textarea>
    <div class="c-foot"><div class="c-ticket">{TICKET}Add your Fandango ticket to show <b>✓ Verified</b></div>
      <div class="c-actions"><button type="button" class="c-cancel">Cancel</button><button type="button" class="c-post" disabled>Post review</button></div></div>
  </div>
</div></div>'''

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# the page background deepens again behind the footer, mirroring the two layers behind the header
END_LAYERS = ('<div data-name="Rectangle 3" style="position:absolute;left:0;bottom:0;width:1440px;height:155px;background:#000;opacity:.5;pointer-events:none"></div>'
              '<div data-name="Rectangle 4" style="position:absolute;left:0;bottom:155px;width:1440px;height:308px;background:linear-gradient(to top,#000,rgba(0,0,0,0));opacity:.5;pointer-events:none"></div>')

AUDIENCE_FULL = {
    'First L': 'I was thrilled that they brought this masterpiece back to Dolby Cinema for 10th Anniversary. It was every bit as powerful and emotional as the first time that I saw it 10 years ago. Ryan & Emmas chemistry is legendary!',
    'Venus': "One of THE BEST movies of all time with musical scores, acting, and story line. Doesn't matter how many times I have seen this movie, it breaks me every time (and I don't even care for musicals I'm extremely picky!)",
    'Zaahir': 'Amazing cinematography and seeing it in Dolby made me appreciate this film more. Ryan Gosling was a standout, some of the songs dragged on a bit but overall great movie and certainly lived up to the hype.',
}

TIPS = {
    'tomatometer': ('Tomatometer', 'The share of approved critics who gave La La Land a positive review: 428 of 472 reviews are Fresh. Certified Fresh.'),
    'popcornmeter': ('Popcornmeter', 'The share of verified audience members who rated La La Land 3.5 stars or higher, from 50,000+ ratings.'),
    'critics': ('Critics Reviews', 'Reviews from approved Tomatometer critics. Top Critics are a curated group of influential critics and outlets.'),
    'audience': ('Audience Reviews', 'Verified reviews come from people who bought a ticket through Fandango.'),
}

CSS = r'''
*,::before,::after{box-sizing:border-box;border:0 solid #e5e7eb;margin:0;padding:0}
img,svg{display:block;max-width:100%;height:auto}
html{scroll-behavior:auto}
html,body{margin:0;background:#222646}
body{font-family:Arial,Helvetica,sans-serif;-webkit-font-smoothing:antialiased;overflow-x:hidden;
  background:linear-gradient(#111323 0, #111323 calc(864px * var(--z,1)), #222646 calc(1172px * var(--z,1)), #222646 calc(100% - 463px * var(--z,1)), #111323 calc(100% - 155px * var(--z,1)), #111323 100%)}
#stage{width:1440px;margin:0 auto;zoom:var(--z,1);position:relative}

/* ---- hero: film-strip parallax ---- */
#heroInner{position:absolute;inset:0;will-change:transform}
#heroDim{position:absolute;inset:0;background:#08070c;opacity:0;pointer-events:none}
.kb{animation:kb 24s ease-in-out infinite alternate;transform-origin:58% 44%}
.paused .kb{animation-play-state:paused}
@keyframes kb{from{transform:scale(1)}to{transform:scale(1.06)}}

/* ---- sticky header ---- */
#sticky{position:fixed;left:0;right:0;top:0;z-index:50;background:#1d203c;border-bottom:1px solid rgba(255,255,255,0.08);
  transform:translateY(-101%);transition:transform 320ms cubic-bezier(.2,.7,.1,1),box-shadow 320ms;}
#sticky.on{transform:translateY(0);box-shadow:0 10px 30px rgba(5,6,16,0.35)}
#stickyInner{width:1440px;margin:0 auto;zoom:var(--z,1)}
#stickyInner [data-node-id="139:6644"]{border-bottom-width:0!important}
.navlink p{transition:color 160ms}
.navlink:hover p{color:#fff!important}

/* ---- affordances ---- */
[data-ix]{cursor:pointer}
[data-ix]:focus-visible{outline:2px solid #fff;outline-offset:3px;border-radius:8px}
.btn-lift{transition:transform 160ms, filter 160ms, background-color 160ms}
.btn-lift:hover{filter:brightness(1.12)}
.btn-lift:active{transform:scale(.97)}
.hover-dim{transition:opacity 160ms}
.hover-dim:hover{opacity:.75}
.zoomable img{transition:transform 420ms cubic-bezier(.2,.7,.1,1)}
.zoomable:hover img{transform:scale(1.05)}
.lift{transition:transform 220ms cubic-bezier(.2,.7,.1,1)}
.lift:hover{transform:translateY(-4px)}
.pulse{animation:pulse 1.2s ease-out 2}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(250,50,10,.7)}100%{box-shadow:0 0 0 14px rgba(250,50,10,0)}}
.ctl-on{background:rgba(246,241,231,0.18);border-radius:6px}
.fade{animation:fade 260ms ease both}
@keyframes fade{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}

/* ---- tooltip / toast ---- */
#tip{position:absolute;top:0;left:0;z-index:40;width:300px;padding:14px 16px;border-radius:12px;background:#0B0B0C;color:#F6F1E7;
  box-shadow:0 12px 28px rgba(0,0,0,0.35);pointer-events:none;opacity:0;transform:translateY(4px);transition:opacity 140ms, transform 140ms}
#tip.on{opacity:1;transform:none}
#tip b{display:block;font-size:14px;line-height:18px;margin-bottom:6px}
#tip span{display:block;font-size:13px;line-height:19px;color:rgba(246,241,231,0.78)}
#toast{position:fixed;left:50%;bottom:28px;z-index:60;transform:translate(-50%,20px);opacity:0;pointer-events:none;
  background:#F6F1E7;color:#1B1C2A;font:700 14px/18px Arial,Helvetica,sans-serif;padding:12px 16px;border-radius:10px;box-shadow:0 12px 28px rgba(0,0,0,.35);transition:opacity 200ms, transform 200ms}
#toast.on{opacity:1;transform:translate(-50%,0)}

/* ---- rate & review: inline composer (option D, Figma 157:201) ---- */
.composer{display:flex;flex-direction:column;padding:18px 20px;border-radius:12px;background:rgba(246,241,231,.05);border:1px solid rgba(246,241,231,.1);transition:border-color 160ms}
.composer.open{gap:16px;padding-bottom:20px;border-color:rgba(246,241,231,.16)}
.c-row{display:flex;justify-content:space-between;align-items:center}
.c-title{font:700 17px/20px Arial,Helvetica,sans-serif;color:#fff;white-space:nowrap}
.c-right{display:flex;align-items:center;gap:14px}
.c-label{font:700 14px/18px Arial,Helvetica,sans-serif;color:#FFD700;white-space:nowrap}
.c-stars{display:flex;gap:6px}
.cstar{width:28px;height:28px;padding:0;background:none;cursor:pointer;border-radius:6px;transition:transform 120ms}
.cstar:hover{transform:scale(1.1)}
.cstar svg{display:block;width:28px;height:28px}
.cstar path{fill:transparent;stroke:rgba(255,255,255,.45);stroke-width:1.6;stroke-linejoin:round;transition:fill 120ms, stroke 120ms}
.cstar.on path{fill:#FFD700;stroke:#FFD700}
.cstar:focus-visible,.c-cancel:focus-visible,.c-post:focus-visible{outline:2px solid #fff;outline-offset:3px}
.c-more{display:flex;flex-direction:column;gap:16px}
.c-more[hidden]{display:none}
.c-text{width:100%;height:116px;resize:none;border-radius:10px;background:rgba(8,7,12,.22);border:1px solid rgba(246,241,231,.18);padding:14px 16px;
  font:400 16px/24px Arial,Helvetica,sans-serif;color:#fff;outline:none}
.c-text::placeholder{color:rgba(255,255,255,.45)}
.c-text:focus{border-color:rgba(246,241,231,.5)}
.c-foot{display:flex;justify-content:space-between;align-items:center}
.c-ticket{display:flex;align-items:center;gap:8px;white-space:nowrap;font:400 14px/18px Arial,Helvetica,sans-serif;color:rgba(255,255,255,.6)}
.c-ticket b{color:rgba(255,255,255,.85)}
.c-actions{display:flex;align-items:center;gap:18px;white-space:nowrap}
.c-cancel{font:700 15px/18px Arial,Helvetica,sans-serif;color:rgba(255,255,255,.7);cursor:pointer;background:none}
.c-cancel:hover{color:#fff}
.c-post{height:42px;padding:0 18px;border-radius:8px;background:#fff;color:#1B1C2A;font:700 16px/20px Arial,Helvetica,sans-serif;cursor:pointer;transition:opacity 160ms, filter 160ms}
.c-post:disabled{opacity:.4;cursor:not-allowed}
.c-post:not(:disabled):hover{filter:brightness(.94)}

@media (prefers-reduced-motion: reduce){
  .kb,.pulse,.fade{animation:none!important}
  #sticky,.zoomable img,.lift,.cstar,.composer{transition:none!important}
}
'''

JS = r'''
(() => {
const $ = (id, root = document) => root.querySelector(`[data-node-id="${id}"]`);
const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
const stage = document.getElementById('stage');
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
let Z = 1;
const fit = () => { Z = Math.min(1, innerWidth / 1440); document.documentElement.style.setProperty('--z', Z); };
fit(); addEventListener('resize', () => { fit(); tick(); });

const leaf = (root, text) => $$('p, span', root).find(e => e.children.length === 0 && e.textContent.trim() === text);
const setText = (root, from, to) => { const e = leaf(root, from); if (e) e.textContent = to; return e; };
const ix = (el, fn, label) => {
  if (!el) return; el.setAttribute('data-ix', ''); el.tabIndex = 0; el.setAttribute('role', 'button');
  if (label) el.setAttribute('aria-label', label);
  el.addEventListener('click', fn);
  el.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); fn(e); } });
};
const toastEl = document.getElementById('toast'); let toastT;
const toast = msg => { toastEl.textContent = msg; toastEl.classList.add('on'); clearTimeout(toastT); toastT = setTimeout(() => toastEl.classList.remove('on'), 1800); };
const SVG = {
  soundOn: '<svg viewBox="0 0 24 24" width="100%" height="100%" fill="none" stroke="#F6F1E7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5 6 9H2v6h4l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/><path d="M19 5a10 10 0 0 1 0 14"/></svg>',
  play: '<svg viewBox="0 0 24 24" width="100%" height="100%"><path d="M7 4.5v15l12.5-7.5z" fill="#F6F1E7"/></svg>',
  check: '<svg viewBox="0 0 24 24" width="100%" height="100%" fill="none" stroke="#F6F1E7" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>',
  starOn: '<svg viewBox="0 0 24 24" width="100%" height="100%"><path d="m12 2.8 2.84 5.76 6.36.92-4.6 4.49 1.09 6.33L12 17.31l-5.69 2.99 1.09-6.33-4.6-4.49 6.36-.92z" fill="#FFD700"/></svg>',
};

/* ---------------- hero: content travels slower than the frame ---------------- */
const hero = $('139:4746');
// one clip for everything inside the frame (cover, video, scrims): composited layers can't each snap their own rounded clip
hero.style.isolation = 'isolate'; hero.style.clipPath = 'inset(0 round 24px)';
const inner = document.createElement('div'); inner.id = 'heroInner';
while (hero.firstChild) inner.appendChild(hero.firstChild);
hero.appendChild(inner);
const dim = document.createElement('div'); dim.id = 'heroDim'; hero.appendChild(dim);
const still = $('139:4747').querySelector('img');   // the cover: sits on top of the video until the first frame is on screen
const LAG = 0.38;   // content moves at 62% of the frame's speed once the frame reaches the top of the viewport

/* ---------------- sticky header ---------------- */
const sticky = document.getElementById('sticky');
// page order: Where to Watch sits above the synopsis, so it leads the nav
$('139:6753', sticky).insertBefore($('139:6758', sticky), $('139:6754', sticky));
const NAV = [['139:6758', ['139:4980'], 'Where to Watch'], ['139:6754', ['139:5017'], 'Overview'], ['139:6756', ['139:6080', '139:5660'], 'Reviews'],
             ['139:6760', ['139:5838'], 'Cast'], ['139:6762', ['139:5897'], 'Media'], ['139:6764', ['139:5925'], 'More']];
const scrollToEl = el => { const y = el.getBoundingClientRect().top + scrollY - (72 + 20) * Z; scrollTo({ top: Math.max(0, y), behavior: reduce ? 'auto' : 'smooth' }); };
NAV.forEach(([id, targets, label]) => {
  const link = $(id, sticky); link.classList.add('navlink');
  ix(link, () => scrollToEl($(targets[0])), label);
});
const setActive = label => NAV.forEach(([id, , l]) => {
  const link = $(id, sticky); const p = link.querySelector('p');
  link.classList.toggle('active', l === label); p.style.color = l === label ? '#ffffff' : 'rgba(255,255,255,0.6)';
});
const goWatch = () => { const row = $('139:4980'); scrollToEl(row); const chip = $('139:4985'); setTimeout(() => { chip.classList.remove('pulse'); void chip.offsetWidth; chip.classList.add('pulse'); }, reduce ? 0 : 450); };
ix($('139:6766', sticky), goWatch, 'Rent from $3.99'); $('139:6766', sticky).classList.add('btn-lift');
ix($('139:6645', sticky), () => scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }), 'Back to top');

function tick() {
  const r = hero.getBoundingClientRect();
  const passed = Math.max(0, -r.top) / Z;                 // design px the frame has travelled above the viewport
  const travel = Math.min(passed, 760);
  inner.style.transform = reduce ? '' : `translate3d(0, ${(travel * LAG).toFixed(2)}px, 0)`;
  dim.style.opacity = reduce ? 0 : (Math.min(1, travel / 760) * 0.5).toFixed(3);
  const show = r.bottom <= 72 * Z + 1;
  sticky.classList.toggle('on', show);
  sticky.setAttribute('aria-hidden', show ? 'false' : 'true');
  // scrollspy: last section whose top is above the nav line
  const line = 72 * Z + 40 * Z;
  let cur = 'Where to Watch', best = -Infinity;
  NAV.forEach(([, targets, label]) => targets.forEach(t => { const top = $(t).getBoundingClientRect().top; if (top <= line && top > best) { best = top; cur = label; } }));
  setActive(cur);
}
let raf = 0; addEventListener('scroll', () => { if (!raf) raf = requestAnimationFrame(() => { raf = 0; tick(); }); }, { passive: true });

/* ---------------- trailer: real video (City of Stars teaser) over the poster still ---------------- */
// The teaser is letterboxed (active picture 1920×796 at y=142). Scale that picture to cover the 1376×760 frame.
const SRC_W = 1920, SRC_H = 1080, PIC_H = 796, PIC_Y = 142, FW = 1376, FH = 760, START = 4;
const BLEED = 4;   // the picture overshoots every edge of the frame, so GPU pixel snapping at any zoom never opens a seam
const k = Math.max((FW + 2 * BLEED) / SRC_W, (FH + 2 * BLEED) / PIC_H);
const video = document.createElement('video');
Object.assign(video, { src: 'assets/trailer-city-of-stars-1440p.mp4', muted: true, playsInline: true, preload: 'auto' });
video.setAttribute('muted', ''); video.setAttribute('playsinline', ''); video.setAttribute('aria-label', 'La La Land teaser trailer, City of Stars');
video.style.cssText = `position:absolute;width:${(SRC_W * k).toFixed(1)}px;height:${(SRC_H * k).toFixed(1)}px;left:${((FW - SRC_W * k) / 2).toFixed(1)}px;top:${((FH - PIC_H * k) / 2 - PIC_Y * k).toFixed(1)}px;max-width:none`;
$('139:4747').insertBefore(video, still);   // video underneath, cover above
let soundOn = false, cc = false, userPaused = reduce, inView = true;
const BAR = 320;
const bar = $('139:4955'), clock = $('139:4966');
const fmt = n => `${Math.floor(n / 60)}:${String(Math.floor(n % 60)).padStart(2, '0')}`;
const render = () => { const d = video.duration || 86, c = video.currentTime || 0; bar.style.width = (BAR * c / d).toFixed(1) + 'px'; clock.textContent = `${fmt(c)} / ${fmt(d)}`; };
const pauseBtn = $('139:4968'); const pauseIcon = pauseBtn.innerHTML;
const syncPlayUi = () => { const playing = !video.paused; pauseBtn.innerHTML = playing ? pauseIcon : SVG.play; hero.classList.toggle('paused', !playing); pauseBtn.setAttribute('aria-label', playing ? 'Pause trailer' : 'Play trailer'); };
const tryPlay = () => { if (!userPaused && inView) video.play().catch(() => syncPlayUi()); };
video.addEventListener('loadedmetadata', () => { video.currentTime = START; render(); tryPlay(); });
video.addEventListener('playing', syncPlayUi);
// reveal: wait until a real frame has been painted, then fade the cover away (nothing bright ever sits under a translucent video)
let revealed = false;
const reveal = () => {
  if (revealed || !still) return; revealed = true;
  still.style.transition = 'opacity 900ms ease'; still.style.opacity = '0';
  still.addEventListener('transitionend', () => { still.style.visibility = 'hidden'; }, { once: true });
};
video.addEventListener('playing', () => {
  if (video.requestVideoFrameCallback) video.requestVideoFrameCallback(() => requestAnimationFrame(reveal));
  else setTimeout(reveal, 120);
});
video.addEventListener('pause', syncPlayUi);
video.addEventListener('timeupdate', render);
video.addEventListener('ended', () => { video.currentTime = START; tryPlay(); });
// save bandwidth and battery: pause while the hero is off screen, resume when it returns (unless the viewer paused it)
new IntersectionObserver(es => { if (theaterOn) return; inView = es[0].isIntersecting; if (!inView && !video.paused) video.pause(); else tryPlay(); }, { threshold: 0.15 }).observe(hero);
const unmute = $('139:4958'), soundIcon = $('139:4959'), soundText = $('139:4964'); const soundOff = soundIcon.innerHTML;
ix(unmute, () => { soundOn = !soundOn; video.muted = !soundOn; soundIcon.innerHTML = soundOn ? SVG.soundOn : soundOff; soundText.textContent = soundOn ? 'Sound on' : 'Sound off'; if (soundOn && video.paused) { userPaused = false; tryPlay(); } }, 'Toggle sound');
unmute.classList.add('btn-lift');
ix(pauseBtn, () => { if (video.paused) { userPaused = false; video.play(); } else { userPaused = true; video.pause(); } }, 'Pause trailer');
const ccBtn = $('139:4972'); ix(ccBtn, () => { cc = !cc; ccBtn.classList.toggle('ctl-on', cc); toast(cc ? 'Captions aren’t available for this teaser' : 'Captions off'); }, 'Captions');
const fsBtn = $('139:4976'); ix(fsBtn, () => enterTheater(), 'Full screen');
[pauseBtn, ccBtn, fsBtn].forEach(b => b.classList.add('hover-dim'));
const progress = $('139:4954'); progress.style.cursor = 'pointer';
progress.addEventListener('click', e => { const r = progress.getBoundingClientRect(); if (video.duration) { video.currentTime = video.duration * (e.clientX - r.left) / r.width; render(); } });
syncPlayUi();

/* ---------------- hero actions ---------------- */
const rent = $('139:4775'); ix(rent, goWatch, 'Rent from $3.99'); rent.classList.add('btn-lift');
const wl = $('139:4781'), wlIcon = $('139:4782'), wlIconOff = wlIcon.innerHTML; let inList = false;
const wlText = leaf(wl, 'Watchlist');
ix(wl, () => { inList = !inList; wlIcon.innerHTML = inList ? SVG.check : wlIconOff; wlText.textContent = inList ? 'In Watchlist' : 'Watchlist'; toast(inList ? 'Added to your Watchlist' : 'Removed from your Watchlist'); }, 'Add to Watchlist');
wl.classList.add('btn-lift');
const rate = $('139:6774'); const rateIconWrap = rate.firstElementChild;
ix(rate, () => goRate(), 'Rate and review');
rate.classList.add('btn-lift');

/* ---------------- rate & review: one shared review, two composers (page + audience drawer) ---------------- */
const LABELS = ['', 'Hated it', "Didn't like it", 'It was OK', 'Really liked it', 'Loved it'];
const ASK = 'What did you think of La La Land?';
const review = { rating: 0, text: '', posted: false };
const composers = [];
function Composer(root) {
  const stars = [...root.querySelectorAll('.cstar')], label = root.querySelector('.c-label'), title = root.querySelector('.c-title');
  const more = root.querySelector('.c-more'), text = root.querySelector('.c-text'), post = root.querySelector('.c-post'), cancel = root.querySelector('.c-cancel');
  let rating = 0, isOpen = false;
  const paint = n => { stars.forEach((b, i) => { b.classList.toggle('on', i < n); b.setAttribute('aria-checked', String(i + 1 === rating)); }); label.textContent = LABELS[n] || ''; };
  const open = () => {
    post.disabled = !rating;
    if (isOpen) return;
    isOpen = true; root.classList.add('open'); more.hidden = false;
    more.classList.remove('fade'); void more.offsetWidth; more.classList.add('fade');
    title.textContent = review.posted ? 'Edit your review' : ASK;
    text.value = review.posted ? review.text : text.value;
    post.textContent = review.posted ? 'Update review' : 'Post review';
    setTimeout(() => text.focus({ preventScroll: true }), 60);
  };
  const close = () => {
    isOpen = false; root.classList.remove('open'); more.hidden = true;
    if (review.posted) { rating = review.rating; title.textContent = 'Your rating'; } else { rating = 0; title.textContent = ASK; text.value = ''; }
    paint(rating);
  };
  stars.forEach((b, i) => {
    b.addEventListener('mouseenter', () => paint(i + 1));
    b.addEventListener('click', () => { rating = i + 1; paint(rating); open(); });
    b.addEventListener('keydown', e => {
      const d = (e.key === 'ArrowRight' || e.key === 'ArrowUp') ? 1 : (e.key === 'ArrowLeft' || e.key === 'ArrowDown') ? -1 : 0;
      if (!d) return; e.preventDefault();
      const n = Math.min(5, Math.max(1, (rating || (d > 0 ? 0 : 2)) + d)); rating = n; paint(n); stars[n - 1].focus();
      if (isOpen) post.disabled = false;
    });
  });
  root.querySelector('.c-stars').addEventListener('mouseleave', () => paint(rating));
  cancel.addEventListener('click', () => { close(); stars[Math.max(0, rating - 1)].focus(); });
  root.addEventListener('keydown', e => { if (e.key === 'Escape' && isOpen) { e.stopPropagation(); close(); stars[Math.max(0, rating - 1)].focus(); } });
  post.addEventListener('click', () => {
    if (!rating) return;
    const first = !review.posted;
    Object.assign(review, { rating, text: text.value.trim(), posted: true });
    composers.forEach(c => c.close());
    toast(first ? 'Thanks! Your review is posted' : 'Review updated');
    rateIconWrap.innerHTML = SVG.starOn;
  });
  const api = { root, close, focus: () => stars[Math.max(0, rating - 1)].focus({ preventScroll: true }) };
  composers.push(api); paint(0); return api;
}
const pageComposer = Composer(document.getElementById('composer'));
Composer(document.getElementById('composerDrawer'));
const comp = pageComposer.root;
// the hero ☆ Rate button leads to the page composer
function goRate() {
  const y = comp.getBoundingClientRect().top + scrollY - innerHeight / 2 + comp.offsetHeight * Z / 2;
  scrollTo({ top: Math.max(0, y), behavior: reduce ? 'auto' : 'smooth' });
  setTimeout(() => { comp.classList.remove('pulse'); void comp.offsetWidth; comp.classList.add('pulse'); pageComposer.focus(); }, reduce ? 0 : 500);
}

/* ---------------- tooltips on info icons ---------------- */
const TIPS = __TIPS__;
const tip = document.getElementById('tip');
const infoFor = (root, label) => {
  const c = $$('[data-name="Icon"]', root).filter(ic => ic.parentElement && [...ic.parentElement.querySelectorAll('p')].some(p => p.textContent.trim() === label));
  c.sort((a, b) => a.parentElement.querySelectorAll('*').length - b.parentElement.querySelectorAll('*').length);
  return c[0] || null;
};
const bindTip = (icon, key) => {
  if (!icon) return; icon.setAttribute('data-ix', ''); icon.tabIndex = 0; icon.setAttribute('aria-label', TIPS[key][0] + ' info');
  const show = () => { const r = icon.getBoundingClientRect(), s = stage.getBoundingClientRect();
    tip.innerHTML = `<b>${TIPS[key][0]}</b><span>${TIPS[key][1]}</span>`;
    let x = (r.left - s.left) / Z - 150 + r.width / Z / 2; x = Math.max(16, Math.min(1440 - 316, x));
    tip.style.left = x + 'px'; tip.style.top = ((r.bottom - s.top) / Z + 10) + 'px'; tip.classList.add('on'); };
  const hide = () => tip.classList.remove('on');
  icon.addEventListener('mouseenter', show); icon.addEventListener('mouseleave', hide); icon.addEventListener('focus', show); icon.addEventListener('blur', hide);
};
bindTip(infoFor($('139:4789'), 'TOMATOMETER'), 'tomatometer');
bindTip(infoFor($('139:4891'), 'POPCORNMETER'), 'popcornmeter');
bindTip($('139:6085'), 'critics');
bindTip(infoFor($('139:5660'), 'Audience Reviews'), 'audience');

/* ---------------- critics tabs ---------------- */
const reviews = $('139:6106');
const views = { 'Top Critics': reviews };
const balsom = ['SIGHT & SOUND', '“La La Land remembers when movies were magical and fun, blending nostalgia and contemporaneity in a candy-sweet love letter to cinema.”', '— Erika Balsom', 'Jan 20, 2017'];
// Fresh: the rotten Andscape excerpt is replaced by a fresh top critic
const fresh = reviews.cloneNode(true); fresh.removeAttribute('data-node-id');
{ const ex = $('139:6270', fresh);
  setText(ex, 'ANDSCAPE', balsom[0]);
  const q = $$('p', ex).find(p => p.textContent.trim().startsWith('“It makes it')); if (q) q.textContent = balsom[1];
  setText(ex, '— Soraya Nadia McDonald', balsom[2]); setText(ex, 'Sep 26, 2017', balsom[3]);
  $('139:6284', ex).replaceWith($('139:6220', fresh).cloneNode(true)); }
views['Fresh'] = fresh;
// Rotten: the dissenting top critic takes the lead slot
const rotten = reviews.cloneNode(true); rotten.removeAttribute('data-node-id');
{ const lead = $('139:6109', rotten);
  setText(lead, 'OBSERVER (UK)', 'ANDSCAPE');
  const pq = $$('p', lead).find(p => p.textContent.trim().startsWith('It is simply'));
  if (pq) pq.textContent = 'It makes it more difficult to just let something like La La Land just passively wash over you when, however well-intentioned, the film hearkens back to a time when black humanity onscreen was deliberately hamstrung.';
  setText(lead, '— Mark Kermode', '— Soraya Nadia McDonald'); setText(lead, 'Jan 16, 2017', 'Sep 26, 2017');
  const rating = $('139:6127', lead); const splat = $('139:6285', rotten).cloneNode(true);
  splat.style.width = '18px'; splat.style.height = '18px'; rating.replaceWith(splat);
  const score = $('139:6134', lead); if (score) { const prevRule = score.nextElementSibling; score.remove(); }
  ['139:6144', '139:6146', '139:6204', '139:6205'].forEach(id => { const n = $(id, rotten); if (n) n.style.display = 'none'; }); }
views['Rotten'] = rotten;
Object.values(views).forEach(v => { if (v !== reviews) { v.style.display = 'none'; reviews.parentElement.appendChild(v); } });
const tabs = [...$('139:6097').children];
const ON_BG = 'rgba(255,255,255,0.92)', ON_TX = '#1b1c2a', OFF_TX = 'rgba(255,255,255,0.6)';
tabs.forEach(tab => {
  const label = tab.textContent.trim();
  ix(tab, () => {
    tabs.forEach(o => { const on = o === tab; o.style.backgroundColor = on ? ON_BG : 'transparent'; o.style.borderColor = on ? 'rgba(0,0,0,0.2)' : 'transparent'; o.style.boxShadow = on ? '0px 4px 4px 0px rgba(0,0,0,0.1)' : 'none'; o.querySelector('p').style.color = on ? ON_TX : OFF_TX; o.setAttribute('aria-selected', on); });
    Object.entries(views).forEach(([k, v]) => { v.style.display = k === label ? '' : 'none'; if (k === label) { v.classList.remove('fade'); void v.offsetWidth; v.classList.add('fade'); } });
  }, label);
  tab.setAttribute('role', 'tab');
});

/* ---------------- audience: expand "More" ---------------- */
const FULL = __AUDIENCE__;
Object.entries(FULL).forEach(([name, text]) => {
  const card = document.querySelector(`[data-name="Audience review · ${name}"]`); if (!card) return;
  const more = $$('span', card).find(s => s.textContent.trim() === 'More'); if (!more) return;
  const body = more.previousElementSibling;
  more.setAttribute('data-ix', ''); more.tabIndex = 0; more.setAttribute('role', 'button');
  const open = () => { body.textContent = text; more.remove(); };
  more.addEventListener('click', open); more.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); } });
  more.addEventListener('mouseenter', () => more.style.textDecoration = 'underline'); more.addEventListener('mouseleave', () => more.style.textDecoration = '');
});

/* ---------------- hover affordances ---------------- */
$$('[data-name^="Provider ·"]').forEach(el => { el.classList.add('btn-lift'); ix(el, () => toast(`Opening ${el.getAttribute('data-name').slice(11)}…`)); });
$$('[data-name^="Person ·"]').forEach(el => { el.classList.add('zoomable'); el.style.cursor = 'pointer'; $$('img', el).forEach(i => i.parentElement.style.overflow = 'hidden'); });
$$('[data-name^="Title ·"]').forEach(el => { el.classList.add('lift'); el.style.cursor = 'pointer'; });
const media = $('139:5907'); if (media) $$('img', media).forEach(img => { const box = img.parentElement; if (box.getBoundingClientRect().width < 200) return; box.style.overflow = 'hidden'; box.classList.add('zoomable'); box.style.cursor = 'pointer'; });
$$('p').filter(p => ['Full review', 'Read all audience reviews', 'More info', 'All 472', 'All 50,000+', 'All 66', 'All 2,122', 'All'].includes(p.textContent.trim())).forEach(p => {
  const row = p.closest('[data-name="Full review"]') || p.parentElement; row.style.cursor = 'pointer';
  row.addEventListener('mouseenter', () => { p.style.textDecoration = 'underline'; p.style.textUnderlineOffset = '3px'; });
  row.addEventListener('mouseleave', () => { p.style.textDecoration = ''; });
});
$$('[data-name="Primary nav"] p, [data-name="Sign in"] p').forEach(p => {
  const base = p.style.color;   // keep the design colour (85% white); clearing it would fall back to black
  p.style.cursor = 'pointer'; p.style.transition = 'color 140ms';
  p.addEventListener('mouseenter', () => { p.style.color = '#fff'; });
  p.addEventListener('mouseleave', () => { p.style.color = base; });
});

tick();
})();
'''


def build():
    page = convert(os.path.join(HERE, 'page.jsx'), 'p', OUT)
    # option D as refined in Figma 147:6789 (157:201): one-line composer between the last audience review and "Read all audience reviews"
    footer = '<div style="align-content:stretch;display:flex;flex-direction:column;align-items:flex-start;padding-top:22px;position:relative;flex-shrink:0;width:100%" data-node-id="139:5825"'
    assert page.count(footer) == 1, 'audience footer not found'
    page = page.replace(footer, COMPOSER.replace('{STARS}', CSTARS) + footer).replace('data-node-id="139:5825" data-name="Critic review · Andscape"', 'data-node-id="139:5825" data-name="Footer"')
    page = page.replace('src="assets/p-b467d.png"', 'src="assets/hero-poster.jpg" fetchpriority="high"')
    # ---- updates from the newest page (Figma 187:8) ----
    def outer(html, nid):
        i = html.index(f'data-node-id="{nid}"'); st = html.rindex('<div', 0, i); depth = 0
        for m in re.finditer(r'<div\b|</div>', html[st:]):
            depth += 1 if m.group(0) == '<div' else -1
            if depth == 0: return html[st:st + m.end()]
    # critics filters: new segmented style (keep the old ids the interaction layer hooks into)
    filters = jsx_to_html(open(os.path.join(HERE, 'filters187.jsx')).read(), {})
    filters = filters.replace('data-node-id="187:369"', 'data-node-id="139:6096"').replace('data-node-id="187:370"', 'data-node-id="139:6097"')
    for tab in ('187:373', '187:375'):   # same 1px border, transparent, so tabs keep their width when selected
        filters = re.sub(r'style="([^"]*)" data-node-id="%s"' % tab, lambda m: f'style="{m.group(1)};border-width:1px;border-style:solid;border-color:transparent" data-node-id="{tab}"', filters)
    page = page.replace(outer(page, '139:6096'), filters)
    # More like this gains 64px below; the footer loses its 64px top margin
    page = re.sub(r'(<div style=")([^"]*)(" data-node-id="139:5925")', lambda m: m.group(1) + m.group(2) + ';padding-bottom:64px' + m.group(3), page, count=1)
    page = re.sub(r'(<div style=")([^"]*)(" data-node-id="139:6055")', lambda m: m.group(1) + m.group(2).replace('padding-top:64px', 'padding-top:0px') + m.group(3), page, count=1)
    # the darker background layers at the end of the page
    root_open = re.search(r'<div [^>]*data-node-id="139:4722"[^>]*>', page)
    page = page[:root_open.end()] + END_LAYERS + page[root_open.end():]
    sticky = convert(os.path.join(HERE, 'sticky.jsx'), 's', OUT)
    # the sticky frame's own background spans the viewport via #sticky
    js = JS.replace('__TIPS__', json.dumps(TIPS)).replace('__AUDIENCE__', json.dumps(AUDIENCE_FULL))
    js = js.replace('tick();\n})();', drawers.JS + theater.JS + '\ntick();\n})();')
    DRAWERS = drawers.critics_drawer() + drawers.audience_drawer()
    css = CSS + drawers.CSS + theater.CSS
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>La La Land Prototype</title>
<link rel="icon" href="assets/tomato.svg" type="image/svg+xml"><link rel="preload" as="image" href="assets/hero-poster.jpg"><style>{css}</style></head>
<body>
<div id="sticky" aria-hidden="true"><div id="stickyInner">{sticky}</div></div>
<div id="stage">{page}<div id="tip" role="tooltip"></div></div>
{DRAWERS}
{theater.HTML}
<div id="toast" role="status" aria-live="polite"></div>
<script>{js}</script>
</body></html>'''
    open(os.path.join(OUT, 'index.html'), 'w').write(html)
    st = os.path.join(OUT, 'static.html')
    if os.path.exists(st): os.remove(st)
    print(os.path.join(OUT, 'index.html'), len(html) // 1024, 'KB')


if __name__ == '__main__':
    build()
