"""Forward local Surge credentials to GitHub Actions Secrets without printing them."""
import pathlib,netrc,subprocess
repo='08-Ser-GT-Je-Personal-20261003/covenant-love-genesis17-20261017-v2-GTser'
creds=netrc.netrc(str(pathlib.Path.home()/'.netrc')).authenticators('surge.surge.sh')
if not creds:
 creds=netrc.netrc(str(pathlib.Path.home()/'.netrc')).authenticators('surge.sh')
if not creds:raise SystemExit('No local Surge login found.')
for name,value in [('SURGE_LOGIN',creds[0]),('SURGE_TOKEN',creds[2])]:
 subprocess.run(['gh','secret','set',name,'--repo',repo],input=value,text=True,check=True,capture_output=True)
print('Configured SURGE_LOGIN and SURGE_TOKEN in GitHub Actions Secrets. No credentials written to project files.')
