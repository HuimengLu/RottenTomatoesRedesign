// Records real interactions from the running prototype (localhost:8765) with a CDP screencast.
import { chromium } from 'playwright-core';
import fs from 'fs';
import path from 'path';
import { execFileSync } from 'child_process';

const OUT = process.argv[2];
const only = process.argv[3];
const W = 1440, H = 900;

async function record(name, script) {
  if (only && only !== name) return;
  const dir = path.join(OUT, '_frames-' + name);
  fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  const b = await chromium.launch({ channel: 'chrome', headless: true, args: ['--autoplay-policy=no-user-gesture-required', '--force-device-scale-factor=1'] });
  const ctx = await b.newContext({ viewport: { width: W, height: H } });
  const p = await ctx.newPage();
  await p.goto('http://localhost:8765/', { waitUntil: 'load' });
  await p.waitForTimeout(1200);
  await p.addStyleTag({ content: '#note{display:none!important}' });
  await p.evaluate(() => {
    let y = scrollY; addEventListener('scroll', () => { if (document.documentElement.style.overflow !== 'hidden') y = scrollY; });
    new MutationObserver(() => { if (document.documentElement.style.overflow === 'hidden') scrollTo(0, y); })
      .observe(document.documentElement, { attributes: true, attributeFilter: ['style'] });
  });
  const ease = (y, ms) => p.evaluate(([y, ms]) => new Promise(res => {
    const a = scrollY, t0 = performance.now();
    const f = t => { const k = Math.min(1, (t - t0) / ms), e = k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; scrollTo(0, a + (y - a) * e); k < 1 ? requestAnimationFrame(f) : res(); };
    requestAnimationFrame(f);
  }), [y, ms]);
  const jump = y => p.evaluate(y => scrollTo(0, y), y);
  const easeIn = (sel, y, ms) => p.evaluate(([sel, y, ms]) => new Promise(res => {
    const el = document.querySelector(sel); const a = el.scrollTop, t0 = performance.now();
    const f = t => { const k = Math.min(1, (t - t0) / ms), e = k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2; el.scrollTop = a + (y - a) * e; k < 1 ? requestAnimationFrame(f) : res(); };
    requestAnimationFrame(f);
  }), [sel, y, ms]);
  const cdp = await ctx.newCDPSession(p);
  const frames = [];
  cdp.on('Page.screencastFrame', async f => {
    const file = path.join(dir, String(frames.length).padStart(5, '0') + '.jpg');
    fs.writeFileSync(file, Buffer.from(f.data, 'base64'));
    frames.push({ file, t: f.metadata.timestamp });
    try { await cdp.send('Page.screencastFrameAck', { sessionId: f.sessionId }); } catch {}
  });
  const start = () => cdp.send('Page.startScreencast', { format: 'jpeg', quality: 92, maxWidth: W, maxHeight: H, everyNthFrame: 1 });
  const stop = async () => { await cdp.send('Page.stopScreencast'); };
  await script({ p, ease, jump, easeIn, start, stop });
  await p.waitForTimeout(100);
  await b.close();
  // ffconcat with real frame durations, then a clean 30fps H.264 encode
  let list = 'ffconcat version 1.0\n';
  frames.forEach((f, i) => {
    const d = i + 1 < frames.length ? Math.max(0.001, frames[i + 1].t - f.t) : 0.5;
    list += `file '${path.basename(f.file)}'\nduration ${d.toFixed(4)}\n`;
  });
  list += `file '${path.basename(frames.at(-1).file)}'\n`;
  fs.writeFileSync(path.join(dir, 'list.txt'), list);
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', path.join(dir, 'list.txt'),
    '-vf', 'fps=30,format=yuv420p', '-c:v', 'libx264', '-preset', 'slow', '-crf', '26', '-movflags', '+faststart', '-an', path.join(OUT, name + '.mp4')]);
  console.log(name, frames.length, 'frames', fs.statSync(path.join(OUT, name + '.mp4')).size >> 10, 'KB');
  fs.rmSync(dir, { recursive: true, force: true });
}

await record('clip-sticky', async ({ p, ease, jump, start, stop }) => {
  await jump(1010);
  await p.waitForTimeout(900);
  await start();
  await p.waitForTimeout(700);
  await ease(2150, 2400);
  await p.waitForTimeout(350);
  await ease(3500, 2600);
  await p.waitForTimeout(800);
  await stop();
});

await record('clip-watch', async ({ p, jump, start, stop }) => {
  await jump(1720);
  await p.waitForTimeout(1000);
  await start();
  await p.waitForTimeout(1100);
  await p.locator('#sticky').getByRole('button', { name: 'Rent from $3.99' }).click();
  await p.waitForTimeout(3200);
  await stop();
});

await record('clip-critics', async ({ p, jump, easeIn, start, stop }) => {
  await jump(1262);
  await p.waitForTimeout(900);
  await start();
  await p.waitForTimeout(1200);
  await p.getByRole('button', { name: 'All critics reviews' }).first().click();
  await p.waitForTimeout(1500);
  const tab = t => p.locator('#drwCritics .d-tab', { hasText: t }).first().click();
  await tab('Fresh'); await p.waitForTimeout(1200);
  await tab('Rotten'); await p.waitForTimeout(1400);
  await tab('Top Critics'); await p.waitForTimeout(600);
  await easeIn('#drwCritics .drw-list', 520, 1800);
  await p.waitForTimeout(900);
  await stop();
});

await record('clip-audience', async ({ p, jump, easeIn, start, stop }) => {
  await jump(2125);
  await p.waitForTimeout(900);
  await start();
  await p.waitForTimeout(1200);
  await p.getByRole('button', { name: 'All audience reviews' }).first().click();
  await p.waitForTimeout(1700);
  await easeIn('#drwAudience .drw-list', 640, 2600);
  await p.waitForTimeout(1200);
  await stop();
});
