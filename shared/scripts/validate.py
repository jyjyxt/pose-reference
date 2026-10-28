#!/usr/bin/env python3
"""Validate all category catalogues, paths, source references and index freshness."""
import argparse
import sys
from catalog import INDEX, index_document, load_catalog, load_json

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-index', action='store_true', help='also verify the generated index is current')
    args = parser.parse_args()
    poses, errors = load_catalog()
    if args.check_index:
        try:
            if load_json(INDEX) != index_document(poses): errors.append('shared/index.json is stale; run build_index.py')
        except ValueError as exc: errors.append(str(exc))
    if errors:
        print('\n'.join(errors), file=sys.stderr); return 1
    print(f'Valid: {len(poses)} actions, {sum(1 for p in poses for _ in __import__("catalog").iter_views(p))} views')
    return 0
if __name__ == '__main__': sys.exit(main())
