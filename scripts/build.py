import pathlib,json,html,re,hashlib,shutil
from bs4 import BeautifulSoup
R=pathlib.Path(__file__).resolve().parents[1]; D=R/'dist';D.mkdir(exist_ok=True)
input_path=R/'sources/index.json'
if not input_path.exists():input_path=R/'sources/used-texts.json'
raw=json.loads(input_path.read_text(encoding='utf-8')); data=json.loads((R/'data.json').read_text(encoding='utf-8'))
def esc(s):return html.escape(s,quote=True)
def source(name):return next(x for x in reversed(raw) if x['name']==name)
def soup(x):return BeautifulSoup(x,'html.parser')
records=[]
def record(label,url,text):
 records.append({'label':label,'url':url,'sha256':hashlib.sha256(text.encode()).hexdigest(),'characters':len(text),'retrieved':'2026-10-17'})
def clean_p(p):
 # Keep original characters and punctuation; remove only footnote markers.
 for s in p.select('sup'):s.decompose()
 return p.get_text()
titles={'apostles-creed':'使徒信经','nicene-creed':'尼西亚信经','athanasian-creed':'亚他那修信经'}
descs=['简明宣认 · 信仰的骨架','同质真神 · 救主的身份','一体三位 · 基督一位二性']
head=lambda title:f'<!doctype html><html lang="zh-Hans"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#203c35"><meta name="description" content="创世记17章与海德堡要理问答主日27：主与我们建立爱的关系。完整讲章、圣约神学、信经背诵与讨论。"><title>{title} · 圣约之爱</title><link rel="icon" href="icon.svg" type="image/svg+xml"><link rel="stylesheet" href="style.css"><link rel="stylesheet" href="v2.css"></head>'
readerlinks=[]
for (slug,title),desc in zip(titles.items(),descs):
 item=source(slug);s=soup(item['html']);alert=s.select_one('.alert');assert alert,title
 paragraphs=[p.get_text() for p in alert.select('p')]; assert paragraphs
 text='\n'.join(paragraphs);record(title,item['url'],text)
 body=''.join('<p>'+esc(p)+'</p>' for p in paragraphs)
 page=head(title)+f'''<body><div class="progress" id="progress"></div><header class="topbar"><a class="brand" href="study.html#creeds"><span class="brandmark">†</span>圣约之爱 · 信经阅读</a><div class="toolbar"><button id="theme">◐ 配色</button><button data-print>打印</button></div></header><main class="reader-shell"><div class="eyebrow">CREED LIBRARY · 干净阅读版</div><h1>{title}</h1><p class="reader-note">指定中文来源：<a href="{item['url']}">ccifellowship.org 原文</a> · 核对日期 2026-10-17<br>字词、标点照录；段落换行用于阅读。古代原稿语言与本页中文译文有别。</p><div class="reader-tools"><button id="mask">逐段背诵</button><button id="read">▷ 朗读</button><button data-print>打印干净版</button><a href="study.html#compare">返回三份比较 ↗</a></div><span class="status" id="speech-status" aria-live="polite"></span><article class="creed-text">{body}</article><p class="reader-note" style="margin-top:35px">点击“逐段背诵”后，点击或用键盘回车揭示每段。打印自动显示完整正文。原文内容独立于本项目讲解。</p></main><script src="app.js"></script></body></html>'''
 (D/(slug+'.html')).write_text(page,encoding='utf-8')
 readerlinks.append(f'<article class="panel"><div class="eyebrow">{desc}</div><h3>{title}</h3><p>独立阅读 · 逐段遮盖 · 系统朗读 · 干净打印</p><a class="button" href="{slug}.html">打开阅读版 ↗</a></article>')
