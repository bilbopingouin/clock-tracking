import os
import sys

path = os.path.dirname(__file__)
if not path:
    path = '.'
sys.path.append('{}/libs/'.format(path))

import db  # noqa: E402


def process(parameters):
    if parameters['debug']:
        print('Processing categories...')

    if parameters['list']:
        out = parameters['db'].get_all('cat')
        if parameters['debug']:
            print('---\n')
        for e in out:
            print('{}: {}'.format(e[0], e[1]))

    elif parameters['name'] is not None and parameters['delete']:
        parameters['db'].delete('cat', (parameters['name'],))

    elif parameters['name'] is not None and parameters['description'] is not None:
        parameters['db'].enter('cat', (parameters['name'], parameters['description'], parameters['edit']))
