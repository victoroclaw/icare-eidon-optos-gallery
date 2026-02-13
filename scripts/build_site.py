import os, re, json, zipfile, shutil, hashlib
from xml.etree import ElementTree as ET

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC=os.path.join(ROOT,'source_docs')
PUB=os.path.join(ROOT,'public')
ASSETS=os.path.join(PUB,'assets')

os.makedirs(ASSETS, exist_ok=True)

ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def slug(s):
    s=s.lower().strip()
    s=re.sub(r'[^a-z0-9]+','-',s)
    return s.strip('-')

def doc_text(z):
    try:
        root=ET.fromstring(z.read('word/document.xml'))
        out=[]
        for p in root.findall('.//w:p',ns):
            t=''.join(n.text or '' for n in p.findall('.//w:t',ns)).strip()
            if t: out.append(t)
        return out
    except Exception:
        return []

cases=[]
for fn in sorted(os.listdir(SRC)):
    if not fn.lower().endswith('.docx'): continue
    path=os.path.join(SRC,fn)
    title=re.sub(r'\.docx$','',fn,flags=re.I)
    if title.strip().lower()=="add comments for each image":
        continue
    s=slug(title)
    with zipfile.ZipFile(path) as z:
        media=[n for n in z.namelist() if n.startswith('word/media/')]
        media.sort()
        text=doc_text(z)
        summary=' | '.join(text[:8])
        imgs=[]
        for i,m in enumerate(media,1):
            ext=os.path.splitext(m)[1].lower() or '.png'
            out_name=f'{s}-{i}{ext}'
            out_path=os.path.join(ASSETS,out_name)
            with z.open(m) as r, open(out_path,'wb') as w:
                shutil.copyfileobj(r,w)
            if os.path.getsize(out_path) < 10000:
                # tiny logo/footer images are not useful in demos
                os.remove(out_path)
                continue
            imgs.append('assets/'+out_name)
    cases.append({'title':title,'slug':s,'summary':summary,'images':imgs,'source_doc':'source_docs/'+fn})

with open(os.path.join(PUB,'cases.json'),'w') as f:
    json.dump({'cases':cases},f,indent=2)

print('built',len(cases),'cases')
