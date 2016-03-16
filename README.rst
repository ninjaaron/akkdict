akkdict
=======
``akkdict`` is a simple command-line python program that takes an
akkadian word as input and opens pdfs of several akkadian dictionaries
to the right page (or somewhere thereabouts). It works well for some of
the illicit pdfs of *The Concise Dictionary of Akkdian* (CDA) and *Das
Akkadishes Handwörterbuch* (AHw) floating around, if you happen to have
them. It also will get you within 100 pages in the *Assyrian Dictionary
of the Oriental Institute of the University of Chicago* (CAD), which can
be freely downloaded from
http://oi.uchicago.edu/research/publications/assyrian-dictionary-oriental-institute-university-chicago-cad
(naturally, ``akkdict`` also has a helper script for this; see below).
If you would like to contribute to expanding and improving the CAD index
or any of the other indicies, we would be happy to pull from you! If you
are a humanities major and using git is too hard, contact me!

Installation
------------
Install akkdict from PyPI with pip3! ``pip install akkdict`` If you
don't have pip and are unmotivated to get it on your platform, you can
download clone the source from github, enter the project directory and
run ``python3 setup.py install``, which will probably require root, and
you should just not do it. Just git pip.

One thing to know is you must have a way to open a PDF to a specific
page number from the command line. This is no problem on Linux. Just
look at the man page for your favorite PDF reader. I hear talk that this
is possible on OS X with AppleScript. There are also command line
options for this in Acrobat Reader. I frankly don't even know if this
package works at all on Windows, but I have my doubts. If someone who
knows something about Windows wants to contribute, please do!

*akkdict* requires some configuration. It will let you know about it.
The default config file has comments which explain things.

Usage
-----
Open a word in the configured dictionaries: ``akkdict šarru``

Print the page number (and volume): ``akkdict -p šarru``

Download the CAD into a local folder: ``akkdict --download-cad``
