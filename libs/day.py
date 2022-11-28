import os
import sys

path = os.path.dirname(__file__)
if not path:
    path = '.'
sys.path.append('{}/libs/'.format(path))

import db # noqa: E402

def get_choices(parameters):
    #mydb = db.db(parameters)

    return parameters['db'].get_dayTypes()


def process(parameters):
    # Some debugging
    if parameters['debug']:
        print('Processing days...')

    # List all the entries
    if parameters['list']:
        out = parameters['db'].get_all('day')
        if parameters['debug']:
            print('---\n')
        for e in out:
            print('{}: {}'.format(e[0], e[1]))
        return # We don't want to mix listing the entries and enter a new one

    
    if 'location' in parameters and parameters['location'] is not None:

        # New entry or entry update
        possible_choices = get_choices(parameters)
        if parameters['location'].lower() not in possible_choices:
            sys.stderr.write('Err: wrong parameter ({}), possible choices: {}\n'.format(parameters['location'], ', '.join(possible_choices)))
            sys.exit(1)

        if 'date' not in parameters:
            sys.stderr.write('Missing date.\n')
            sys.exit(1)

        #mydb = db.db(parameters)
        parameters['db'].enter('day', (parameters['date'], parameters['location']))

    else:
        if 'date' not in parameters:
            sys.stderr.write('Missing date.\n')
            sys.exit(1)

        # Delete an entry
        if parameters['delete']:
            parameters['db'].delete('day', (parameters['date']))

        # Read a given entry
        else:
            out = parameters['db'].read('day', (parameters['date']))
            if out is not None:
                if parameters['debug']:
                    print('---\n')
                print('{}: {}'.format(out[0][0], out[0][1]))
        
        


