import requests,hashlib,pathlib
R=pathlib.Path(__file__).resolve().parents[1]
urls=['https://08-ser-gt-je-personal-20261003.github.io/covenant-love-genesis17-20261017-v2-GTser/','https://covenant-love-genesis17-20261017-v2-gtser.surge.sh/','https://08-ser-gt-je-personal-20261003.github.io/covenant-love-genesis17-20261017-v1/','https://covenant-love-genesis17-20261017-v1.surge.sh/']
for url in urls:
 for path in ['index.html','study.html','style.css','v2.css','app.js','apostles-creed.html','nicene-creed.html','athanasian-creed.html']:
  response=requests.get(url+path,timeout=40);response.raise_for_status()
  expected=(R/'dist'/path).read_bytes()
  # Git checkout may normalize source line endings; wording and markup must match.
  actual=response.content.replace(b'\r\n',b'\n');expected=expected.replace(b'\r\n',b'\n')
  if actual!=expected:
   i=next((i for i,(a,b) in enumerate(zip(actual,expected)) if a!=b),min(len(actual),len(expected)))
   raise AssertionError((url,path,len(actual),len(expected),i,actual[max(0,i-30):i+70],expected[max(0,i-30):i+70]))
 print('PUBLIC OK:',url,'8 files match checked local release')
