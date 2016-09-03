import os, sys
import shlex
import click
from . import pagefinder
import subprocess
expanduser = os.path.expanduser


class Configs:
    def __init__(self, path=None):
        if path:
            self.path = expanduser(path)
        else:

            for path in map(
                  expanduser, ('~/.config/akkdict/conf.ini', '~/.akkdictrc')):
                if os.path.exists(path):
                    self.path = path
                    break
            else:
                raise FileNotFoundError('config file not found')

        self.cfg = configparser.ConfigParser()
        self.cfg.read(self.path)
        self.cfg['dicts'] = \
                {k: expanduser(v) for k, v in self.cfg['dicts'].items()}

    def __getitem__(self, key):
        return self.cfg[key]

    def __setitem__(self, key, value):
        self.cfg[key] = value

    def __delitem__(self, key):
        del self.cfg[value]

    def __getattr__(self, name):
        return getattr(self.cfg, name)

    def write(self):
        self.cfg.write(open(self.path, 'w'))


def create_config():
    os.makedirs(expanduser('~/.config/akkdict'), exists_ok=True)
    from pkg_resources import ResourceManager
    r = ResourceManager()
    shutil.copy(r.resource_filename('akkdict', 'conf.ini'),
                expanduser('~/.config/akkdict/conf.ini'))

    os.mkdirs(expanduser('~/.cache/akkdict'), exists_ok=True)
    shutil.copy(r.resource_filename('akkdict', 'indicies/cad.csv'),
                expanduser('~/.cache/akkdict/cad.csv'))


def lookup(dict, query):
    try:
        return pagefinder.lookup(dict, query)
    except ValueError as e:
        print(e, file=sys.stderr)
        exit(2)


def opendictionaries(query, dicts, command):
    for name, path in dicts.items():
        name = name.lower()
        if name == 'cad':
            if not path[-1] == '/':
                path += '/'
            path, page = cadfind(query, path)
        else:
            page = lookup(name, query)
        subprocess.Popen(shlex.split(command.format(page=page, file=path)))


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
@click.option('--updat-cad-index', is_flag=True,
              help='get the latest CAD index as updated by you and your peers')
@click.argument('query', required=False)
def main(query, p, download_cad, updat_cad_index):
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

    if updat_cad_index:
        # hit that dang webserver I still have to write
        print('updating from the remote index is not yet supported')

    if not query:
        print('missing argument [query].', file=sys.stderr)
        exit(1)

    if p:
        print(lookup('cad', query))
        exit()

    try:
        cfg = Configs()
    except FileNotFoundError:
        print("Oops! you don't have a config file yet!",
              'Creating ~/.config/akkdict...')
        create_config()
        print('Now, go edit ~/.config/akkdict/conf.ini for your local setup',
              'and then try the command again!')
        exit(1)
    else:
        opendictionaries(query, cfg['dicts'], cfg['conf']['command'])
