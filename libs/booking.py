import os
import sys

path = os.path.dirname(__file__)
if not path:
    path = '.'
sys.path.append('{}/libs/'.format(path))

import db  # noqa: E402


def process(parameters):
    if parameters['debug']:
        print('Processing bookings...')

    if parameters['list']:
        out = parameters['db'].get_all('book')
        if parameters['debug']:
            print('---\n')
        for e in out:
            print('{}: {} ({})'.format(e[0], e[2], e[1]))

    elif parameters['delete']:
        parameters['db'].delete('book', (parameters['time'],parameters['date']))

    elif parameters['start_stop'] is not None and parameters['project'] is not None:
        parameters['db'].enter('book', (parameters['time'], parameters['date'], parameters['start_stop'], parameters['project'], parameters['message'], parameters['edit']))

    else:
        sys.stderr.write('I don\'t know what to do with this information, sorry.\n')
