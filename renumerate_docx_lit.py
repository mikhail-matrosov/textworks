#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  4 17:22:18 2024

@author: miha
"""

import re
import xml.etree.ElementTree as ET
from zipfile import ZipFile
from copy import deepcopy
import io

fn = '/home/miha/Downloads/Типы остановок .docx'

in_text_link_regex = r'\[\d{1,3}\]'  # [2], [1], [123], etc


# Parse the document
zf = ZipFile(fn)
doc = zf.open('word/document.xml').read()
bf = io.BytesIO(doc)
tree = ET.parse(bf)
t = tree.getroot()


# Walk the tree, find all <w:t>
def walk(t):
    yield t
    for c in t:
        yield from walk(c)

# def walk_path(t):
#     yield (t, )
#     for c in t:
#         for e in walk_path(c):
#             yield (t, *e)

def find_tags(t, tag):
    for c in walk(t):
        if c.tag == tag or c.tag.endswith('}' + tag):
            yield c

def find_text(t, text):
    for el in walk(t):
        if el.text and text == el.text:
            yield el


links = {}  # ordered dictionary
for e in find_tags(t, 't'):
    if e.text:
        for l in re.findall(in_text_link_regex, e.text):
            links[l] = None  # store

# llist = [*find_text(t, 'Список литературы')][0]  # path in the tree t

llist_pars = []
llist_index = -1
llist_home = t[0]


# Find a list of literature pars
for i, p in enumerate(llist_home):  # iterate body: elements p
    if [*find_text(p, 'Список литературы')]:
        llist_index = i
        continue

    brbr = False
    for e in find_tags(p, 'pStyle'):
        # Search for any other headings
        if [1 for v in e.attrib.values() if 'Heading' in v]:
            brbr = True
    if brbr:
        break

    if llist_index >= 0:
        if [*find_tags(p, 'numPr')]:
            llist_pars.append(p)
        # Any other text
        elif [x for x in find_tags(p, 't') if x.text]:
            print('!!! ATTENTION !!! text ignored from the literature list:')
            for x in find_tags(p, 't'):
                if x.text:
                    print(x.text[:80])

print(f'Found {len(links)} different links')
print(f'Found {len(llist_pars)} lit entries')

# old links -> new links
old_2_new_map = {k: f'[{i+1}]' for i, k in enumerate(links)}


# Produce mapping: text_link -> par
for k in links:
    i = int(k[1:-1])  # detect integer from '[123]'
    if i <= len(llist_pars):
        links[k] = llist_pars[i-1]
    else:
        # no mapping found
        print(f'No mapping for link [{i}] - created a stub')
        el = deepcopy(llist_pars[0])
        [*find_tags(el, 't')][-1].text = 'STUB'
        links[k] = el



# Substitute links in the text
def sub(m):
    return old_2_new_map[m.group()]
for e in find_tags(t, 't'):
    if e.text:
        e.text = re.sub(in_text_link_regex, sub, e.text)


# Collect links to the list
for l in links.values():
    if l in llist_home:
        llist_home.remove(l)
for l in links.values():
    llist_home.insert(llist_index+1, l)
    llist_index += 1


# Write
bf.seek(0)
tree.write(bf)
bf.seek(0)

# with open('/home/miha/authors/out.xml', 'wb') as f:
#     tree.write(f)

with ZipFile('/home/miha/authors/out.docx', 'w') as res:
    for n in zf.namelist():
        if n == 'word/document.xml':
            res.writestr(n, bf.read())
        else:
            res.writestr(n, zf.open(n).read())










