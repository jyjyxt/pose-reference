#!/usr/bin/env python3
"""Search across categories; results identify both action and view."""
import argparse
import json
import sys
from catalog import CATEGORIES, image_path, iter_views, load_index

ALIASES = {'standing':'站姿', 'stand':'站姿', 'sitting':'坐姿', 'sit':'坐姿', 'squatting':'蹲姿', 'kneeling':'跪立', 'lying':'卧', 'front':'front', 'side':'side', 'high angle':'high', 'low angle':'low', 'upper body':'upper_body', 'full body':'full_body', 'couple':'双人'}

def text(value):
    return ALIASES.get(value.strip().casefold(), value.strip().casefold())

def search(poses, query='', category='', domain='', tags=(), people=None, framing='', angle='', adult=False, limit=5, distinct=False, phase='', prop=''):
    results = []
    q, angle = text(query), text(angle)
    for pose in poses:
        if pose['content_rating'] != 'general' and not (adult and pose['content_rating'] == 'adult'): continue
        if category and pose['category'] != category: continue
        if domain and domain not in pose['domains']: continue
        if people is not None and pose['people'] != people: continue
        if framing and pose['framing'] != text(framing): continue
        if any(text(t) not in ' '.join(pose['tags']).casefold() for t in tags): continue
        extensions = pose.get('extensions', {})
        props = pose.get('props', []) + extensions.get('fitness', {}).get('equipment', []) + extensions.get('yoga', {}).get('props', [])
        if prop and text(prop) not in ' '.join(props).casefold(): continue
        for phase_record, view in iter_views(pose):
            if phase and (not phase_record or text(phase) not in (phase_record['id'].casefold() + ' ' + phase_record['name'].casefold())): continue
            haystack = ' '.join([pose['id'], pose['name'], pose.get('description',''), pose['category'], *pose['domains'], *pose['tags'], *props, *extensions.get('fitness', {}).get('target_muscles', []), view['id'], view['angle'], view.get('angle_label',''), phase_record['name'] if phase_record else '']).casefold()
            if q and q not in haystack: continue
            if angle and angle not in (view['angle'].casefold(), view.get('angle_label','').casefold()): continue
            folder = CATEGORIES / pose['category']
            row = {'id': pose['id'], 'view_id': view['id'], 'name': pose['name'], 'category': pose['category'], 'domains': pose['domains'], 'tags': pose['tags'], 'kind': pose['kind'], 'people': pose['people'], 'framing': pose['framing'], 'angle': view['angle'], 'angle_label': view.get('angle_label', view['angle']), 'phase': phase_record['id'] if phase_record else None, 'phase_name': phase_record['name'] if phase_record else None, 'image_path': str(image_path(folder, view['image'])), 'source_id': view.get('source_id', pose['source_id']), 'content_rating': pose['content_rating']}
            results.append(row)
            if len(results) >= limit: return results
            if distinct: break
    return results

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--query', default=''); p.add_argument('--category', default=''); p.add_argument('--domain', default=''); p.add_argument('--tag', action='append', default=[]); p.add_argument('--people', type=int); p.add_argument('--framing', choices=['full_body','upper_body','mixed','other']); p.add_argument('--angle', default=''); p.add_argument('--phase', default=''); p.add_argument('--prop', default=''); p.add_argument('--adult', action='store_true'); p.add_argument('--distinct', action='store_true'); p.add_argument('--limit', type=int, default=5)
    args=p.parse_args()
    if not 1 <= args.limit <= 100: p.error('--limit must be 1–100')
    if args.people is not None and args.people < 1: p.error('--people must be positive')
    poses, errors=load_index()
    if errors: print('\n'.join(errors),file=sys.stderr); return 1
    rows=search(poses,args.query,args.category,args.domain,args.tag,args.people,args.framing or '',args.angle,args.adult,args.limit,args.distinct,args.phase,args.prop)
    print(json.dumps({'results':rows,'count':len(rows)},ensure_ascii=False,indent=2)); return 0
if __name__=='__main__': sys.exit(main())
