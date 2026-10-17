import requests, json, pathlib
from bs4 import BeautifulSoup
root=pathlib.Path(__file__).resolve().parents[1]
out=root/'sources'; out.mkdir(exist_ok=True)
base='https://ccifellowship.org'
paths=['/books/book-of-praise/creeds/apostles-creed','/books/book-of-praise/creeds/nicene-creed','/books/book-of-praise/creeds/athanasian-creed','/books/book-of-praise/confessions/heidelberg-catechism','/books/book-of-praise/confessions/the-belgic-confession','/books/book-of-praise/confessions/canons-of-dort','/sermons/heidelberg-catechism/lord-day-27']
paths += ['/books/book-of-praise/confessions/heidelberg-catechism/section2']
paths += ['/books/book-of-praise/confessions/heidelberg-catechism/section2/part5']
paths += ['/books/book-of-praise/confessions/the-belgic-confession/'+str(n) for n in [15,22,24,33,34]]
paths += ['/books/book-of-praise/confessions/canons-of-dort/section'+str(n) for n in [1,2,3,4,5]]
data=[]
for path in paths:
 r=requests.get(base+path,timeout=40)
 if r.status_code==404: print('Not found',path); continue
 r.raise_for_status(); s=BeautifulSoup(r.text,'html.parser')
 body=s.select_one('article.article-body') or s.select_one('.field--name-body') or s.select_one('article') or s.select_one('main')
 name=path.split('/')[-1]
 if 'canons-of-dort/section' in path: name='dort-'+name
 (out/(name+'.html')).write_text(str(body),encoding='utf-8')
 links=[{'title':a.get_text(' ',strip=True),'url':requests.compat.urljoin(base,a.get('href',''))} for a in s.select('a') if '/books/' in a.get('href','')]
 data.append({'name':name,'url':base+path,'text':body.get_text('\n',strip=True),'html':str(body),'links':links})
 if path.endswith('heidelberg-catechism/section2'):
  paths.extend(dict.fromkeys(requests.compat.urlparse(a['url']).path for a in links if any('/lord-day-'+str(n)==requests.compat.urlparse(a['url']).path[-len('/lord-day-'+str(n)):] for n in [25,26,27,28])))
 if path.endswith('/part5'):
  paths.extend(dict.fromkeys(requests.compat.urlparse(a['url']).path for a in links if '/part5/' in a['url']))
 if path.endswith('canons-of-dort/section1'):
  paths.extend(dict.fromkeys(requests.compat.urlparse(a['url']).path for a in links if a['title'].startswith(('第五条','第十七条'))))
 print(name,len(data[-1]['text']))
(out/'index.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