quotes=[]
# Heidelberg exact wording, question titles + answers, without footnote indices.
hc=source('lord-day-27'); hs=soup(hc['html']); articles=hs.select('.entity-reference article');assert len(articles)==3
hc_text=[]
for a in articles:
 h=a.select_one('h4').get_text(strip=True);p=a.select_one('p.no-indent');answer=clean_p(p);hc_text.append(h+'\n'+answer)
 quotes.append(f'<div class="original"><div class="quote-label">海德堡要理问答 · 主日27 · 指定网站原文</div><h3>{esc(h)}</h3><p>{esc(answer)}</p></div>')
record('海德堡要理问答 主日27',hc['url'],'\n'.join(hc_text))
quotes.append(f'<p class="quote-source"><a href="{hc["url"]}">核对主日27全文与经文脚注 ↗</a> · 本页省去上标脚注数字，正文不改写。</p>')
for name,label,limit in [('34','比利时信条 第34条',1),('dort-5','多特信经 第一项第5条',None),('dort-17','多特信经 第一项第17条',None),('dort5-14','多特信经 第五项第14条',None)]:
 item=source(name);ps=soup(item['html']).select('p');texts=[clean_p(p) for p in ps];texts=texts[:limit] if limit else texts;text='\n'.join(texts);record(label,item['url'],text)
 quotes.append(f'<div class="original" style="margin-top:22px"><div class="quote-label">{label} · 指定网站原文'+('节选' if limit else '')+'</div>'+''.join('<p>'+esc(p)+'</p>' for p in texts)+f'</div><p class="quote-source"><a href="{item["url"]}">核对{label}全文 ↗</a></p>')
