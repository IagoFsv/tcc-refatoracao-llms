"""Leitor minimo de .xlsx (so o necessario para ler as planilhas do Zhang).

Evita depender de openpyxl/pandas so para conferir duas planilhas.
"""

import zipfile, re, sys, xml.etree.ElementTree as ET
NS={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
def col(ref):
    c=re.match(r'[A-Z]+',ref).group(); n=0
    for ch in c: n=n*26+ord(ch)-64
    return n-1
def read(path):
    z=zipfile.ZipFile(path); ss=[]
    if 'xl/sharedStrings.xml' in z.namelist():
        for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',NS):
            ss.append(''.join(t.text or '' for t in si.iter('{%s}t'%NS['m'])))
    wb=ET.fromstring(z.read('xl/workbook.xml'))
    names=[s.get('name') for s in wb.find('m:sheets',NS)]
    sheets={}
    for i,name in enumerate(names,1):
        root=ET.fromstring(z.read(f'xl/worksheets/sheet{i}.xml')); rows=[]
        for r in root.iter('{%s}row'%NS['m']):
            row={}
            for c in r.findall('m:c',NS):
                v=c.find('m:v',NS); t=c.get('t')
                if t=='inlineStr': val=''.join(x.text or '' for x in c.iter('{%s}t'%NS['m']))
                elif v is None: continue
                elif t=='s': val=ss[int(v.text)]
                else: val=v.text
                row[col(c.get('r'))]=val
            if row: rows.append([row.get(k,'') for k in range(max(row)+1)])
        sheets[name]=rows
    return sheets
if __name__=='__main__':
    for n,rows in read(sys.argv[1]).items():
        print('== sheet',n,len(rows),'rows')
        for r in rows[:int(sys.argv[2]) if len(sys.argv)>2 else 15]: print(r)
