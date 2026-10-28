#!/usr/bin/env python3
"""Build the deterministic global index after validating category data."""
import sys
from catalog import load_catalog, write_index

def main():
    poses, errors = load_catalog()
    if errors:
        print('\n'.join(errors), file=sys.stderr); return 1
    write_index(poses)
    print(f'Indexed {len(poses)} actions')
    return 0
if __name__ == '__main__': sys.exit(main())
