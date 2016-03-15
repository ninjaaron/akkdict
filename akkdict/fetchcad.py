#!/usr/bin/env python3

import re, sys, os
import urllib.request as ur
domain = 'http://oi.uchicago.edu'
url = (domain + '/research/publications/'
       'assyrian-dictionary-oriental-institute-university-chicago-cad')

print('Getting the list of PDFs...')
with ur.urlopen(url) as cad:
    pdfs = [re.sub(r'.*"(.*?\.pdf)".*', r'\1', l.decode().strip())
            for l in cad if b'.pdf' in l]

os.mkdir('CAD')
os.chdir('CAD')
print('Downloading PDFs. Most of them are between 10 and 50 MB,',
      'so this may take somet time...')
for pdf in pdfs:
    target = re.sub(r'.*/(.*)', r'\1', pdf)
    print('saving', target)
    with ur.urlopen(domain + pdf) as responce, open(target, 'wb') as target:
        target.write(responce.read())
