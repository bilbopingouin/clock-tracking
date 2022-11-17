import argparse
import datetime
import os
import sys
import math

path = os.path.dirname(__file__)
if not path:
    path = '.'
sys.path.append('{}/libs/'.format(path))

import day # noqa: E402


def parse_arguments():
    ''' Parse the input arguments '''

    path_to_file = os.path.dirname(__file__)
    if not path_to_file:
        path_to_file = '.'
    script_dir = os.path.dirname(os.path.realpath(__file__))

    mymod=None

    parser = argparse.ArgumentParser(
        description='Time tracking', add_help=False)

    parser.add_argument(
        '-d', '--debug',
        help='Print some debug message [default: false]',
        action='store_true', required=False)
    parser.add_argument(
        '-h', '--help',
        help='Print the in-line help',
        action='store_true', required=False)

    #gr_glb = parser.add_argument_group('Global options')
    #gr_glb.add_argument(
    #    '--list',
    #    help='List the selected elements',
    #    action='store_true', required=False)
    #gr_glb.add_argument(
    #    '--edit',
    #    help='Edit the selected element',
    #    type=int, default=math.nan, required=False)
    #gr_glb.add_argument(
    #    '--delete',
    #    help='Delete the selected element',
    #    type=int, default=math.nan, required=False)
    #gr_glb.add_argument(
    #    '--time',
    #    help='Set the time for the entry (format: 03:45)',
    #    type=str,
    #    default=datetime.datetime.now().time().isoformat(timespec='minutes'),
    #    required=False)
    #gr_glb.add_argument(
    #    '--date',
    #    help='Set the date for the entry (format: ISO: YYYY-MM-DD)',
    #    type=str,
    #    default=datetime.date.today().isoformat(),
    #    required=False)

    #gr_fn = parser.add_argument_group('Functions')
    #gr_fn.add_argument(
    #    'function',
    #    help='Pick a function',
    #    nargs='?', default=None)

    gr_db = parser.add_argument_group('DB Config')
    gr_db.add_argument(
        '--sqlite-file',
        help='File when using SQLite3 [default: {}/db/db.sql]'.format(
            script_dir),
        default='{}/../db/db.sql'.format(script_dir), required=False)

    subparsers = parser.add_subparsers(help='Functions', dest='subparser_name')
    parse_day = subparsers.add_parser('day', help='Location, ..')
    parse_day.add_argument(
        'location',
        help='Work day',
        nargs='?', type=str, default=None)
    parse_day.add_argument(
        '--date',
        help='Set the date for the entry (format: ISO: YYYY-MM-DD)',
        type=str,
        default=datetime.date.today().isoformat(),
        required=False)
    parse_day.add_argument(
        '--edit',
        help='Edit the selected element',
        action='store_true', required=False)


    try:
        options = parser.parse_args()
    except:
        sys.exit(0)

    parameters = {}

    # Debug:
    parameters['debug'] = options.debug

    # Help
    parameters['help'] = options.help
    if parameters['help']:
        parser.print_help()

    if 'list' in options:
        parameters['list'] = options.list

    if 'delete' in options:
        parameters['delete'] = options.delete
    
    if 'edit' in options:
        parameters['edit'] = options.edit

    if 'time' in options:
        parameters['time'] = options.time

    if 'date' in options:
        try:
            date=datetime.date.fromisoformat(options.date)
        except ValueError:
            sys.stderr.write('Wrong date format, please use the ISO format: YYYY-MM-DD\n')
            sys.exit(1)
        parameters['date'] = date

    #parameters['function'] = mymod
    #parameters['function'] = None #options.function
    if 'subparser_name' in options:
        parameters['function'] = options.subparser_name

    if 'location' in options:
        parameters['location'] = options.location

    parameters['sqlite file'] = options.sqlite_file

    # Print all the parameters
    if parameters['debug']:
        print('\n---\nParameters:')
        for key in parameters:
            print('- {}: {}'.format(key, parameters[key]))

    # Done with the input parameters
    return parameters
