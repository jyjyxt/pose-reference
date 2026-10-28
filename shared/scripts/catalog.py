#!/usr/bin/env python3
"""Catalogue loading and validation shared by all pose skills."""
import json
import os
import re
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / 'shared/schema/pose.schema.json'
CATEGORIES = ROOT / 'categories'
INDEX = ROOT / 'shared/index.json'


def load_json(path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        raise ValueError(f'{path}: {exc}') from exc


def _validate(value, spec, schema, where, errors):
    if '$ref' in spec:
        ref = spec['$ref']
        if not ref.startswith('#/$defs/'):
            errors.append(f'{where}: unsupported schema reference {ref}')
            return
        return _validate(value, schema['$defs'][ref.split('/')[-1]], schema, where, errors)
    if 'allOf' in spec:
        for part in spec['allOf']: _validate(value, part, schema, where, errors)
    if 'if' in spec:
        conditional_errors = []
        _validate(value, spec['if'], schema, where, conditional_errors)
        branch = spec.get('then' if not conditional_errors else 'else')
        if branch: _validate(value, branch, schema, where, errors)
    if 'not' in spec:
        negated_errors = []
        _validate(value, spec['not'], schema, where, negated_errors)
        if not negated_errors: errors.append(f'{where}: forbidden combination')
    if 'const' in spec and value != spec['const']: errors.append(f'{where}: expected {spec["const"]!r}')
    typ = spec.get('type')
    types = {'object': dict, 'array': list, 'string': str, 'number': (int, float), 'integer': int}
    if typ and (not isinstance(value, types[typ]) or typ in ('integer', 'number') and isinstance(value, bool)):
        errors.append(f'{where}: expected {typ}')
        return
    if 'enum' in spec and value not in spec['enum']:
        errors.append(f'{where}: invalid value {value!r}')
    if isinstance(value, str):
        if len(value) < spec.get('minLength', 0): errors.append(f'{where}: string is too short')
        if 'pattern' in spec and not re.search(spec['pattern'], value): errors.append(f'{where}: invalid format')
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if 'minimum' in spec and value < spec['minimum']: errors.append(f'{where}: below minimum')
        if 'maximum' in spec and value > spec['maximum']: errors.append(f'{where}: above maximum')
    if isinstance(value, list):
        if len(value) < spec.get('minItems', 0): errors.append(f'{where}: too few items')
        if spec.get('uniqueItems') and len({json.dumps(v, sort_keys=True, ensure_ascii=False) for v in value}) != len(value): errors.append(f'{where}: duplicate items')
        if 'items' in spec:
            for i, item in enumerate(value): _validate(item, spec['items'], schema, f'{where}[{i}]', errors)
    if isinstance(value, dict):
        for key in spec.get('required', []):
            if key not in value: errors.append(f'{where}: missing {key}')
        properties = spec.get('properties', {})
        if spec.get('additionalProperties') is False:
            for key in value.keys() - properties.keys(): errors.append(f'{where}: unexpected field {key}')
        for key, child in value.items():
            if key in properties: _validate(child, properties[key], schema, f'{where}.{key}', errors)


def image_path(category_dir, relative):
    path = (category_dir / relative).resolve()
    if not path.is_relative_to(category_dir.resolve()):
        raise ValueError(f'image path escapes category: {relative}')
    return path


def iter_views(pose):
    if pose['kind'] == 'pose':
        for view in pose.get('views', []): yield None, view
    else:
        for phase in pose.get('phases', []):
            for view in phase.get('views', []): yield phase, view


def load_catalog():
    schema = load_json(SCHEMA)
    errors, records, ids, view_ids = [], [], set(), set()
    for folder in sorted(CATEGORIES.iterdir()):
        if not folder.is_dir() or folder.name.startswith('.'): continue
        if not (folder / 'poses.json').is_file():
            errors.append(f'{folder}: missing poses.json'); continue
        try:
            data, sources = load_json(folder / 'poses.json'), load_json(folder / 'sources.json')
        except ValueError as exc:
            errors.append(str(exc)); continue
        before = len(errors)
        _validate(data, schema, schema, str(folder / 'poses.json'), errors)
        if not isinstance(sources, dict) or not all(isinstance(k, str) and k and isinstance(v, dict) and isinstance(v.get('description'), str) and v['description'] and isinstance(v.get('url'), str) and v['url'] for k, v in sources.items()):
            errors.append(f'{folder}/sources.json: expected source ID map with description and url'); continue
        if len(errors) != before: continue
        for pose in data:
            label = pose['id']
            if label in ids: errors.append(f'{label}: duplicate action ID')
            ids.add(label)
            if pose['category'] != folder.name or not label.startswith(folder.name + ':'): errors.append(f'{label}: category and ID must match folder {folder.name}')
            if pose['source_id'] not in sources: errors.append(f'{label}: unknown source {pose["source_id"]}')
            kind = pose['kind']
            if kind == 'pose' and ('views' not in pose or 'phases' in pose): errors.append(f'{label}: pose requires views and forbids phases')
            if kind == 'movement' and ('phases' not in pose or 'views' in pose): errors.append(f'{label}: movement requires phases and forbids views')
            phases = pose.get('phases', [])
            if len({p['id'] for p in phases}) != len(phases): errors.append(f'{label}: duplicate phase ID')
            for phase, view in iter_views(pose):
                vid = view['id']
                if vid in view_ids: errors.append(f'{label}: duplicate view ID {vid}')
                view_ids.add(vid)
                if view.get('source_id', pose['source_id']) not in sources: errors.append(f'{label}/{vid}: unknown source')
                for field in ('image',):
                    if field in view:
                        try:
                            path = image_path(folder, view[field])
                            if not path.is_file(): errors.append(f'{label}/{vid}: missing {field}: {path}')
                        except ValueError as exc: errors.append(f'{label}/{vid}: {exc}')
            records.append(pose)
    return records, errors


def index_document(records):
    return {'version': 1, 'poses': records}


def write_index(records):
    content = json.dumps(index_document(records), ensure_ascii=False, indent=2) + '\n'
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=INDEX.parent, delete=False) as f:
        temp = Path(f.name)
        try:
            f.write(content)
        except BaseException:
            temp.unlink(missing_ok=True)
            raise
    try:
        os.replace(temp, INDEX)
    finally:
        temp.unlink(missing_ok=True)


def load_index():
    records, errors = load_catalog()
    if errors: return [], errors
    try:
        index = load_json(INDEX)
    except ValueError as exc:
        return [], [str(exc)]
    if index != index_document(records):
        return [], ['shared/index.json is stale; run python3 shared/scripts/build_index.py']
    return index['poses'], []
