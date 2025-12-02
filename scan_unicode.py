# -*- coding: utf-8 -*-
"""Scan juego/*.py for non-ASCII characters and print locations and names."""
import glob, unicodedata

files = glob.glob('juego/*.py')
found = []
for path in files:
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        for i, line in enumerate(f, 1):
            for j, ch in enumerate(line):
                if ord(ch) > 127:
                    try:
                        name = unicodedata.name(ch)
                    except ValueError:
                        name = '<no name>'
                    found.append((path, i, j+1, ch, f'U+{ord(ch):04X}', name, line.strip()))

if not found:
    print('No non-ASCII characters found.')
else:
    for p, ln, col, ch, code, name, ctx in found:
        print(f"{p}: line {ln}, col {col}, char={repr(ch)}, {code}, {name}")
        print(f"   Context: {ctx}")
        print()