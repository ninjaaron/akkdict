import os, sys
import shlex
import click
from . import pagefinder
from subprocess import Popen
home = os.environ['HOME']


def lookup(dict, query):
    try:
        return pagefinder.lookup(dict, query)
    except ValueError as e:
        print(e, file=sys.stderr)
        exit(2)


def opendictionaries(query, dicts, command):
    for name, path in dicts.items():
        name = name.lower()
        if path[0] == '~':
            path = path.replace('~', home, 1)
        if name == 'cad':
            if not path[-1] == '/':
                path += '/'
            path, page = cadfind(query, path)
        else:
            page = lookup(name, query)
        Popen(shlex.split(command.format(page=page, file=path)))


def cadfind(query, path):
    """work a little on the pagefinder output for CAD"""
    cad_vol, page = lookup('cad', query).split()
    for file_ in os.listdir(path):
        if cad_vol + '.pdf' in file_:
            path += file_
            return (path, page)


@click.command()
@click.option('-p', is_flag=True, help='just print the dictionary reference.')
@click.option('--download-cad', is_flag=True,
              help='download the CAD from the University of Chicago website.')
@click.argument('query', required=False)
def main(query, p, download_cad):
    '''
    Look up Akkadian words in the CAD and other dictionaries. query should be
    an akkadian word. Diacritics on consonants count. Diacritics on vowels, not
    so much.
    '''
    import configparser
    import shutil
    if download_cad:
        from akkdict.fetchcad import download
        download()
        exit()
    if not query:
        print('missing argument [query].', file=sys.stderr)
        exit(1)
    if p:
        print(lookup('cad', query))
        exit()
    cfg = configparser.ConfigParser()
    if not cfg.read(home + '/.akkdictrc'):
        print("Oops! you don't have a config file yet!",
              'Creating ~/.akkdictrc...', file=sys.stderr)
        from pkg_resources import ResourceManager
        rm = ResourceManager()
        shutil.copy(rm.resource_filename('akkdict', 'conf.ini'),
                    home + '/.akkdictrc')
        print('Now, go edit ~/.akkdictrc for your local setup and then try',
              'the command again!', file=sys.stderr)
        exit(1)
    else:
        opendictionaries(query, cfg['dicts'], cfg['conf']['command'])
