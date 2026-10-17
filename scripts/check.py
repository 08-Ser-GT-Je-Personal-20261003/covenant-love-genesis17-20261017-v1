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
assert len(main.select('main section'))==12
assert len(main.select('#questions details'))==12
assert len(main.select('.sermon'))==4
raw=json.loads((R/'sources/used-texts.json').read_text(encoding='utf-8'))
for slug in ['apostles-creed','nicene-creed','athanasian-creed']:
 origin=BeautifulSoup(next(x['html'] for x in raw if x['name']==slug),'html.parser').select('.alert p')
 rendered=BeautifulSoup((D/(slug+'.html')).read_text(encoding='utf-8'),'html.parser').select('.creed-text p')
 assert [p.get_text() for p in origin]==[p.get_text() for p in rendered],f'Creed text differs: {slug}'
assert all(main.select_one('#'+id).get_text(strip=True) for id in ['point1','point2','point3','point4','discussion','confessions'])
study=BeautifulSoup((D/'study.html').read_text(encoding='utf-8'),'html.parser')
assert study.select_one('#compare') and len(study.select('#creed-links a'))==3
# Check the catechism and all confessional excerpts too, excluding only footnote superscripts.
hc=next(x for x in raw if x['name']=='lord-day-27')
articles=BeautifulSoup(hc['html'],'html.parser').select('.entity-reference article')
orig=[]
for a in articles:
 p=a.select_one('p.no-indent')
 for marker in p.select('sup'):marker.decompose()
 orig.append((a.select_one('h4').get_text(strip=True),p.get_text()))
rendered=main.select('#confession-quotes .original')
assert [(a.h3.get_text(),a.p.get_text()) for a in rendered[:3]]==orig
for block,name in zip(rendered[3:],['34','dort-5','dort-17','dort5-14']):
 ps=BeautifulSoup(next(x['html'] for x in raw if x['name']==name),'html.parser').select('p')
 for p in ps:
  for marker in p.select('sup'):marker.decompose()
 if name=='34':ps=ps[:1]
 assert [p.get_text() for p in block.select('p')]==[p.get_text() for p in ps],name
assert len(rendered)==7
print('PASS: links, 12 focused sections, 4 sermon parts, 12 discussions, study page; all 3 creeds and 7 confessional quote blocks match primary sources.')
