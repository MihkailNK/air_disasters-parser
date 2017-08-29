import sqlite3
import sys
import os


# Class for interacting with the SQLite database
class ADDatabase:
    def __init__(self, dbname='Air_Disaster.db'):
        self.name = dbname
        self.cursor = None
        self._db_connect= None

    def connect(self):
        try:
            self._db_connect = sqlite3.connect(self.name,detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        except Exception:
            print("Error connecting to DB: ", Exception)
            self.cursor = None
            return False
        else:
            self.cursor = self._db_connect.cursor()
            return True

    # Checking the existence of the database file
    def try_exist(self):
        if os.path.isfile(self.name):
            return True
        return False

    def disconnect(self):
        self._db_connect.close()
        self.cursor = None

    def select(self, params='*'):
        ex_str = 'SELECT '+params+' FROM disasters'
        if self._db_connect:
            self.cursor.execute(ex_str)
            data = self.cursor.fetchall()
            return data
        return None

    def create(self):
        if self.connect():
            self.cursor.execute('CREATE TABLE disasters(id INTEGER PRIMARY KEY, disaster_id INTEGER UNIQUE, victims_onland INTEGER, victims_personal INTEGER, victims_passengers INTEGER, personal INTEGER, passengers INTEGER, victims_total INTEGER, date DATE)')
            self._db_connect.commit()

    def insert(self, disaster_data):
        if self.connect():
            dat = {key: disaster_data[key] if str(disaster_data[key]).isdigit() else -1  for key in disaster_data}
            dat.update({'date': disaster_data['date']})
            try:
                ex_str = 'INSERT INTO ' \
                         'disasters(id, disaster_id, victims_onland, victims_personal, victims_passengers, personal, passengers, victims_total, date)' \
                         """ VALUES (NULL, {id}, {v_onland}, {v_personal}, {v_passengers}, {personal}, {passengers}, {v_total}, '{date}')""".format(**dat)
                self.cursor.execute(ex_str)
                self._db_connect.commit()
                return True
            except:
                fmode = 'a'
                if not os.path.isfile('error_log.txt'):
                    fmode = 'w'
                f = open("error_log.txt", fmode)
                print(sys.exc_info(), '  disaster ID: ', dat['id'])
                f.write(str(dat['id'])+str(sys.exc_info())+ '\n')
                f.close()
        return False





