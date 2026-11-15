#!/usr/bin/env python3
"""Builds catalog.json for the Kainuwa Studio store from the folders of this repo.

Put files in these folders (a sub folder name becomes the category shown in the app):
  fonts/<Category>/<Name>.ttf          Category: Sans Serif, Serif, Display, Handwriting, Monospace ...
  backgrounds/<Category>/<name>.png
  icons/<Category>/<name>.svg
  shapes/<Category>/<name>.svg
  images/<Category>/<name>.png
  transitions/<Category>/<name>.json

You can also upload ONE zip into the folder incoming/ that contains these folders.
The zip is unpacked, deleted, and the catalog is rebuilt.
"""
import json
import os
import re
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TYPES = {
    'fonts': ('font', {'.ttf', '.otf'}),
    'backgrounds': ('background', {'.png', '.jpg', '.jpeg', '.webp'}),
    'icons': ('icon', {'.svg', '.png'}),
    'shapes': ('shape', {'.svg'}),
    'images': ('image', {'.png', '.jpg', '.jpeg', '.webp', '.svg'}),
    'transitions': ('transition', {'.json'}),
}


def unpack_incoming():
    folder = os.path.join(ROOT, 'incoming')
    if not os.path.isdir(folder):
        return
    for name in sorted(os.listdir(folder)):
        if not name.lower().endswith('.zip'):
            continue
        path = os.path.join(folder, name)
        with zipfile.ZipFile(path) as z:
            for info in z.infolist():
                if info.is_dir():
                    continue
                parts = [p for p in info.filename.replace('\\', '/').split('/') if p not in ('', '.')]
                if '..' in parts:
                    continue
                # Allow a single wrapping folder inside the zip.
                if parts and parts[0] not in TYPES and parts[0] != 'previews' and len(parts) > 1 and parts[1] in TYPES:
                    parts = parts[1:]
                if not parts or (parts[0] not in TYPES and parts[0] != 'previews'):
                    continue
                target = os.path.join(ROOT, *parts)
                os.makedirs(os.path.dirname(target), exist_ok=True)
                with z.open(info) as src, open(target, 'wb') as dst:
                    dst.write(src.read())
        os.remove(path)
        print('Unpacked', name)


def slug(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def pretty(stem):
    s = re.sub(r'[_\-]+', ' ', stem)
    s = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s.title() if s.islower() else s


def main():
    unpack_incoming()
    old = {}
    cat_path = os.path.join(ROOT, 'catalog.json')
    if os.path.exists(cat_path):
        try:
            data = json.load(open(cat_path, encoding='utf-8'))
            for it in (data['items'] if isinstance(data, dict) else data):
                old[it.get('file', '')] = it
        except Exception:
            pass
    items = []
    for folder, (kind, exts) in TYPES.items():
        base = os.path.join(ROOT, folder)
        if not os.path.isdir(base):
            continue
        for dirpath, _, files in os.walk(base):
            for f in sorted(files):
                stem, ext = os.path.splitext(f)
                if ext.lower() not in exts:
                    continue
                full = os.path.join(dirpath, f)
                rel = os.path.relpath(full, ROOT).replace(os.sep, '/')
                sub = os.path.relpath(dirpath, base).replace(os.sep, '/')
                category = '' if sub == '.' else sub.split('/')[0]
                prev = old.get(rel, {})
                preview = ''
                for pe in ('.png', '.jpg', '.webp'):
                    cand = 'previews/' + stem + pe
                    if os.path.exists(os.path.join(ROOT, cand)):
                        preview = cand
                        break
                if not preview and kind in ('background', 'icon', 'shape', 'image'):
                    preview = rel
                item = {
                    'id': prev.get('id') or (kind + '-' + slug((category + '-' if category else '') + stem)),
                    'type': kind,
                    'name': prev.get('name') or pretty(stem),
                    'file': rel,
                    'preview': preview,
                    'sizeKb': max(1, round(os.path.getsize(full) / 1024)),
                }
                if category:
                    item['category'] = category
                for extra in ('tags', 'premium', 'description'):
                    if extra in prev:
                        item[extra] = prev[extra]
                items.append(item)
    items.sort(key=lambda i: (i['type'], i.get('category', ''), i['name'].lower()))
    seen = set()
    for it in items:
        base_id = it['id']
        n = 2
        while it['id'] in seen:
            it['id'] = base_id + '-' + str(n)
            n += 1
        seen.add(it['id'])
    with open(cat_path, 'w', encoding='utf-8') as out:
        json.dump({'version': 1, 'items': items}, out, indent=2, ensure_ascii=False)
        out.write('\n')
    print('catalog.json has', len(items), 'items')


if __name__ == '__main__':
    sys.exit(main())
