import os
import sqlite3
import sys


class db:
    #===============================================
    # Initialisation
    #-----------------------------------------------
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

    #===============================================
    # Create a DB file
    #-----------------------------------------------
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

            # Types of clocks
            cur.execute(
                'CREATE TABLE IF NOT EXISTS clockTypes (id INT, key STR, desc STR);')
            cur.execute(
                'INSERT INTO clockTypes (id, key, desc) VALUES(1, "in", "Clock-in");')
            cur.execute(
                'INSERT INTO clockTypes (id, key, desc) VALUES(2, "out", "Clock-out");')

            # Clocks
            cur.execute(
                'CREATE TABLE IF NOT EXISTS clocks (id INT, date DATE, time TIME, typeId INT);')

            # Categories
            cur.execute(
                'CREATE TABLE IF NOT EXISTS categories (id INT, name STR, desc STR);')

            # Projects
            cur.execute(
                'CREATE TABLE IF NOT EXISTS projects (id INT, name STR, catId INT, desc STR);')

            # Types of bookings
            cur.execute(
                'CREATE TABLE IF NOT EXISTS bookingsTypes (id INT, key STR, desc STR);')
            cur.execute(
                'INSERT INTO bookingsTypes (id, key, desc) VALUES(1, "start", "Start the action");')
            cur.execute(
                'INSERT INTO bookingsTypes (id, key, desc) VALUES(2, "stop", "Stop the action");')

            # Bookings
            cur.execute(
                'CREATE TABLE IF NOT EXISTS bookings (id INT, date DATE, time TIME, prjId INT, typeId INT, com STR);')

            # Last ID
            cur.execute(
                'CREATE TABLE IF NOT EXISTS lastId (tablename STR, lastId INT);')
            cur.execute(
                'INSERT INTO lastId (tablename, lastId) VALUES("clocks", 0);')
            cur.execute(
                'INSERT INTO lastId (tablename, lastId) VALUES("categories", 0);')
            cur.execute(
                'INSERT INTO lastId (tablename, lastId) VALUES("projects", 0);')
            cur.execute(
                'INSERT INTO lastId (tablename, lastId) VALUES("bookings", 0);')

    #===============================================
    # Days functions
    #-----------------------------------------------
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

    def get_all_days(self):
        out = None
        with sqlite3.connect(self.filename) as con:
            cur = con.cursor()

            # Check if there are no entry for that date
            cur.execute(
                'SELECT d.date,t.desc FROM days AS d INNER JOIN dayTypes AS t ON d.typeId=t.id ORDER BY d.date;')
            out = cur.fetchall()

        return out

    def delete_days(self, values):
        with sqlite3.connect(self.filename) as con:
            cur = con.cursor()

            # Check if there are no entry for that date
            cur.execute(
                'DELETE FROM days WHERE date=?;', (values,))


    def report_days(self, start_date, end_date):
        out=None
        with sqlite3.connect(self.filename) as con:
            cur = con.cursor()

            # Check if there are no entry for that date
            cmd = 'SELECT t.desc, COUNT(*) FROM days AS d INNER JOIN dayTypes AS t ON t.id=d.typeId WHERE date>=? AND date<=? GROUP BY d.typeId;'
            if self.debug:
                print(cmd)
            cur.execute(cmd , (start_date, end_date))
            out=cur.fetchall()

        return out

    def read_days(self, date):
        out=None
        with sqlite3.connect(self.filename) as con:
            cur = con.cursor()

            # Check if there are no entry for that date
            cmd = 'SELECT d.date, t.desc FROM days AS d INNER JOIN dayTypes AS t ON t.id=d.typeId WHERE date=?;'
            if self.debug:
                print(cmd)
            cur.execute(cmd , (date,))
            out=cur.fetchall()

        return out


    #===============================================
    # Clocks functions
    #-----------------------------------------------
    def enter_clock(self, values):
        # Get the values
        val_date, val_time, val_io = values

        with sqlite3.connect(self.filename) as con:
            cur = con.cursor()

            # Get the type ID
            cur.execute('SELECT id FROM clockTypes WHERE key=?;', (val_io,))
            rows = cur.fetchall()
            tid = rows[0][0]

            # Get the last entered Id
            cur.execute('SELECT lastId FROM lastId WHERE tablename="clocks";')
            rows=cur.fetchall()
            new_id = int(rows[0][0])+1

            # New entry
            cur.execute('INSERT INTO clocks (id, date, time, typeId) VALUES(?, ?, ?, ?);', (new_id, val_date.isoformat(), val_time, tid))

            # Update the last Id
            cur.execute('UPDATE lastId SET lastId=? WHERE tablename="clocks";', (new_id,))
    

    def get_all_clocks(self):
        out = None
        with sqlite3.connect(self.filename) as con:
            cur = con.cursor()

            # Check if there are no entry for that date
            cur.execute(
                'SELECT c.id, c.date,c.time,t.desc FROM clocks AS c INNER JOIN clockTypes AS t ON c.typeId=t.id ORDER BY c.date, c.time;')
            out = cur.fetchall()

        return out

    def read_clocks(self, values):
        val_date, val_time = values
        out = None
        with sqlite3.connect(self.filename) as con:
            cur = con.cursor()

            # Check if there are no entry for that date
            cur.execute(
                'SELECT MAX(c.time),t.desc FROM clocks AS c INNER JOIN clockTypes AS t ON c.typeId=t.id WHERE c.date=? AND c.time<? ORDER BY c.time;', (val_date, val_time))
            out = cur.fetchall()

        return out



    #===============================================
    # Projects functions
    #-----------------------------------------------
    def enter_prj(self, values):
        # Get the values
        val_name, val_cat, val_desc, val_edit = values

        with sqlite3.connect(self.filename) as con:
            cur = con.cursor()

            # Check if the entry does not already exist
            cur.execute('SELECT * FROM projects WHERE name=?;', (val_name,))
            rows = cur.fetchall()
            if rows:
                if not val_edit:
                    sys.stderr.write('The given category ({}) is already known as {}\n'.format(val_name, rows[0][2]))
                    sys.exit(1)
                else:
                    if self.debug:
                        print('Updating {} to {}'.format(val_name, val_desc))
                    cur.execute('UPDATE projects SET desc=? WHERE name=?', (val_desc, val_name))
                    cur.execute('UPDATE projects SET catId=? WHERE name=?', (val_cat, val_name))

            else:
                # Check that the category is known
                cur.execute('SELECT id FROM categories WHERE name=?;', (val_cat,))
                rows=cur.fetchall()

                if not rows:
                    sys.stderr.write('Unkown category\n')
                    sys.exit(1)
                else:
                    catId = rows[0][0]

                    # Get the last entered Id
                    cur.execute('SELECT lastId FROM lastId WHERE tablename="projects";')
                    rows=cur.fetchall()
                    new_id = int(rows[0][0])+1

                    # New entry
                    cur.execute('INSERT INTO projects (id, name, catId, desc) VALUES(?, ?, ?, ?);', (new_id, val_name, catId, val_desc))

                    # Update the last Id
                    cur.execute('UPDATE lastId SET lastId=? WHERE tablename="projects";', (new_id,))
    

    def get_all_prj(self):
        out = None
        with sqlite3.connect(self.filename) as con:
            cur = con.cursor()

            cur.execute(
                'SELECT p.name, c.name, p.desc FROM projects p INNER JOIN categories c ON p.catId = c.id;')
            out = cur.fetchall()

        return out

    def delete_prj(self, values):
        val_name, = values
        if self.debug:
            print('val_name={}'.format(val_name))

        with sqlite3.connect(self.filename) as con:
            cur = con.cursor()

            # Check if the entry does not already exist
            cur.execute('SELECT * FROM projects WHERE name=?;', (val_name,))
            rows = cur.fetchall()

            # Delete it
            if rows:
                cur.execute('DELETE FROM projects WHERE name=?', (val_name,))

    #===============================================
    # Categories functions
    #-----------------------------------------------
    def enter_cat(self, values):
        # Get the values
        val_name, val_desc, val_edit = values

        with sqlite3.connect(self.filename) as con:
            cur = con.cursor()

            # Check if the entry does not already exist
            cur.execute('SELECT * FROM categories WHERE name=?;', (val_name,))
            rows = cur.fetchall()
            if rows:
                if not val_edit:
                    sys.stderr.write('The given category ({}) is already known as {}\n'.format(val_name, rows[0][2]))
                    sys.exit(1)
                else:
                    if self.debug:
                        print('Updating {} to {}'.format(val_name, val_desc))
                    cur.execute('UPDATE categories SET desc=? WHERE name=?', (val_desc, val_name))

            else:
                # Get the last entered Id
                cur.execute('SELECT lastId FROM lastId WHERE tablename="categories";')
                rows=cur.fetchall()
                new_id = int(rows[0][0])+1

                # New entry
                cur.execute('INSERT INTO categories (id, name, desc) VALUES(?, ?, ?);', (new_id, val_name, val_desc))

                # Update the last Id
                cur.execute('UPDATE lastId SET lastId=? WHERE tablename="categories";', (new_id,))
    

    def get_all_cat(self):
        out = None
        with sqlite3.connect(self.filename) as con:
            cur = con.cursor()

            cur.execute(
                'SELECT name, desc FROM categories;')
            out = cur.fetchall()

        return out

    def delete_cat(self, values):
        val_name, = values
        if self.debug:
            print('val_name={}'.format(val_name))

        with sqlite3.connect(self.filename) as con:
            cur = con.cursor()

            # Check if the entry does not already exist
            cur.execute('SELECT * FROM categories WHERE name=?;', (val_name,))
            rows = cur.fetchall()

            # Delete it
            if rows:
                cur.execute('DELETE FROM categories WHERE name=?', (val_name,))


    #===============================================
    # Bookings functions
    #-----------------------------------------------
    def enter_book(self, values):
        # Get the values
        val_time, val_date, val_startstop, val_prj, val_m, val_edit = values

        with sqlite3.connect(self.filename) as con:
            cur = con.cursor()

            # Get the project id
            cur.execute('SELECT id FROM projects WHERE name=?', (val_prj,))
            rows=cur.fetchall()

            if rows:
                prjid = rows[0][0]

                # Get the last entered Id
                cur.execute('SELECT lastId FROM lastId WHERE tablename="bookings";')
                rows=cur.fetchall()
                new_id = int(rows[0][0])+1

                # Get the type Id
                cur.execute('SELECT id FROM bookingsTypes WHERE key=?', (val_startstop,))
                rows=cur.fetchall()
                typeid=rows[0][0]

                # New entry
                cur.execute('INSERT INTO bookings (id, date, time, prjId, typeId, com) VALUES(?, ?, ?, ?, ?, ?);', (new_id, val_date, val_time, prjid, typeid, val_m))

                # Update the last Id
                cur.execute('UPDATE lastId SET lastId=? WHERE tablename="bookings";', (new_id,))
    

    def get_all_book(self):
        out = None
        with sqlite3.connect(self.filename) as con:
            cur = con.cursor()

            cur.execute(
                'SELECT name, desc FROM categories;')
            out = cur.fetchall()

        return out

    def delete_book(self, values):
        val_name, = values
        if self.debug:
            print('val_name={}'.format(val_name))

        with sqlite3.connect(self.filename) as con:
            cur = con.cursor()

            # Check if the entry does not already exist
            cur.execute('SELECT * FROM categories WHERE name=?;', (val_name,))
            rows = cur.fetchall()

            # Delete it
            if rows:
                cur.execute('DELETE FROM categories WHERE name=?', (val_name,))


    #===============================================
    # Generic functions
    #-----------------------------------------------
    def enter(self, table, values):
        if self.debug:
            print('Enter {} into {}'.format(values, table))

        if 'day' == table:
            self.enter_day(values)
        elif 'clock' == table:
            self.enter_clock(values)
        elif 'cat' == table:
            self.enter_cat(values)
        elif 'prj' == table:
            self.enter_prj(values)
        elif 'book' == table:
            self.enter_book(values)


    def get_all(self, table):
        if self.debug:
            print('Get all from {}'.format(table))

        out = None
        if 'day' == table:
            out = self.get_all_days()
        elif 'clock' == table:
            out = self.get_all_clocks()
        elif 'cat' == table:
            out = self.get_all_cat()
        elif 'prj' == table:
            out = self.get_all_prj()
        return out

    def delete(self, table, values):
        if self.debug:
            print('Deleting an entry from {} with the parameters {}'.format(table, values))

        if 'day' == table:
            self.delete_days(values)
        elif 'cat' == table:
            self.delete_cat(values)
        elif 'prj' == table:
            self.delete_prj(values)

    def report(self, table, start_date, end_date):
        if self.debug:
            print('Reporting {} from {} to {}'.format(table, start_date, end_date))

        if 'days' == table:
            return (self.report_days(start_date, end_date))

    def read(self, table, values):
        if self.debug:
            print('Reading an entry from {} with the parameters {}'.format(table, values))

        if 'day' == table:
            return(self.read_days(values))
        elif 'clock' == table:
            return(self.read_clocks(values))
