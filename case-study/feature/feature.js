// Feature Presentation: subtitles, the projector-screen travel, and the player bar.
(() => {
  const scenes = [...document.querySelectorAll('[data-scene]')].map(el => ({ el, subs: [...el.querySelectorAll('.subs p')] }));
  const fill = document.querySelector('.player__fill');
  const tl = document.querySelector('.player__tl');
  const ticks = [...document.querySelectorAll('[data-tick]')];
  const now = document.querySelector('.player__now');
  const clock = document.querySelector('.player__t b');
  const screen = document.querySelector('.screen');
  const pageImg = document.querySelector('.screen__p img');
  const RUNTIME = 360;   // seconds, an estimate of the read
  let vh = innerHeight, max = 1, marks = [];

  const measure = () => {
    vh = innerHeight;
    max = document.documentElement.scrollHeight - vh;
    marks = ticks.map(a => {
      const id = a.getAttribute('href').slice(1), s = document.getElementById(id);
      const top = s.getBoundingClientRect().top + scrollY;
      a.style.left = (top / max * 100).toFixed(2) + '%';
      return { top, name: a.title };
    });
    if (screen && pageImg) screen.style.setProperty('--travel', Math.max(0, pageImg.getBoundingClientRect().height - screen.clientHeight) + 'px');
  };

  const tick = () => {
    const y = scrollY;
    scenes.forEach(s => {
      const r = s.el.getBoundingClientRect();
      if (r.bottom < -vh || r.top > vh * 2) return;
      const p = Math.min(1, Math.max(0, -r.top / (r.height - vh)));
      s.el.style.setProperty('--p', p.toFixed(4));
      if (s.subs.length) {
        const i = Math.min(s.subs.length - 1, Math.floor(p * s.subs.length));
        s.subs.forEach((e, k) => e.classList.toggle('on', k === i && r.top <= 1 && r.bottom >= vh - 1));
        s.el.dataset.now = s.subs[i].dataset.fx;
      }
    });
    const f = y / max;
    fill.style.setProperty('--p', f.toFixed(4));
    let cur = marks[0];
    marks.forEach(m => { if (m.top <= y + vh * .4) cur = m; });
    if (cur && now.textContent !== cur.name) now.textContent = cur.name;
    const t = Math.round(f * RUNTIME);
    clock.textContent = `${Math.floor(t / 60)}:${String(t % 60).padStart(2, '0')}`;
  };

  let raf = 0;
  addEventListener('scroll', () => { if (!raf) raf = requestAnimationFrame(() => { raf = 0; tick(); }); }, { passive: true });
  addEventListener('resize', () => { measure(); tick(); });
  addEventListener('load', () => { measure(); tick(); });
  document.fonts?.ready.then(() => { measure(); tick(); });
  document.querySelectorAll('img').forEach(i => i.addEventListener('load', measure, { once: true }));
  measure(); tick();
})();
