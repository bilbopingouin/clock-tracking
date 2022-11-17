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
    if parameters['debug']:
        print('Yes')

    possible_choices = get_choices(parameters)

    if 'location' in parameters:
        if parameters['location'].lower() not in possible_choices:
            sys.stderr.write('Err: wrong parameter ({}), possible choices: {}\n'.format(parameters['location'], ', '.join(possible_choices)))
            sys.exit(1)

        if 'date' not in parameters:
            sys.stderr.write('Missing date.\n')
            sys.exit(1)

        #mydb = db.db(parameters)
        parameters['db'].enter('day', (parameters['date'], parameters['location']))


