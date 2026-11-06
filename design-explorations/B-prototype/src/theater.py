"""Full-screen trailer (hero full-screen button): the hero's text fades, the picture leans in, then the teaser plays full screen."""

HTML = '''<div id="theater" role="dialog" aria-modal="true" aria-label="Full screen: La La Land teaser, City of Stars" hidden>
  <div class="th-backdrop" id="thBackdrop"></div>
  <div class="th-frame" id="thFrame"><div class="th-screen" id="thScreen"></div></div>
  <div class="th-ui">
    <div class="th-top"><div class="th-title"><b>La La Land</b><span>Official Teaser · City of Stars</span></div>
      <button type="button" class="th-btn" id="thExit" aria-label="Exit full screen"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 4v5H4M15 4v5h5M9 20v-5H4M15 20v-5h5"/></svg></button></div>
    <div class="th-bottom">
      <div class="th-bar" id="thBar" role="slider" aria-label="Seek" tabindex="0"><div class="th-fill" id="thFill"></div></div>
      <div class="th-row">
        <button type="button" class="th-btn" id="thPlay" aria-label="Pause"></button>
        <button type="button" class="th-btn" id="thMute" aria-label="Mute"></button>
        <span class="th-time" id="thTime">0:00 / 1:26</span>
      </div>
    </div>
  </div>
</div>'''

CSS = r'''
/* ---- hero focus: the text recedes slowly, the picture leans in ---- */
[data-node-id="139:4761"],[data-node-id="139:4787"],[data-node-id="139:4953"]{transition:opacity 650ms cubic-bezier(.4,0,.2,1), transform 650ms cubic-bezier(.4,0,.2,1)}
[data-node-id="139:4761"]{transition-delay:70ms}
[data-node-id="139:4748"],[data-node-id="139:4749"],[data-node-id="139:4750"]{transition:opacity 650ms cubic-bezier(.4,0,.2,1)}
.hero-focus [data-node-id="139:4761"],.hero-focus [data-node-id="139:4787"]{opacity:0;transform:translateY(-12px)}
.hero-focus [data-node-id="139:4953"]{opacity:0;transform:translateY(12px)}
.hero-focus [data-node-id="139:4748"],.hero-focus [data-node-id="139:4749"],.hero-focus [data-node-id="139:4750"]{opacity:0}
[data-node-id="139:4747"]{transition:transform 650ms cubic-bezier(.4,0,.2,1);transform-origin:50% 50%}
.hero-focus [data-node-id="139:4747"]{transform:scale(1.03)}
/* ---- full screen: the picture rises out of the hero frame ---- */
#theater{position:fixed;inset:0;z-index:200;overflow:hidden;font-family:Arial,Helvetica,sans-serif;color:#fff}
#theater[hidden]{display:none}
#theater.idle{cursor:none}
.th-backdrop{position:absolute;inset:0;background:#000;opacity:0}
.th-frame{position:absolute;inset:0;overflow:hidden;will-change:clip-path}
.th-screen{position:absolute;inset:0}
.th-screen video{position:absolute!important;left:0!important;top:0!important;width:100%!important;height:100%!important;max-width:none!important;object-fit:contain;
  opacity:1!important;transition:none!important;transform-origin:0 0;will-change:transform}
/* controls: show on movement, fade when idle */
.th-ui{position:absolute;inset:0;pointer-events:none;opacity:0;transition:opacity 300ms ease;
  background:linear-gradient(rgba(0,0,0,.45),rgba(0,0,0,0) 18%,rgba(0,0,0,0) 78%,rgba(0,0,0,.55))}
#theater.awake .th-ui{opacity:1}
.th-ui button,.th-ui .th-bar{pointer-events:auto}
.th-top{position:absolute;left:32px;right:32px;top:24px;display:flex;justify-content:space-between;align-items:flex-start}
.th-title{display:flex;flex-direction:column;gap:4px}
.th-title b{font:700 18px/22px Arial,Helvetica,sans-serif}
.th-title span{font:400 14px/18px Arial,Helvetica,sans-serif;color:rgba(246,241,231,.7)}
.th-bottom{position:absolute;left:32px;right:32px;bottom:24px;display:flex;flex-direction:column;gap:12px}
.th-bar{position:relative;height:14px;display:flex;align-items:center;cursor:pointer}
.th-bar::before{content:"";position:absolute;left:0;right:0;height:3px;border-radius:2px;background:rgba(246,241,231,.22)}
.th-fill{position:relative;height:3px;border-radius:2px;background:#FA320A;width:0}
.th-row{display:flex;align-items:center;gap:14px}
.th-btn{width:40px;height:40px;border-radius:20px;background:rgba(246,241,231,.1);display:flex;align-items:center;justify-content:center;cursor:pointer;transition:background 140ms}
.th-btn:hover{background:rgba(246,241,231,.22)}
.th-btn:focus-visible,.th-bar:focus-visible{outline:2px solid #fff;outline-offset:3px}
.th-time{font:700 14px/16px Arial,Helvetica,sans-serif;color:rgba(246,241,231,.85)}
@media (prefers-reduced-motion: reduce){
  [data-node-id="139:4747"],[data-node-id="139:4761"],[data-node-id="139:4787"],[data-node-id="139:4953"]{transition:none!important}
  .hero-focus [data-node-id="139:4747"],.hero-focus [data-node-id="139:4761"],.hero-focus [data-node-id="139:4787"],.hero-focus [data-node-id="139:4953"]{transform:none!important}
}
'''