content=(R/'content.html').read_text(encoding='utf-8')
study=(R/'study-content.html').read_text(encoding='utf-8')
study=study.replace('11 三大信经深度比较','01 三大信经深度比较').replace('12 信经干净阅读与背诵','02 信经干净阅读与背诵')
questions=''.join(f'<details><summary>{esc(q)}</summary><div class="answer"><p><b>参考答案</b> · {esc(a)}</p><p><b>答案分析</b> · {esc(analysis)}</p><p><b>讨论落点</b> · {esc(app)}</p></div></details>' for q,a,analysis,app in data['questions'])
content=content.replace('<div id="questions"></div>','<div id="questions">'+questions+'</div>').replace('<div id="confession-quotes"></div>','<div id="confession-quotes">'+''.join(quotes)+'</div>')
study=study.replace('<div class="three" id="creed-links"></div>','<div id="creed-links" class="three">'+''.join(readerlinks)+'</div>').replace('<div id="creed-links" class="three"></div>','<div id="creed-links" class="three">'+''.join(readerlinks)+'</div>')
srcs=''.join(f'<div class="source-entry"><a href="{r["url"]}">{r["label"]} ↗</a><span>指定来源 · 提取字符 {r["characters"]} · 核对 {r["retrieved"]}</span></div>' for r in records)
content=content.replace('<div id="source-list"></div>','<div id="source-list">'+srcs+'</div>')
sections=soup(content).select('section[data-title]');toc=''.join(f'<a href="#{s["id"]}">{s["data-title"]}</a>' for s in sections)
art='''<figure class="hero-art"><svg viewBox="0 0 600 620" role="img" aria-labelledby="arttitle artdesc"><title id="arttitle">约中的家：星空下的门与橄榄枝</title><desc id="artdesc">原创象征插画：拱门、星辰、橄榄枝与三条相连的道路，象征应许、家庭和通向神同住的盼望。</desc><defs><linearGradient id="arch" x2="0" y2="1"><stop stop-color="#c9d4bd"/><stop offset="1" stop-color="#e7e5d3"/></linearGradient><linearGradient id="night" x2="1" y2="1"><stop stop-color="#345344"/><stop offset="1" stop-color="#1b342e"/></linearGradient></defs><circle cx="300" cy="310" r="247" fill="none" stroke="#b8c2ac" stroke-width="1"/><circle cx="300" cy="310" r="275" fill="none" stroke="#c3cbb9" stroke-dasharray="2 9"/><path d="M135 526V235a165 165 0 0 1 330 0v291Z" fill="url(#arch)"/><path d="M170 526V244a130 130 0 0 1 260 0v282Z" fill="url(#night)"/><g fill="#dbc68b"><circle cx="237" cy="225" r="2.5"/><circle cx="337" cy="183" r="2"/><circle cx="384" cy="260" r="2.5"/><circle cx="212" cy="320" r="2"/><circle cx="309" cy="282" r="1.5"/><path d="M300 125l3 10 10 3-10 3-3 10-3-10-10-3 10-3Z"/><path d="M359 324l2 7 7 2-7 2-2 7-2-7-7-2 7-2Z"/></g><path d="M170 440Q300 350 430 440V526H170Z" fill="#687b5c"/><path d="M170 465Q310 410 430 466V526H170Z" fill="#94a07c"/><path d="M274 526Q220 458 298 416Q340 386 300 368Q354 392 320 424Q264 474 345 526Z" fill="#d6c49b"/><path d="M95 535H505M122 547H478M148 559H452" stroke="#ab9b77" stroke-width="2"/><path d="M102 490Q66 404 123 323M86 428L49 398M92 397L136 365M98 370L75 342" stroke="#70805c" fill="none" stroke-width="3"/><g fill="#82936d"><ellipse cx="57" cy="401" rx="11" ry="25" transform="rotate(-48 57 401)"/><ellipse cx="120" cy="377" rx="11" ry="25" transform="rotate(45 120 377)"/><ellipse cx="81" cy="352" rx="10" ry="23" transform="rotate(-30 81 352)"/><ellipse cx="114" cy="337" rx="10" ry="24" transform="rotate(28 114 337)"/></g><g stroke="#af8b4e" fill="none"><circle cx="480" cy="199" r="25"/><path d="M480 164V153M480 234V245M445 199H434M515 199H526"/></g><text x="300" y="593" text-anchor="middle" fill="#7c886e" font-family="serif" font-size="13" letter-spacing="7">我 要 作 你 们 的 神</text></svg><figcaption>原创象征插画 · 不作历史场景复原</figcaption></figure>'''
org='08-Ser-GT-Je-Personal-20261003';name='covenant-love-genesis17-20261017-v2-GTser';repo=f'https://github.com/{org}/{name}';pages=f'https://{org.lower()}.github.io/{name}/';surge=f'https://{name.lower()}.surge.sh'
page=head('主与我们建立爱的关系')+f'''<body><div class="progress" id="progress"></div><header class="topbar"><a href="#" class="brand"><span class="brandmark">†</span><span>圣约之爱<small>COVENANT & COMMUNION</small></span></a><div class="toolbar"><a class="nav-link" href="study.html">信经学习 ↗</a><button id="toc-toggle" aria-controls="toc" aria-expanded="true">☷ 目录</button><button id="font" class="desktop-only" aria-pressed="false">A 字号</button><button id="theme">◐ 配色</button><button id="focus" aria-pressed="false">讲章模式</button><button id="read">▷ 朗读</button><button data-print class="desktop-only">打印</button></div></header><header class="hero"><div class="hero-copy"><div class="eyebrow">CONTINENTAL REFORMED · LORD’S DAY 27</div><h1>主与我们建立<br><em>爱的关系</em></h1><p>在应许里认识归属，在宝血里看见代价，<br>在家庭中传递盼望，以信心与感恩回应。</p><div class="hero-meta"><span class="tag">创世记 17 章</span><span class="tag">海德堡要理问答 · 主日27</span><span class="tag">2026.10.17 · v2.0</span></div><a href="#point1" class="button">开始读讲章 <span aria-hidden="true">↗</span></a><a href="#overview" style="font-size:13px;margin-left:18px">先看四字提纲 ↓</a><span class="scroll-note">源 · 血 · 家 · 信 / 一条通向神同住的路</span><span class="status" id="speech-status" aria-live="polite"></span></div>{art}</header><noscript><p class="noscript">正文、原文阅读与讨论内容均可直接阅读；交互功能需要启用 JavaScript。</p></noscript><div class="page-layout"><nav class="toc" id="toc" aria-label="详细目录"><h2>阅读导航 / CONTENTS</h2><input id="toc-search" type="search" placeholder="筛选目录…" aria-label="筛选目录">{toc}<p class="search-empty" id="search-empty" hidden>未找到对应目录。</p><p style="padding:20px 12px;color:var(--muted)">先看整体，再读局部。<br>让原文约束推论，让恩典带出感恩。</p></nav><main>{content}</main></div><footer class="footer"><span>圣约之爱 · 创17 / 主日27 · 2026.10.17</span><span><a href="{repo}">源文件 ↗</a><a href="{pages}">GitHub Pages ↗</a><a href="{surge}">Surge ↗</a></span></footer><button class="backtop" id="backtop" aria-label="返回顶部">↑</button><script>window.CARDS={json.dumps(data['cards'],ensure_ascii=False)};</script><script src="app.js"></script></body></html>'''
(D/'index.html').write_text(page,encoding='utf-8')
study_toc=''.join(f'<a href="#{sec["id"]}">{sec["data-title"]}</a>' for sec in soup(study).select('section[data-title]'))
study_page=head('三大信经 · 比较与背诵')+f'''<body><div class="progress" id="progress"></div><header class="topbar"><a class="brand" href="index.html"><span class="brandmark">†</span><span>圣约之爱<small>三大信经 · 比较与背诵</small></span></a><div class="toolbar"><a class="nav-link" href="index.html#point1">返回讲章 ↗</a><button id="toc-toggle" aria-controls="toc" aria-expanded="true">☷ 目录</button><button id="theme">◐ 配色</button><button data-print>打印</button></div></header><div class="study-intro"><div class="eyebrow">ONE FAITH · THREE HISTORICAL TASKS</div><h1>认识所信的神，<br><em>记住所信的道。</em></h1><p>使徒信经立骨架，尼西亚信经明身份，亚他那修信经辨界限。<br>三份告白共同见证：向我们施恩的，是真实的三一神；为我们流血的，是真神也是真人的中保。</p><a class="button" href="#creeds">打开原文阅读与背诵 ↓</a><span class="status" id="speech-status" aria-live="polite"></span></div><div class="page-layout"><nav class="toc" id="toc" aria-label="信经学习目录"><h2>信经学习 / CREEDS</h2><input id="toc-search" type="search" placeholder="筛选目录…" aria-label="筛选目录">{study_toc}<p class="search-empty" id="search-empty" hidden>未找到对应目录。</p><a href="index.html#confessions">三项联合信条与本课 →</a></nav><main>{study}</main></div><footer class="footer"><a href="index.html">← 返回讲章</a><a href="{repo}">v2.0 · 源文件 ↗</a></footer><button class="backtop" id="backtop" aria-label="返回顶部">↑</button><script>window.CARDS={json.dumps(data['cards'],ensure_ascii=False)};</script><script src="app.js"></script></body></html>'''
(D/'study.html').write_text(study_page,encoding='utf-8')
for f in ['style.css','v2.css','app.js']:shutil.copyfile(R/f,D/f)
(D/'icon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#203c35"/><path d="M32 12V52M18 26H46" stroke="#d8b67d" stroke-width="4"/></svg>',encoding='utf-8')
(D/'.nojekyll').write_text('')
(R/'sources/verification.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
(D/'sources').mkdir(exist_ok=True);shutil.copyfile(R/'sources/verification.json',D/'sources/verification.json')
# Minimal input snapshot: exact original wording used by the build, no unrelated site material.
(R/'sources/used-texts.json').write_text(json.dumps([x for x in raw if x['name'] in set(titles)|{'lord-day-27','34','dort-5','dort-17','dort5-14'} and ('/sermons/' not in x['url'])],ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Built {len(sections)} sections, {len(data["questions"])} discussions, 3 creed readers; {len(page)} HTML characters.')
