import os
import sys
import tkinter as tk

path = os.path.dirname(__file__)
if not path:
    path = '.'
sys.path.append('{}/libs/'.format(path))

#import app  # noqa: E402
import db # noqa: E402
import interface # noqa: E402

######################


def main_function():
    # Parse the inputs
    parameters = interface.parse_arguments()

    # Create a db
    parameters['db'] = db.db(parameters)

    # Process the command
    if parameters['function'] is None:
        print('\n***\nThank you and have a nice day.')
    else:
        try:
            mymod = __import__(parameters['function'])
        except Exception as e:
            if parameters['debug']:
                print(e)
            print('No function {} known.'.format(parameters['function']))
            sys.exit(1)

        if parameters['debug']:
            print('Entering module {}'.format(parameters['function']))

        mymod.process(parameters)
        


######################
if '__main__' == __name__:
    main_function()
