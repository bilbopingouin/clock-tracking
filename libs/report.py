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
        print('Processing reports...')

    # If we did not select an item
    if 'item' not in parameters or parameters['item'] is None:
        return


    # Get start and end dates
    if 'date' not in parameters:
        sys.stderr.write('Missing date.\n')
        sys.exit(1)
    if 'duration' not in parameters:
        sys.stderr.write('Missing date duration.\n')
        sys.exit(1)
    end_date = parameters['date']
    start_date = end_date
    if 'year' == parameters['duration']:
        start_date = datetime.datetime(year=end_date.year-1, month=end_date.month, day=end_date.day) + datetime.timedelta(days=1)
    elif 'month' == parameters['duration']:
        start_date = datetime.datetime(year=end_date.year, month=end_date.month-1, day=end_date.day) + datetime.timedelta(days=1)
    elif 'week' == parameters['duration']:
        start_date = datetime.datetime(year=end_date.year, month=end_date.month, day=end_date.day-7) + datetime.timedelta(days=1)
    elif 'start' == parameters['duration']:
        start_date = parameters['start date']
    if parameters['debug']:
        print('Reporting from {} to {}'.format(start_date.isoformat(), end_date.isoformat()))

    
    report  = parameters['db'].report(parameters['item'], start_date, end_date)
    if parameters['debug']:
        print('---\n')
    for e in report:
        print('{}: {}'.format(e[0], e[1]))
