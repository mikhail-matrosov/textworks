#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 15:04:20 2023

@author: miha
"""

import json
words = json.load(open('/home/miha/words_dictionary.json'))


'''
Skeletal Transform

Mawari
Mesh
points
motion
weighted sum
sparse
Base points
Key points
control points
Factorization
Decomposition
Deformation
Encoding
Compression
live
streaming
animated
3D
objects
models
'''

groups = '''
deformation
clusters
sparse
decomposition
'''.split('\n')

codes = {}
regex_parts = []
for g in groups:
    gcodes = {}
    ws = g.split()
    if len(ws) == 1:
        w = ws[0].lower()
        for i in range(4):
            gcodes[w[:i+1]] = ws[0]
    if len(ws) == 2:
        w0 = ws[0].lower()
        w1 = ws[1].lower()
        for i in range(1, 5):
            for j in range(5):
                gcodes[w0[:i] + w1[:j]] = ' '.join(ws)
    if gcodes:
        regex_parts.append('|'.join(gcodes))
        codes.update(gcodes)

print(regex_parts)
print()

import re
x = ''.join(f'({p})?' for p in regex_parts)
rex = re.compile(x)

for w in words:
    if 2 < len(w) < 12:
        m = rex.fullmatch(w)
        if m:
            decoded = [codes[g] for g in m.groups() if g]
            beatuful = [g.upper() + codes[g][len(g):].lower() for g in m.groups() if g]
            if len(decoded) == len(set(decoded)) > 2:
                print(w, ' '*(13-len(w)), ' '.join(beatuful))






