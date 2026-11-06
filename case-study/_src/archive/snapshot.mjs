// Freezes each version into static frames for html_to_figma. Writes <out>/<slug>.raw.html and stage captures.
import { chromium } from 'playwright-core';
import fs from 'fs';
import path from 'path';

const [,, ROOT, OUT] = process.argv;
fs.mkdirSync(OUT, { recursive: true });
const tomato = fs.readFileSync(path.join(ROOT, 'assets/svg/tomato.svg'), 'utf8');
const splat = fs.readFileSync(path.join(ROOT, 'assets/svg/splat.svg'), 'utf8');
const BASE = 'http://localhost:8770/case-study';

const b = await chromium.launch({ channel: 'chrome', headless: true });
const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } });

// Shared freeze: runs in the page
const freeze = ({ tomato, splat }) => {
  document.querySelectorAll('img[loading]').forEach(i => { i.loading = 'eager'; i.removeAttribute('decoding'); });
  document.querySelectorAll('.reveal').forEach(e => { e.classList.remove('reveal'); });
  // video → poster image
  document.querySelectorAll('video').forEach(v => {
    const i = document.createElement('img');
    i.src = v.getAttribute('poster'); i.alt = v.getAttribute('aria-label') || ''; i.className = v.className; i.style.cssText = 'width:100%;height:100%;object-fit:cover;display:block';
    v.replaceWith(i);
  });
  // masks → real vectors
  const color = el => { let n = el; while (n) { const c = getComputedStyle(n).color; if (c) return c; n = n.parentElement; } return '#fff'; };
  const paint = (svg, fill, w) => {
    const d = document.createElement('div'); d.innerHTML = svg.replace(/<mask[\s\S]*?<\/mask>/g, '').replace(/\smask="[^"]*"/g, '').replace(/fill="[^"]*"/g, `fill="${fill}"`);
    const s = d.firstElementChild; s.setAttribute('width', w); s.setAttribute('height', w);
    return s;
  };
  document.querySelectorAll('.glyph--tomato').forEach(g => {
    const fs = parseFloat(getComputedStyle(g).fontSize), s = paint(tomato, color(g), .76 * fs);
    s.style.cssText = 'display:inline-block;vertical-align:-.06em'; g.replaceWith(s);
  });
  document.querySelectorAll('.o-splat i').forEach(i => {
    const plate = getComputedStyle(i).backgroundColor, box = i.getBoundingClientRect().width || 40;
    const s = paint(splat, plate, box); s.style.display = 'block'; i.replaceWith(s);
  });
  // before/after: a real split instead of clip-path
  document.querySelectorAll('.cmp').forEach(c => {
    const x = parseFloat(c.style.getPropertyValue('--x')) || 50;
    c.querySelector('input')?.remove();
    const a = c.querySelector('.cmp__after'), i = a.querySelector('img');
    a.style.cssText = `position:absolute;top:0;bottom:0;right:0;left:${x}%;overflow:hidden;clip-path:none`;
    i.style.cssText = `position:absolute;right:0;top:0;height:100%;width:${(100 / (1 - x / 100)).toFixed(3)}%;max-width:none`;
  });
  // chart: move class styling onto the SVG itself
  document.querySelectorAll('svg.slope').forEach(s => {
    const box = s.getBoundingClientRect();
    s.setAttribute('width', Math.round(box.width)); s.setAttribute('height', Math.round(box.height));
    s.style.cssText = `width:${Math.round(box.width)}px;height:${Math.round(box.height)}px;display:block`;
    s.querySelectorAll('text').forEach(t => { t.childNodes.forEach(n => { if (n.nodeType === 3) n.textContent = n.textContent.replace(/  /g, '\u00A0\u00A0'); }); });
    s.querySelectorAll('title').forEach(t => t.remove());
    s.querySelectorAll('line[stroke=transparent]').forEach(t => t.remove());
    s.querySelectorAll('*').forEach(e => {
      const c = getComputedStyle(e);
      if (e.tagName === 'text' || e.tagName === 'tspan') {
        e.setAttribute('fill', c.fill); e.setAttribute('font-size', c.fontSize); e.setAttribute('font-weight', c.fontWeight); e.setAttribute('font-family', 'Instrument Sans');
      } else if (['line', 'circle', 'rect'].includes(e.tagName)) {
        if (c.fill !== 'none') e.setAttribute('fill', c.fill);
        if (c.stroke !== 'none') { e.setAttribute('stroke', c.stroke); e.setAttribute('stroke-width', c.strokeWidth); }
      }
      e.removeAttribute('class');
    });
  });
  document.querySelectorAll('.sl-table,script,dialog,.about,.sticky-about,.player,.bar').forEach(e => e.remove());
};

