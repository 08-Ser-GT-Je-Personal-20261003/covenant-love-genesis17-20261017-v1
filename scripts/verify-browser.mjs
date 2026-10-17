import { chromium } from '../.deploy/tools/node_modules/playwright/index.mjs';
import fs from 'node:fs';
const browser=await chromium.launch({headless:true});fs.mkdirSync('qa',{recursive:true});let failures=[];let reports=[];
for(const width of [320,360,390,768,1024,1440,1920]){
 const page=await browser.newPage({viewport:{width,height:1000},deviceScaleFactor:1});
 page.on('pageerror',e=>failures.push(`${width}: ${e.message}`));
 await page.goto('http://127.0.0.1:4189',{waitUntil:'networkidle'});
 const result=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,sections:document.querySelectorAll('main section').length,overflows:[...document.querySelectorAll('main *')].filter(e=>{const r=e.getBoundingClientRect();return r.width&&r.right>innerWidth+1&&!e.closest('.table-wrap')}).slice(0,8).map(e=>e.tagName+'.'+e.className)}));
 if(result.scroll>width||result.overflows.length)failures.push(JSON.stringify(result));
 if(width===390||width===1440)await page.screenshot({path:`qa/home-${width}.png`,fullPage:false});
 await page.locator('#toc-toggle').click();await page.locator('#toc-toggle').click();
 await page.locator('#quiz-next').click();await page.locator('#quiz-card summary').click();
 if(!await page.locator('#quiz-card details').getAttribute('open').then(x=>x!==null))failures.push('Quiz failed');
 await page.locator('#questions summary').first().click();
 await page.locator('#theme').click();await page.locator('#theme').click();
 await page.locator('[data-map="canaan"]').click();if(await page.locator('.map svg').getAttribute('viewBox')==='0 0 960 420')failures.push('Map view failed');await page.locator('[data-map="all"]').click();
 await page.locator('[data-story="4"]').click();if(!await page.locator('#story-detail').innerText().then(t=>t.includes('启21')))failures.push('Story explorer failed');
 if(width===390){await page.locator('#point2').scrollIntoViewIfNeeded();await page.screenshot({path:'qa/sermon-390.png'});}
 await page.locator('#focus').click();if(!await page.locator('#point1').isVisible())failures.push('Focus failed');await page.locator('#focus').click();
 await page.goto('http://127.0.0.1:4189/study.html');
 if(await page.locator('#creed-links a').count()!==3)failures.push('Missing creed links');
 if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))failures.push('Study page overflow '+width);
 await page.locator('#quiz-next').click();await page.locator('#quiz-card summary').click();
 if(width===1440)await page.screenshot({path:'qa/study-1440.png'});
 for(const slug of ['apostles-creed','nicene-creed','athanasian-creed']){
  await page.goto(`http://127.0.0.1:4189/${slug}.html`);await page.locator('#mask').click();const count=await page.locator('.masked').count();await page.locator('.creed-text p').first().click();if(await page.locator('.masked').count()!==count-1)failures.push('Mask failed');await page.locator('#mask').click();
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);if(overflow)failures.push(`${slug} ${width} overflow`);
 }
 reports.push(result);await page.close();
}
const printPage=await browser.newPage();await printPage.goto('http://127.0.0.1:4189/athanasian-creed.html');await printPage.pdf({path:'qa/athanasian-reader.pdf',format:'A4',margin:{top:'15mm',bottom:'15mm',left:'15mm',right:'15mm'}});await printPage.close();
await browser.close();fs.writeFileSync('qa/browser-results.json',JSON.stringify({reports,failures},null,2));console.log(JSON.stringify({reports,failures},null,2));if(failures.length)process.exit(1);
