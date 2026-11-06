import json,traceback
from pathlib import Path
n=json.load(open('/downloads/assignment1-recovery/original_assignment1.ipynb'));ns={};log=[]
for i,c in enumerate(n['cells']):
 if c['cell_type']!='code' or i in [1,6]:continue
 s=''.join(c['source']).replace("'/content/movies.csv'",repr('/downloads/assignment1-work/movies_public_mirror.csv'))
 try:exec(compile(s,f'original_cell_{i}','exec'),ns)
 except Exception as e:log.append({'cell':i,'error':repr(e)});print('FAILED CELL',i,repr(e));break
Path('/downloads/assignment1-work/baseline_status.json').write_text(json.dumps({'scope':'Original source baseline excluding dependency install and profiling, public mirror data not byte-verified against Drive','failures':log},indent=2))
