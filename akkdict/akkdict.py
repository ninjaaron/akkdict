#!/usr/bin/env python3

import os
import shutil
import click
import shlex
import configparser
from .pagefinder import lookup
from subprocess import Popen
home = os.environ['HOME']


def opendictionaries(query, dicts, command):
    for name, path in dicts.items():
        name = name.lower()
        if path[0] == '~':
            path = path.replace('~', home, 1)
        if name == 'cad':
            if not path[-1] == '/':
                path += '/'
            path, page = cadfind(path)
        else:
             page = lookup(name, query)
        Popen(shlex.split(command.format(page=page, file=path)))


def cadfind(path):
    """work a little on the pagefinder output for CAD"""
    cad_vol, page = lookup('cad', query).split()
    for file_ in os.listdir(path):
        if cad_vol + '.pdf' in file_:
            path += file_
            return (path, page)

@click.command()
@click.argument('query')
def main(query):
    '''look up Akkadian words in the CAD and other dictionaries'''
    cfg = configparser.ConfigParser()
    try:
        cfg.read(home + '/.akkdictrc')
    except FileNotFoundError:
        print('create a config by copying akkdict/conf.ini to the file',
              '~/.akkdictrc and modify it for your local setup.')
    else:
        opendictionaries(query, cfg['dicts'], cfg['conf']['command'])
