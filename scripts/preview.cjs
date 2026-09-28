// Requires Playwright in the local environment; not needed for daily refreshes.
const {chromium}=require('playwright');
const fs=require('node:fs');
const path=require('node:path');
const {pathToFileURL}=require('node:url');
(async()=>{
  const root=path.resolve(__dirname,'..');
  const themes=JSON.parse(fs.readFileSync(path.join(root,'themes.json'),'utf8'));
  const browser=await chromium.launch({headless:true});
  const evidence=[];
  for(const theme of themes){
    for(const mode of ['light','dark']){
      const page=await browser.newPage({viewport:{width:1100,height:1000},deviceScaleFactor:1});
      await page.goto(pathToFileURL(path.join(root,'.preview',`${theme.id}-${mode}.html`)).href);
      await page.evaluate(()=>Promise.all([...document.images].map(i=>i.decode())));
      await page.screenshot({path:path.join(root,'previews',`${theme.id}-${mode}.png`),fullPage:true});
      await page.locator('img').first().screenshot({path:path.join(root,'previews',`${theme.id}-hero-${mode}.png`)});
      await page.setViewportSize({width:390,height:844});
      const check=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,images:[...document.images].every(i=>i.complete&&i.naturalWidth>0)}));
      if(check.overflow||!check.images)throw Error(`Bad mobile layout: ${theme.id} ${mode}`);
      evidence.push({theme:theme.id,mode,mobileWidth:390,...check});
      await page.close();
    }
  }
  fs.writeFileSync(path.join(root,'previews','checks.json'),JSON.stringify(evidence,null,2)+'\n');
  await browser.close();console.log('14 desktop renders and 14 mobile image/overflow checks passed.');
})().catch(e=>{console.error(e);process.exit(1)});
