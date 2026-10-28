#!/usr/bin/env python3
"""Select catalogue views for one pose transfer image."""
import argparse
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'shared/scripts'))
from catalog import load_index
from search import search

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--count',type=int); p.add_argument('--framing',choices=['mixed','full','upper'],default='mixed'); p.add_argument('--id',action='append',default=[],help='Exact action or view ID; repeat in panel order'); p.add_argument('--category',default=''); p.add_argument('--domain',default=''); p.add_argument('--tag',action='append',default=[]); p.add_argument('--query',default=''); p.add_argument('--phase',default=''); p.add_argument('--prop',default=''); p.add_argument('--people',type=int,default=1); p.add_argument('--adult',action='store_true')
    a=p.parse_args()
    if a.count is not None and not 1<=a.count<=9: p.error('--count must be 1–9')
    if len(a.id)>9 or len(set(a.id))!=len(a.id): p.error('provide at most 9 unique IDs')
    if a.id and a.count is not None and a.count!=len(a.id): p.error('--count must equal the number of IDs')
    poses, errors=load_index()
    if errors: p.error('\n'.join(errors))
    framing={'full':'full_body','upper':'upper_body','mixed':''}[a.framing]
    # Explicit IDs are exact selections; no hidden default framing or people filters.
    candidates=search(poses,category='' if a.id else a.category,domain='' if a.id else a.domain,tags=() if a.id else a.tag,query='' if a.id else a.query,people=None if a.id else a.people,framing='' if a.id else framing,adult=a.adult,limit=100000,phase='' if a.id else a.phase,prop='' if a.id else a.prop)
    if a.id:
        selected=[]
        for wanted in a.id:
            matches=[r for r in candidates if wanted in (r['id'],r['view_id'])]
            if not matches: p.error('ID not found or excluded by content filter: '+wanted)
            selected.append(sorted(matches,key=lambda r:r['angle']!='front')[0])
    else:
        # One view per action, preferring front. Diversify by the first tag, then cycle.
        best={}
        for row in candidates:
            old=best.get(row['id'])
            if old is None or (old['angle']!='front' and row['angle']=='front'): best[row['id']]=row
        pools={}
        for row in best.values(): pools.setdefault(row['tags'][0] if row['tags'] else row['category'],[]).append(row)
        count=a.count or 5; selected=[]
        while len(selected)<count and any(pools.values()):
            for pool in pools.values():
                if pool and len(selected)<count: selected.append(pool.pop(0))
        if len(selected)<count: p.error(f'only {len(selected)} suitable actions available; requested {count}')
    for number,row in enumerate(selected,1): row['number']=number
    print(json.dumps({'poses':selected,'count':len(selected)},ensure_ascii=False,indent=2))
if __name__=='__main__': main()