JS = r'''
/* ---------------- full-screen trailer (hero full-screen button) ---------------- */
const theater = document.getElementById('theater'), thScreen = document.getElementById('thScreen');
const thPlay = document.getElementById('thPlay'), thMute = document.getElementById('thMute'), thTime = document.getElementById('thTime');
const thBar = document.getElementById('thBar'), thFill = document.getElementById('thFill');
const TH_ICON = {
  play: '<svg viewBox="0 0 24 24" width="20" height="20"><path d="M7 4.5v15l12.5-7.5z" fill="#fff"/></svg>',
  pause: '<svg viewBox="0 0 24 24" width="20" height="20" fill="#fff"><rect x="6" y="4.5" width="4" height="15" rx="1"/><rect x="14" y="4.5" width="4" height="15" rx="1"/></svg>',
  on: '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5 6 9H2v6h4l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/><path d="M19 5a10 10 0 0 1 0 14"/></svg>',
  off: '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5 6 9H2v6h4l5 4V5z"/><path d="m22 9-6 6M16 9l6 6"/></svg>',
};
let theaterOn = false, thHome = null, thIdle = 0, thClosing = false, thNative = false, thRel = null;
const thFrame = document.getElementById('thFrame'), thBackdrop = document.getElementById('thBackdrop');
const TEXT_OUT = 650, RISE = 900, EASE_RISE = 'cubic-bezier(.22,.8,.2,1)', EASE_SINK = 'cubic-bezier(.4,0,.2,1)';
const wait = ms => new Promise(r => setTimeout(r, ms));
const thSync = () => {
  thPlay.innerHTML = video.paused ? TH_ICON.play : TH_ICON.pause; thPlay.setAttribute('aria-label', video.paused ? 'Play' : 'Pause');
  thMute.innerHTML = video.muted ? TH_ICON.off : TH_ICON.on; thMute.setAttribute('aria-label', video.muted ? 'Unmute' : 'Mute');
  const d = video.duration || 86, c = video.currentTime || 0;
  thFill.style.width = (100 * c / d).toFixed(2) + '%'; thTime.textContent = `${fmt(c)} / ${fmt(d)}`;
};
['timeupdate', 'play', 'pause', 'volumechange'].forEach(ev => video.addEventListener(ev, () => { if (theaterOn) thSync(); }));
const wake = () => {
  theater.classList.add('awake'); theater.classList.remove('idle');
  clearTimeout(thIdle); thIdle = setTimeout(() => { if (!video.paused) { theater.classList.remove('awake'); theater.classList.add('idle'); } }, 2200);
};
// where the hero frame and the hero's video are on screen, expressed as a clip and a transform of the full-screen video
const fileRect = () => {   // the video file (16:9, letterbox included) as object-fit:contain draws it full screen
  const vw = innerWidth, vh = innerHeight, s = Math.min(vw / 1920, vh / 1080);
  return { l: (vw - 1920 * s) / 2, t: (vh - 1080 * s) / 2, w: 1920 * s };
};
const heroPose = () => {
  const f = hero.getBoundingClientRect(), r = 24 * Z, F = fileRect();
  const hw = thRel.w * f.width, hl = f.left + thRel.x * f.width, ht = f.top + thRel.y * f.width, sc = hw / F.w;
  return {
    clip: `inset(${f.top.toFixed(2)}px ${(innerWidth - f.right).toFixed(2)}px ${(innerHeight - f.bottom).toFixed(2)}px ${f.left.toFixed(2)}px round ${r.toFixed(2)}px)`,
    transform: `translate(${(hl - sc * F.l).toFixed(2)}px, ${(ht - sc * F.t).toFixed(2)}px) scale(${sc.toFixed(5)})`,
  };
};
const TH_FULL = { clip: 'inset(0px 0px 0px 0px round 0px)', transform: 'translate(0px, 0px) scale(1)' };
const move = (from, to, dur, easing) => Promise.all([
  thFrame.animate([{ clipPath: from.clip }, { clipPath: to.clip }], { duration: dur, easing, fill: 'forwards' }).finished,
  video.animate([{ transform: from.transform }, { transform: to.transform }], { duration: dur, easing, fill: 'forwards' }).finished,
]);
async function enterTheater() {
  if (theaterOn) return;
  theaterOn = true; thClosing = false; thNative = false;
  thHome = { parent: video.parentElement, next: video.nextSibling, muted: video.muted };
  userPaused = false; video.muted = false;        // full screen plays with sound
  video.play().catch(() => {});
  hero.classList.add('hero-focus');               // 1. the text recedes and the picture leans in
  document.documentElement.style.overflow = 'hidden';
  if (!reduce) await wait(TEXT_OUT);
  if (!theaterOn) return;
  // 2. lift the very same video element out of the frame, exactly where it is, then let it rise to fill the screen
  const f = hero.getBoundingClientRect(), v = video.getBoundingClientRect();
  thRel = { x: (v.left - f.left) / f.width, y: (v.top - f.top) / f.width, w: v.width / f.width };
  const start = heroPose();
  theater.hidden = false;
  thFrame.style.clipPath = start.clip; video.style.transform = start.transform;
  thScreen.appendChild(video);                    // same element: no reload, no jump in playback
  thSync();
  if (!reduce) {
    thBackdrop.animate([{ opacity: 0 }, { opacity: 1 }], { duration: RISE, easing: 'cubic-bezier(.3,0,.2,1)', fill: 'forwards' });
    await move(start, TH_FULL, RISE, EASE_RISE);
  } else thBackdrop.style.opacity = 1;
  thFrame.style.clipPath = TH_FULL.clip; video.style.transform = 'none';
  thFrame.getAnimations().forEach(a => a.cancel()); video.getAnimations().forEach(a => a.cancel());
  thBackdrop.style.opacity = 1; thBackdrop.getAnimations().forEach(a => a.cancel());
  if (!theaterOn || thClosing) return;
  // 3. only now hand over to the browser's full screen, so its own window animation never competes with ours
  const fs = theater.requestFullscreen ? theater.requestFullscreen({ navigationUI: 'hide' }) : null;
  if (fs && fs.then) fs.then(() => { thNative = true; }).catch(() => {});
  wake(); thPlay.focus({ preventScroll: true });
}
async function leaveTheater() {
  if (!theaterOn || thClosing) return;
  thClosing = true; clearTimeout(thIdle); theater.classList.remove('awake', 'idle');
  if (document.fullscreenElement) { await document.exitFullscreen().catch(() => {}); }
  if (thNative && !reduce) await wait(260);       // let the window settle back before measuring the hero
  thNative = false;
  if (!reduce) {
    const end = heroPose();
    thBackdrop.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 760, easing: 'ease', fill: 'forwards' });
    await move(TH_FULL, end, 760, EASE_SINK);        // the picture settles back into its frame
  }
  thHome.parent.insertBefore(video, thHome.next);
  thFrame.getAnimations().forEach(a => a.cancel()); video.getAnimations().forEach(a => a.cancel()); thBackdrop.getAnimations().forEach(a => a.cancel());
  video.style.transform = ''; thFrame.style.clipPath = ''; thBackdrop.style.opacity = '';
  theater.hidden = true; theaterOn = false; thClosing = false;
  video.muted = thHome.muted; video.style.opacity = 1;
  document.documentElement.style.overflow = '';
  hero.classList.remove('hero-focus');            // the text drifts back in
  syncPlayUi(); fsBtn.focus({ preventScroll: true });
}
document.addEventListener('fullscreenchange', () => { if (!document.fullscreenElement && theaterOn) leaveTheater(); });
document.getElementById('thExit').addEventListener('click', leaveTheater);
thPlay.addEventListener('click', () => { if (video.paused) { userPaused = false; video.play(); } else { userPaused = true; video.pause(); } wake(); });
thMute.addEventListener('click', () => { video.muted = !video.muted; wake(); });
const seekTo = x => { const r = thBar.getBoundingClientRect(); if (video.duration) video.currentTime = video.duration * Math.min(1, Math.max(0, (x - r.left) / r.width)); };
thBar.addEventListener('click', e => { seekTo(e.clientX); wake(); });
theater.addEventListener('mousemove', wake);
theater.addEventListener('keydown', e => {
  if (e.key === ' ' || e.key === 'k') { e.preventDefault(); thPlay.click(); }
  else if (e.key === 'm') thMute.click();
  else if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); video.currentTime = Math.max(0, video.currentTime + (e.key === 'ArrowRight' ? 5 : -5)); wake(); }
  else if (e.key === 'Escape' || e.key === 'f') { e.preventDefault(); leaveTheater(); }
  else if (e.key === 'Tab') {
    const f = [...theater.querySelectorAll('button, [tabindex="0"]')]; const a = f[0], z = f[f.length - 1];
    if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus(); } else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus(); }
    wake();
  }
});
'''
