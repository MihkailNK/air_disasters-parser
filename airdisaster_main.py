# coding: UTF8

import sys
import os

from ad_database import ADDatabase
from ad_parsers import DisasterParser, YearParser
from ad_main_class import Disaster


# Collect information on the period
def get_disasters_of_the_year(year):
    disasters_list = []
    y_parser = YearParser(year)
    disasters_ids_list = y_parser.get_disasters_ids()
    for disaster_id in disasters_ids_list:
        disaster = Disaster()
        disaster.disaster_id = disaster_id
        disaster.date = year

        d_parser = DisasterParser(disaster_id)
        stat= d_parser.get_statistic()
        disaster.personal = stat            # Victims in personal and personal count
        disaster.passengers = stat          # Victims in passengers and passengers count
        disaster.vict_onland = stat['v_onland']
        disaster.total = stat['total']
        date_dict = d_parser.get_date()
        if disaster.try_int(date_dict['y']):
            disaster.date = date_dict
        disasters_list.append(disaster)
    return disasters_list


# Calculation of the number of victims of the disaster
def get_disasters_of_the_period(year1, year2):
    disasters_on_period = {y: [] for y in range(year1, year2 + 1)}
    for y in range(year1, year2 + 1):
        disasters_on_period[y] = get_disasters_of_the_year(y)
    return disasters_on_period

# Load indormation in format {year: [Disaster, Disaster,...], year:...} into SQLite database
def load_to_db(disasters):
    db_name = 'AirDisasters.db'
    db = ADDatabase(db_name)
    if not db.try_exist():
        db.create()
    db.connect()
    for period in disasters:
            for disaster in disasters[period]:
                db.insert(disaster.simple)
    db.disconnect()

def liad_from_db():
    db_name = 'AirDisasters.db'
    db = ADDatabase(db_name)
    if not db.try_exist():
        return False
    db.connect()
    print(db.select())

def main():
    year = 2003
    year2 = 2003

    disasters_on_the_perion  = get_disasters_of_the_period(year, year2)
    load_to_db(disasters_on_the_perion)
    liad_from_db()


if __name__ == '__main__':
    main()
