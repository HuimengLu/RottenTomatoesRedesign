// The Long Take: scroll drives one camera across a single world.
(() => {
  const stage = document.querySelector('.stage');
  const world = document.querySelector('.world');
  const steps = [...document.querySelectorAll('.step')].map(el => ({ el, ...JSON.parse(el.dataset.step) }));
  const blocks = [...document.querySelectorAll('.blk')].map(el => {
    const [dx, dy, s] = el.dataset.t.split(',').map(Number);
    return { el, dx, dy, s };
  });
  const tiers = [...document.querySelectorAll('[data-tier]')];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const bar = document.querySelector('.bar__p');
  const ticks = [...document.querySelectorAll('[data-tick]')];
  const chapters = steps.filter(s => s.el.dataset.ch).map(s => ({ s, tick: ticks.find(t => t.dataset.tick === s.el.dataset.ch) }));
  const TRAVEL_PAGE_H = 5226, NEW_X = 1700;

  const lerp = (a, b, t) => a + (b - a) * t;
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const smooth = t => t * t * (3 - 2 * t);

  let vw = innerWidth, vh = innerHeight, tops = [], small = false;
  const measure = () => {
    vw = innerWidth; vh = innerHeight; small = vw <= 900;
    tops = steps.map(s => { const r = s.el.getBoundingClientRect(); return { top: r.top + scrollY, h: r.height }; });
  };

  // Safe area: the part of the viewport the panel leaves free for the frame
  const safe = mode => {
    if (small) return { x: 0, y: 0, w: vw, h: vh * .44 };
    if (mode === 'side') { const x = vw * .38; return { x, y: 0, w: vw - x, h: vh }; }
    if (mode === 'wide') { const x = vw * .46; return { x, y: 0, w: vw - x, h: vh }; }
    return { x: 0, y: 0, w: vw, h: vh };
  };
  // Fit a world rect into the safe area
  const fit = (r, mode) => {
    const a = safe(mode), pad = small ? 8 : 28;
    const s = Math.min((a.w - pad * 2) / r[2], (a.h - pad * 2) / r[3]);
    return { x: a.x + a.w / 2 - (r[0] + r[2] / 2) * s, y: a.y + a.h / 2 - (r[1] + r[3] / 2) * s, s };
  };

  const mix = (a, b, t) => ({ x: lerp(a.x, b.x, t), y: lerp(a.y, b.y, t), s: Math.exp(lerp(Math.log(a.s), Math.log(b.s), t)) });

  let cur = null, active = -1, sortP = 0;

  const target = () => {
    const c = scrollY + vh / 2;
    let i = 0;
    for (let k = 0; k < tops.length; k++) if (tops[k].top <= c) i = k;
    const p = clamp((c - tops[i].top) / tops[i].h);
    const a = steps[i], b = steps[i + 1] || a;
    let ca = fit(a.cam, a.mode);
    if (a.fx === 'travel') {
      // one slow move down the whole page
      const t = clamp((p - .08) / .86);
      const pageH = TRAVEL_PAGE_H, viewH = a.cam[3];
      ca = fit([a.cam[0], (pageH - viewH) * smooth(t), a.cam[2], viewH], a.mode);
      if (p < .94) return { cam: ca, i, p };
    }
    const start = a.fx === 'sort' ? .92 : .62;   // the sort holds its frame until every module has landed
    const q = smooth(clamp((p - start) / (1 - start)));
    return { cam: q ? mix(ca, fit(b.cam, b.mode), q) : ca, i, p };
  };

  const apply = (t) => {
    if (t.i !== active) {
      active = t.i;
      const s = steps[active];
      stage.className = 'stage ' + (s.fx ? s.fx.split(' ').map(f => 'fx-' + f).join(' ') : '');
      stage.dataset.bg = s.bg;
      let ch = chapters[0];
      chapters.forEach(c => { if (steps.indexOf(c.s) <= active) ch = c; });
      ticks.forEach(a => a.classList.toggle('on', a === ch?.tick));
    }
    // The sort: modules lift off the page and settle into their tiers
    const s = steps[active];
    if (s.fx === 'sort') {
      sortP = clamp((t.p - .04) / .82);
      stage.style.setProperty('--old', 1 - clamp(sortP * 5));
      const n = blocks.length;
      blocks.forEach((b, i) => {
        const delay = (i / n) * .42;
        const k = smooth(clamp((sortP - delay) / .58));
        b.el.style.transform = `translate(${b.dx * k}px,${b.dy * k}px) scale(${lerp(1, b.s, k)})`;
      });
      tiers.forEach(el => el.classList.toggle('on', sortP > .78));
      stage.classList.toggle('moving', sortP > 0 && sortP < 1);   // layers only while flying, so landed modules re-raster sharp
    } else if (s.fx === 'sorted' || active > steps.findIndex(x => x.fx === 'sort')) {
      if (sortP !== 1) {
        sortP = 1;
        stage.style.setProperty('--old', 0);
        blocks.forEach(b => { b.el.style.transform = `translate(${b.dx}px,${b.dy}px) scale(${b.s})`; });
      }
    } else if (sortP !== 0) {
      sortP = 0;
      blocks.forEach(b => { b.el.style.transform = ''; });
      tiers.forEach(el => el.classList.remove('on'));
      stage.style.setProperty('--old', 1);
    }
  };

  const frame = () => {
    const t = target();
    if (!cur || reduce) cur = t.cam;
    else {
      const k = .14;
      cur = { x: lerp(cur.x, t.cam.x, k), y: lerp(cur.y, t.cam.y, k), s: Math.exp(lerp(Math.log(cur.s), Math.log(t.cam.s), k)) };
    }
    world.style.transform = `translate3d(${cur.x.toFixed(2)}px,${cur.y.toFixed(2)}px,0) scale(${cur.s.toFixed(5)})`;
    apply(t);
    const max = document.documentElement.scrollHeight - vh;
    bar.style.setProperty('--p', (scrollY / max).toFixed(4));
    requestAnimationFrame(frame);
  };

  addEventListener('resize', measure);
  addEventListener('load', measure);
  measure();
  document.fonts?.ready.then(measure);
  requestAnimationFrame(frame);
  // expose for checks
  window.__lt = { steps, measure };
})();
