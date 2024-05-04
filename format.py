#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 22:19:44 2023

@author: miha
"""

import re


lines = open('authors.txt').readlines()

out = []
good = 0
for i, l in enumerate(lines):
    try:
        m = re.match(r'\d+\.\s*'
                     r'(?P<authors>(([\w\'-]+\s){1,3}(\w{1,2}\.?\s?){1,3},\s)+)'
                     r'(?P<last_author>([\w\'-]+\s){1,3}(\w{1,2}\.?\s?){1,3}\b)'
                     r'(;(?P<sci_group>).+?\.)?'
                     r'(?P<rest>.*?)'
                     r'(?P<year>(19|20)\d\d).{0,8};\s*'
                     r'(?P<issue>\d+).*'
                     r'(?P<vol>\d+)\)?:\s*'
                     r'(?P<garbage>.*?)'
                     r'(doi:\s*(?P<doi>.+))?'
                     r'$',
                     l.strip())
        authors = m.group('authors') + m.group('last_author') + (m.group('sci_group') or '')
        authors = [s.strip() for s in authors.split(',')]
        year = m.group('year')
        issue = m.group('issue')
        vol = m.group('vol') or ''
        garbage = m.group('garbage')
        m_garbage = re.match('(?P<pages>\d{1,4}(-\d{1,4})?)', garbage.strip())
        if m_garbage:
            pages = m_garbage.group('pages')
        else:
            pages = garbage
        doi = m.group('doi')
        # rest = [s.strip() for s in m.group('rest').split('.') if s.strip()]
        art_name, journal_name = m.group('rest').split('. ', 1)

        out.append(f'{authors[0]} {art_name}. / {", ".join(authors)} // '
                   f'<em>{journal_name.strip().rstrip(".")}</em>.'
                   f' – {year}. – T. {vol} – № {issue} – {pages}.')
        good += 1
    except:
        out.append('!!!!! ' + l.strip())

print(good)

with open('output.html', 'wt') as f:
    f.write('''\
<html><body>
''')
    f.write('<br>\n'.join(out))
    f.write('''\
    </body></html>
    ''')

