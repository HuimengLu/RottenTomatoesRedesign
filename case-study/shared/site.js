// Shared behaviour for all three versions: compare sliders, lightbox, reveals, in-view video, about drawer.
(() => {
  document.documentElement.classList.add('js');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* before / after */
  document.querySelectorAll('.cmp').forEach(c => {
    const input = c.querySelector('input');
    if (!input) return;
    const set = v => c.style.setProperty('--x', v + '%');
    input.addEventListener('input', () => set(input.value));
    set(input.value);
  });

  /* scroll-driven before/after: Original first, then Redesign wipes in from the right */
  document.querySelectorAll('[data-wipe]').forEach(track => {
    const cmp = track.querySelector('.cmp'), pin = track.querySelector('.wipe__pin'), video = cmp.querySelector('video');
    const HOLD = .08;   // a beat of pure Original at the start, and of pure Redesign at the end
    let raf = 0;
    const update = () => {
      raf = 0;
      const r = track.getBoundingClientRect();
      const travel = Math.max(1, r.height - pin.offsetHeight);
      const raw = (parseFloat(getComputedStyle(pin).top) - r.top) / travel;
      const p = Math.min(1, Math.max(0, (raw - HOLD) / (1 - 2 * HOLD)));
      cmp.style.setProperty('--x', ((1 - p) * 100).toFixed(2) + '%');
      cmp.classList.toggle('is-wiping', p > 0 && p < 1);
      if (video) {
        const shown = p > 0 && r.bottom > 0 && r.top < innerHeight;
        if (shown && video.paused && !reduce) video.play().catch(() => {});
        if (!shown && !video.paused) video.pause();
        if (p === 0 && video.currentTime) video.currentTime = 0;   // so it always opens from its first frame
      }
    };
    const request = () => { if (!raf) raf = requestAnimationFrame(update); };
    addEventListener('scroll', request, { passive: true });
    addEventListener('resize', request);
    update();
  });

  /* lightbox */
  const lb = document.createElement('dialog');
  lb.className = 'lb';
  lb.setAttribute('aria-label', 'Media viewer');
  lb.innerHTML = '<div class="lb__bar"><span class="lb__t"></span><button class="lb__x" aria-label="Close">×</button></div><div class="lb__s"><img alt=""><video controls muted loop playsinline hidden></video></div>';
  document.body.appendChild(lb);
  const lbImg = lb.querySelector('img'), lbVid = lb.querySelector('video'), lbT = lb.querySelector('.lb__t'), lbS = lb.querySelector('.lb__s');
  const openLb = el => {
    const isVideo = el.dataset.kind === 'video';
    lbImg.hidden = isVideo;
    lbVid.hidden = !isVideo;
    if (isVideo) lbVid.src = el.dataset.zoom;
    else { lbImg.src = el.dataset.zoom; lbImg.alt = el.dataset.title || ''; }
    lbT.textContent = el.dataset.title || '';
    lbS.classList.toggle('is-fit', el.dataset.fit !== 'tall');
    lbS.scrollTop = 0;
    lb.showModal();
    if (isVideo && !reduce) lbVid.play().catch(() => {});
  };
  document.addEventListener('click', e => {
    const t = e.target.closest('[data-zoom]');
    if (t) { e.preventDefault(); openLb(t); }
  });
  lb.addEventListener('close', () => { lbVid.pause(); lbVid.removeAttribute('src'); lbVid.load(); });
  lb.querySelector('.lb__x').addEventListener('click', () => lb.close());
  lbImg.addEventListener('click', () => lb.close());
  lb.addEventListener('click', e => { if (e.target === lb || e.target === lbS) lb.close(); });

  /* reveals */
  const els = [...document.querySelectorAll('.reveal')];
  if (reduce || !('IntersectionObserver' in window)) els.forEach(e => e.classList.add('in'));
  else {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -7% 0px', threshold: .02 });
    els.forEach(e => io.observe(e));
  }

  /* video plays only while on screen */
  const vids = [...document.querySelectorAll('video[data-inview]')];
  if (vids.length && 'IntersectionObserver' in window) {
    const vio = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting && !reduce) e.target.play().catch(() => {}); else e.target.pause();
    }), { threshold: .25 });
    vids.forEach(v => vio.observe(v));
  }

  /* about drawer */
  const about = document.querySelector('.about');
  if (about) {
    const open = on => { about.classList.toggle('on', on); about.setAttribute('aria-hidden', on ? 'false' : 'true'); };
    document.querySelectorAll('[data-about]').forEach(b => b.addEventListener('click', () => open(!about.classList.contains('on'))));
    about.querySelector('.about__x').addEventListener('click', () => open(false));
    addEventListener('keydown', e => { if (e.key === 'Escape') open(false); });
  }

  /* the About chip follows the reader once the intro has scrolled away */
  const sa = document.querySelector('.sticky-about');
  if (sa) addEventListener('scroll', () => sa.classList.toggle('show', scrollY > innerHeight * .8), { passive: true });

  /* chapter nav state */
  const links = [...document.querySelectorAll('[data-nav] a[href^="#"]')];
  if (links.length && 'IntersectionObserver' in window) {
    const map = new Map(links.map(a => [a.getAttribute('href').slice(1), a]));
    const nio = new IntersectionObserver(es => es.forEach(e => {
      if (!e.isIntersecting) return;
      links.forEach(a => { a.classList.remove('on'); a.removeAttribute('aria-current'); });
      const cur = map.get(e.target.id);
      cur?.classList.add('on');
      cur?.setAttribute('aria-current', 'true');
    }), { rootMargin: '-45% 0px -50% 0px' });
    map.forEach((_, id) => { const s = document.getElementById(id); if (s) nio.observe(s); });
  }
})();
