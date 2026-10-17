import pathlib,json,hashlib
from bs4 import BeautifulSoup
R=pathlib.Path(__file__).resolve().parents[1];D=R/'dist'
for f in D.glob('*.html'):
 s=BeautifulSoup(f.read_text(encoding='utf-8'),'html.parser');ids=[x['id'] for x in s.select('[id]')];assert len(ids)==len(set(ids)),f'Duplicate ID: {f}'
 for a in s.select('a[href]'):
  h=a['href']
  if h.startswith('#') and len(h)>1:assert h[1:] in ids,(f,h)
  elif not h.startswith(('http','mailto','#')):
   path,_,anchor=h.partition('#');target=D/path;assert target.exists(),(f,h)
   if anchor:assert BeautifulSoup(target.read_text(encoding='utf-8'),'html.parser').find(id=anchor),(f,h)
 assert s.title and s.select_one('meta[name=viewport]')
main=BeautifulSoup((D/'index.html').read_text(encoding='utf-8'),'html.parser')
assert len(main.select('main section'))==15
assert len(main.select('#questions details'))==12
assert len(main.select('.sermon'))==4
raw=json.loads((R/'sources/used-texts.json').read_text(encoding='utf-8'))
for slug in ['apostles-creed','nicene-creed','athanasian-creed']:
 origin=BeautifulSoup(next(x['html'] for x in raw if x['name']==slug),'html.parser').select('.alert p')
 rendered=BeautifulSoup((D/(slug+'.html')).read_text(encoding='utf-8'),'html.parser').select('.creed-text p')
 assert [p.get_text() for p in origin]==[p.get_text() for p in rendered],f'Creed text differs: {slug}'
assert all(main.select_one('#'+id).get_text(strip=True) for id in ['point1','point2','point3','point4','discussion','confessions','creeds'])
print('PASS: local links, 15 sections, 4 sermon parts, 12 discussions, 3 exact creed texts.')
