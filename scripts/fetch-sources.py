"""Refresh primary texts used by the study. No unrelated site crawling."""
import concurrent.futures,json,pathlib,requests
from bs4 import BeautifulSoup
R=pathlib.Path(__file__).resolve().parents[1]
old=json.loads((R/'sources/used-texts.json').read_text(encoding='utf-8'))
extra={'name':'dort5-14','url':'https://ccifellowship.org/books/book-of-praise/confessions/canons-of-dort/section5/14'}
if not any(x['name']=='dort5-14' for x in old):old.append(extra)
def fetch(item):
 r=requests.get(item['url'],timeout=45);r.raise_for_status()
 s=BeautifulSoup(r.content,'html.parser')
 body=s.select_one('article.article-body') or s.select_one('.entity-reference')
 if body is None:raise RuntimeError('Missing primary text: '+item['url'])
 return {'name':item['name'],'url':item['url'],'html':str(body),'text':body.get_text('\n',strip=True)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:data=list(pool.map(fetch,old))
(R/'sources/index.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
for item in data:
 print(item['name'],len(item['text']))
 if item['name']=='dort5-14':print(item['text'])
print('Refreshed primary-source snapshots. Review wording before publishing.')