async function open(slug) {
  const p = await ctx.newPage();
  await p.goto(`${BASE}/${slug}/`, { waitUntil: 'load' });
  await p.addStyleTag({ content: 'html{scroll-behavior:auto!important}' });
  await p.evaluate(() => document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager'));
  await p.waitForLoadState('networkidle');
  await p.waitForTimeout(800);
  return p;
}
const save = (slug, frames, cls) => {
  fs.writeFileSync(path.join(OUT, `${slug}.raw.html`), `<div class="ff-root ${cls}">${frames}</div>`);
  console.log(slug, frames.length >> 10, 'KB');
};

/* ---------- A. Plates: one frame per chapter, decisions split ---------- */
{
  const p = await open('plates');
  await p.evaluate(freeze, { tomato, splat });
  const html = await p.evaluate(() => {
    document.querySelector('.top').style.position = 'static';
    const out = [];
    const main = document.querySelector('main');
    const names = ['A · 00 Opening', 'A · 01 The Disconnect', 'A · 02 The Product Reality', 'A · 03 Information Architecture', 'A · 04 Key Design Decisions', 'A · 05 The Redesigned Experience', 'A · 06 Reflection'];
    [...main.children].forEach((s, i) => {
      if (i === 4) {
        const ch = s.querySelector('.chp').parentElement.outerHTML;
        out.push(`<section class="ff" data-name="${names[4]}">${ch}</section>`);
        s.querySelectorAll('.dec').forEach((d, k) => out.push(`<section class="ff" data-name="A · 04 Decision 0${k + 1}">${d.outerHTML}</section>`));
      } else if (i === 0) {
        out.push(`<section class="ff" data-name="${names[0]}">${document.querySelector('.top').outerHTML}${s.innerHTML}</section>`);
      } else if (i === 6) {
        out.push(`<section class="ff" data-name="${names[6]}">${s.innerHTML}${document.querySelector('.foot').outerHTML}</section>`);
      } else out.push(`<section class="ff" data-name="${names[i]}">${s.innerHTML}</section>`);
    });
    return out.join('\n');
  });
  save('plates', html, 'v-plates');
  await p.close();
}

/* ---------- B. The Long Take: storyboard, one frame per camera position ---------- */
{
  const p = await open('long-take');
  const n = await p.evaluate(() => document.querySelectorAll('.step').length);
  const dir = path.join(OUT, 'stage'); fs.mkdirSync(dir, { recursive: true });
  await p.addStyleTag({ content: '.steps{opacity:0!important}.bar{display:none!important}' });
  for (let i = 0; i < n; i++) {
    if (fs.existsSync(path.join(dir, `s${String(i).padStart(2, '0')}.jpg`))) continue;
    await p.evaluate(i => { const s = document.querySelectorAll('.step')[i], r = s.getBoundingClientRect(); scrollTo(0, r.top + scrollY + r.height * (s.classList.contains('step--sort') ? .9 : .4) - innerHeight / 2); }, i);
    await p.waitForTimeout(i ? 1700 : 2400);
    await p.screenshot({ path: path.join(dir, `s${String(i).padStart(2, '0')}.jpg`), type: 'jpeg', quality: 84 });
  }
  await p.addStyleTag({ content: '.steps{opacity:1!important}' });
  await p.evaluate(freeze, { tomato, splat });
  const html = await p.evaluate(() => {
    return [...document.querySelectorAll('.step')].map((s, i) => {
      const id = String(i).padStart(2, '0');
      const title = (s.querySelector('h1,h2,h3,.lt-state,.st-b,.label,.pathrow b,.voice__n')?.textContent || 'Step').replace(/\s+/g, ' ').trim().slice(0, 40).replace(/"/g, '');
      const mode = s.className.match(/step--(side|wide|full)/)?.[1] || 'side';
      const panel = s.querySelector('.panel');
      panel.removeAttribute('style');
      return `<section class="ff ff-b ff-b--${mode}${s.classList.contains('step--sort') ? ' ff-b--sort' : ''} ${i < 16 ? 'ff-b1' : 'ff-b2'}" data-name="B · ${id} ${title}"><img class="ff-stage" src="stage/s${id}.jpg" alt=""><div class="${s.className.replace(/step--travel/, '')}">${panel.outerHTML}</div></section>`;
    }).join('\n');
  });
  save('long-take', html, 'v-longtake');
  await p.close();
}

/* ---------- C. Feature: one frame per section, pinned scenes split by subtitle ---------- */
{
  const p = await open('feature');
  await p.evaluate(freeze, { tomato, splat });
  const html = await p.evaluate(() => {
    const out = [];
    const clean = el => el.outerHTML;
    [...document.querySelector('main').children].forEach((s, i) => {
      const label = (s.querySelector('h1,h2,h3,.big,.cut__t,.take__t,.slate,cite')?.textContent || s.className).replace(/\s+/g, ' ').trim().slice(0, 40).replace(/"/g, '');
      const id = String(i).padStart(2, '0');
      if (s.matches('.scene')) {
        const subs = [...s.querySelectorAll('.subs p')];
        const pick = subs.length > 3 ? [0, 3, 6] : subs.map((_, k) => k);
        pick.forEach((k, j) => {
          const c = s.cloneNode(true);
          c.dataset.now = subs[k].dataset.fx;
          c.querySelectorAll('.subs p').forEach((e, q) => { if (q === k) { e.className = 'on'; } else e.remove(); });
          if (subs.length > 3) c.style.setProperty('--p', (k / (subs.length - 1)).toFixed(3));
          out.push(`<section class="ff ff-c-pin" data-name="C · ${id}.${j + 1} ${subs[k].textContent.trim().slice(0, 28).replace(/"/g, '')}">${c.outerHTML}</section>`);
        });
      } else if (s.matches('.open')) {
        out.push(`<section class="ff ff-c-pin" data-name="C · ${id} Title card">${clean(s)}</section>`);
      } else out.push(`<section class="ff" data-name="C · ${id} ${label}">${clean(s)}</section>`);
    });
    return out.join('\n');
  });
  save('feature', html, 'v-feature');
  await p.close();
}
await b.close();
