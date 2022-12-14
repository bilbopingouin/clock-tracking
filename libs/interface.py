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
        type=str, default='{}/../db/db.sql'.format(script_dir), required=False)

    subparsers = parser.add_subparsers(help='Functions', dest='subparser_name')

    # Day
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
    parse_day.add_argument(
        '--list',
        help='List all the entries',
        action='store_true', required=False)
    parse_day.add_argument(
        '--delete',
        help='Delete the selected date entry',
        action='store_true', required=False)

    # Report
    parse_report = subparsers.add_parser('report', help='Reporting')
    report_items_list = {'days'}
    parse_report.add_argument(
        'item',
        help='Elements that should be reported [{}]'.format('/'.join(e for e in report_items_list)),
        nargs=1, type=str, default=None)
    parse_report.add_argument(
        '--date',
        help='Set the date for the entry (format: ISO: YYYY-MM-DD)',
        type=str,
        default=datetime.date.today().isoformat(),
        required=False)
    parse_report_period = parse_report.add_mutually_exclusive_group()
    parse_report_period.add_argument(
        '--year',
        help='Report for one year up to the selected date',
        action='store_true', required=False)
    parse_report_period.add_argument(
        '--month',
        help='Report for one month up to the selected date',
        action='store_true', required=False)
    parse_report_period.add_argument(
        '--week',
        help='Report for one week up to the selected date',
        action='store_true', required=False)
    parse_report_period.add_argument(
        '--day',
        help='Report for one day up to the selected date',
        action='store_true', required=False)
    parse_report_period.add_argument(
        '--start-date',
        help='Set the start date for the report (format: ISO: YYYY-MM-DD)',
        type=str,
        default=datetime.date.today().isoformat(),
        required=False)
    
    # Clock
    parse_clock = subparsers.add_parser('clock', help='Clock in/out')
    parse_clock.add_argument(
        'in_out',
        help='Specify if it is a clock-in or a clock-out',
        nargs='?', type=str, default=None)
    parse_clock.add_argument(
        '--date',
        help='Set the date for the entry (format: ISO: YYYY-MM-DD)',
        type=str,
        default=datetime.date.today().isoformat(),
        required=False)
    parse_clock.add_argument(
        '--time',
        help='Set the time for the entry (format: 03:45)',
        type=str,
        default=datetime.datetime.now().time().isoformat(timespec='minutes'),
        required=False)
    parse_clock.add_argument(
        '--list',
        help='List all the entries',
        action='store_true', required=False)
    parse_clock.add_argument(
        '--status',
        help='Are we clocked in or out?',
        action='store_true', required=False)
    
    # Category
    parse_cat = subparsers.add_parser('category', help='Booking categories')
    parse_cat.add_argument(
        'cat',
        help='New category to be entered. It should contain the name of the category (single word) followed by a description. E.g. "admin General administrative tasks"',
        nargs='*', type=str, default=[])
    parse_cat.add_argument(
        '--name',
        help='Name of the category',
        type=str, default=None, required=False)
    parse_cat.add_argument(
        '--description',
        help='Description of the category',
        type=str, default=None, required=False)
    parse_cat.add_argument(
        '--list',
        help='List all the entries',
        action='store_true', required=False)
    parse_cat.add_argument(
        '--edit',
        help='Edit the selected category entry',
        action='store_true', required=False)
    parse_cat.add_argument(
        '--delete',
        help='Delete the selected category entry',
        action='store_true', required=False)
    
    # Project
    parse_prj = subparsers.add_parser('project', help='Booking project')
    parse_prj.add_argument(
        'prj',
        help='New project to be entered. It should contain the name of the project (single word) followed by the name of the category and a description. E.g. "mycustomer-101 customer The project 101 with the famous mycustomer"',
        nargs='*', type=str, default=[])
    parse_prj.add_argument(
        '--name',
        help='Name of the project',
        type=str, default=None, required=False)
    parse_prj.add_argument(
        '--description',
        help='Description of the project',
        type=str, default=None, required=False)
    parse_prj.add_argument(
        '--category',
        help='Category of the project',
        type=str, default=None, required=False)
    parse_prj.add_argument(
        '--list',
        help='List all the entries',
        action='store_true', required=False)
    parse_prj.add_argument(
        '--edit',
        help='Edit the selected project entry',
        action='store_true', required=False)
    parse_prj.add_argument(
        '--delete',
        help='Delete the selected project entry',
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

    if 'status' in options:
        parameters['status'] = options.status

    if 'name' in options:
        parameters['name'] = options.name

    if 'description' in options:
        parameters['description'] = options.description

    if 'category' in options:
        parameters['category'] = options.category

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

    if 'item' in options:
        if options.item[0] not in report_items_list:
            sys.stderr.write('Report item ({}) not known\n'.format(options.item[0]))
            sys.exit(1)
        parameters['item'] = options.item[0]

    if 'function' in parameters and 'report' == parameters['function']:
        if options.year:
            parameters['duration'] = 'year'
        elif options.month:
            parameters['duration'] = 'month'
        elif options.week:
            parameters['duration'] = 'week'
        elif options.day:
            parameters['duration'] = 'day'
        else:
            # By default we choose a monthly review
            parameters['duration'] = 'start'
            try:
                parameters['start date'] = datetime.date.fromisoformat(options.start_date)
            except ValueError:
                sys.stderr.write('Wrong date format, please use the ISO format: YYYY-MM-DD\n')
                sys.exit(1)

    if 'in_out' in options:
        parameters['in_out'] = options.in_out
        if parameters['in_out'] is not None:
            parameters['in_out'] = parameters['in_out'].lower()
            if parameters['in_out'] not in {'in', 'out'}:
                sys.stderr.write('Unknown option ({}), please select \'in\' or \'out\''.format(parameters['in_out']))
                sys.exit(1)

    parameters['sqlite file'] = options.sqlite_file

    """
    We need two parameters for the categories:
    - name (single word)
    - description (one or more words)
    Those can be either defined individually using the key arguments --name / --description or using the positional argument. Or even using a combination of both.

    If no key argument is used. The first word of the positional argument is the name, the rest is taken as description.
    If both keys are used, we ignore the positional argument.
    If the name key is used, we assume the positional argument is the description
    """
    if 'cat' in options:
        cat_str = options.cat
        if cat_str:
            # We have some positional argument

            index=0
            if parameters['name'] is None:
                parameters['name'] = cat_str[index]
                index += 1

            if parameters['description'] is None and len(cat_str)>index:
                parameters['description'] = ' '.join(cat_str[index:])

    """
    We need three parameters for the projects:
    - name (single word)
    - category (single word)
    - description (one or more words)
    Those can be either defined individually using the key arguments --name / --description or using the positional argument. Or even using a combination of both.

    We consider if the key is used or not.
    | case | name | category | description | Interpret the positional arguments |
    | ---- | ---- | -------- | ----------- | --- |
    |    1 | no   | no       | no          | name=A[0], cat=A[1], desc=A[2:] |
    |    2 | yes  | no       | no          | cat=A[0], desc=A[1:] |
    |    3 | yes  | yes      | no          | desc=A[0:] |
    |    4 | no   | yes      | no          | name=A[0], desc=A[1:] |
    |    5 | no   | yes      | yes         | name=A[0] |
    |    6 | yes  | yes      | yes         | - |
    |    7 | yes  | no       | yes         | cat=A[0] |
    |    8 | no   | no       | yes         | name=A[0], cat=A[1] |
    """
    if 'prj' in options:
        prj_str = options.prj
        if prj_str:
            # We have some positional argument

            index=0
            if parameters['name'] is None:
                parameters['name'] = prj_str[index]
                index += 1

            if parameters['category'] is None and len(prj_str)>index:
                parameters['category'] = prj_str[index]
                index += 1

            if parameters['description'] is None and len(prj_str)>index:
                parameters['description'] = ' '.join(prj_str[index:])


    # Print all the parameters
    if parameters['debug']:
        print('\n---\nParameters:')
        for key in parameters:
            print('- {}: {}'.format(key, parameters[key]))

    # Done with the input parameters
    return parameters
