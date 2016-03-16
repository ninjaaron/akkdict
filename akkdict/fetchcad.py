#!/usr/bin/env python3

import re, sys, os
from urllib.request import urlretrieve, urlopen


def download():
    domain = 'http://oi.uchicago.edu'
    url = (domain + '/research/publications/'
           'assyrian-dictionary-oriental-institute-university-chicago-cad')
    print('Getting the list of PDFs...')
    with urlopen(url) as cad:
        pdfs = [re.sub(r'.*"(.*?\.pdf)".*', r'\1', l.decode().strip())
                for l in cad if b'.pdf' in l]
    os.mkdir('CAD')
    os.chdir('CAD')
    print('Downloading PDFs...')
    for pdf in pdfs:
        target = re.sub(r'.*/(.*)', r'\1', pdf)
        print(target)
        urlretrieve(domain + pdf, target, reporthook)


def reporthook(blocknum, blocksize, totalsize):
    readsofar = (blocknum * blocksize) / 1048576
    totalsize = totalsize / 1048576
    if totalsize > 0:
        percent = readsofar / totalsize
        s = "\r{:5.1%} {:.1f}M / {:.1f}M".format(
            percent, readsofar, totalsize)
        sys.stderr.write(s)
        if readsofar >= totalsize: # near the end
            sys.stderr.write("\n")
    else: # total size is unknown
        sys.stderr.write("read %d\n" % (readsofar,))
