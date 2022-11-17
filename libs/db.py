import os
import sqlite3
import sys


class db:
    def __init__(self, parameters):
        self.debug = parameters['debug']

        if 'sqlite file' not in parameters:
            parameters['sqlite file'] = 'default.sql'
        self.filename = parameters['sqlite file']

        if not os.path.exists(parameters['sqlite file']):
            self.create_file()

        self.edit = False
        if 'edit' in parameters:
            self.edit = parameters['edit']

    def create_file(self):
        with sqlite3.connect(self.filename) as con:
            cur = con.cursor()

            # Types of days
            cur.execute(
                'CREATE TABLE IF NOT EXISTS dayTypes (id INT, key STR, desc STR);')
            cur.execute(
                'INSERT INTO dayTypes (id, key, desc) VALUES(1, "office", "Working at the office");')
            cur.execute(
                'INSERT INTO dayTypes (id, key, desc) VALUES(2, "wfh", "Home office");')
            cur.execute(
                'INSERT INTO dayTypes (id, key, desc) VALUES(3, "trip", "Business trip");')
            cur.execute(
                'INSERT INTO dayTypes (id, key, desc) VALUES(4, "sick", "Sick day");')
            cur.execute(
                'INSERT INTO dayTypes (id, key, desc) VALUES(5, "free", "Holiday or other non-worked days");')

            # Days
            cur.execute(
                'CREATE TABLE IF NOT EXISTS days (date DATE, typeId INT);')

    def get_dayTypes(self):
        with sqlite3.connect(self.filename) as con:
            cur = con.cursor()

            cur.execute('SELECT key from dayTypes;')
            rows = cur.fetchall()

            return [e[0] for e in rows]

    def enter_day(self, values):
        val_date, val_type = values
        # print(val_date)
        # print(val_date.isoformat())
        # print(val_type)
        with sqlite3.connect(self.filename) as con:
            cur = con.cursor()

            # Check if there are no entry for that date
            cur.execute(
                'SELECT t.key FROM days AS d INNER JOIN dayTypes AS t ON d.typeId=t.id WHERE d.date=?;', (val_date.isoformat(),))
            rows = cur.fetchall()
            # print(rows)
            previous_entry = None
            if rows:
                previous_entry = rows[0][0]
            # print(previous_entry)

            # Get the Type ID
            cur.execute('SELECT id FROM dayTypes WHERE key=?;', (val_type,))
            rows = cur.fetchall()
            # print(rows)
            tid = rows[0][0]
            # print(tid)

            # Enter the new value
            if (previous_entry) and (previous_entry != val_type):
                if self.edit:
                    print('Updating from {} to {} for {}'.format(
                        previous_entry, val_type, val_date))
                    cur.execute('UPDATE days SET typeId=? WHERE date=?',
                                (tid, val_date.isoformat()))
                else:
                    sys.stderr.write('There is already entry for that date. Add the \'--edit\' option to update it.\n')
            else:
                cur.execute(
                    'INSERT INTO days (date, typeId) VALUES(?, ?);', (val_date.isoformat(), tid))

    def enter(self, table, values):
        if self.debug:
            print('Enter {} into {}'.format(values, table))

        if 'day' == table:
            self.enter_day(values)
