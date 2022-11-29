import datetime
import os
import sys

path = os.path.dirname(__file__)
if not path:
    path = '.'
sys.path.append('{}/libs/'.format(path))

import db # noqa: E402

def process(parameters):
    if parameters['debug']:
        print('Processing clocks...')

    if 'in_out' not in parameters:
        sys.stderr.write('Missing in/out\n')
        sys.exit(1)

    if parameters['in_out'] is None:
        # Global functions
        
        if 'list' in parameters and parameters['list']:
            out = parameters['db'].get_all('clock')
            if parameters['debug']:
                print('---\n')
            for e in out:
                print('{}. {} / {}: {}'.format(e[0], e[1], e[2], e[3]))
        elif 'status' in parameters and parameters['status']:
            out = parameters['db'].read('clock', (parameters['date'], parameters['time']))
            if parameters['debug']:
                print('---\n')
            status = out[0][1]
            if status is None:
                print('Clock-out')
            else:
                print(status)

    else:
        # In or Out
        if 'date' not in parameters:
            sys.stderr.write('Missing date.\n')
            sys.exit(1)
        if 'time' not in parameters:
            sys.stderr.write('Missing time.\n')
            sys.exit(1)
        parameters['db'].enter('clock', (parameters['date'], parameters['time'], parameters['in_out']))
