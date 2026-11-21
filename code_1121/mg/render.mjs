// node render.mjs jobs.json [--still]
import pw from '/opt/npm-tools/node_modules/playwright/index.js'; const { chromium } = pw;
import fs from 'fs'; import path from 'path'; import { execFileSync } from 'child_process';
const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const still = process.argv.includes('--still');
const FPS = 30, Y0 = 860, H = 900; // render band y 860..1760
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
await page.goto('file://' + path.resolve('engine.html'));
await page.evaluate(() => document.fonts.ready);
for (const job of jobs) {
  await page.evaluate(j => window.build(j), job);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(job._first?150:150); await page.evaluate(async()=>{for(const f of document.fonts){ if(f.family.includes('Emoji')||f.family.includes('Noto')) {} } }); await page.evaluate(async t=>{await document.fonts.load('120px "Noto Color Emoji"', t)}, (job.els.filter(e=>e.kind==='emoji').map(e=>e.text).join('')||'x')); await page.waitForTimeout(300);
  await page.evaluate(j => window.build(j), job);
  if (still) {
    await page.evaluate(t => window.frame(t), job.stillAt ?? Math.min(job.dur - 0.3, 1.5));
    await page.screenshot({ path: job.out.replace(/\.mov$/, '.png'), omitBackground: true });
    console.log('still', job.out); continue;
  }
  const dir = `/tmp/claude-0/frames_${path.basename(job.out, '.mov')}`;
  fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  const n = Math.round(job.dur * FPS);
  for (let i = 0; i < n; i++) {
    await page.evaluate(t => window.frame(t), i / FPS);
    await page.screenshot({ path: `${dir}/f${String(i).padStart(4, '0')}.png`, omitBackground: true, clip: { x: 0, y: Y0, width: 1080, height: H } });
  }
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-framerate', String(FPS), '-i', `${dir}/f%04d.png`,
    '-vf', `pad=1080:1920:0:${Y0}:color=black@0,format=yuva444p10le`,
    '-c:v', 'prores_ks', '-profile:v', '4', '-pix_fmt', 'yuva444p10le', '-alpha_bits', '8', '-q:v', '12', '-vendor', 'apl0', job.out]);
  fs.rmSync(dir, { recursive: true, force: true });
  console.log('ok', job.out, n);
}
await browser.close();
