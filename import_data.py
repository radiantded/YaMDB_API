import argparse
import csv
import os
import re
import sqlite3
import sys

from api_yamdb.settings import DATABASES


def main():
    parser = argparse.ArgumentParser(
        description="Import data from .csv files to DB api_yamdb"
    )
    parser.add_argument('-p', '--path', type=str, required=True,
                        help='Path to .csv file')
    parser.add_argument('-t', '--table', type=str, required=True,
                        help='DB tablename')
    args = parser.parse_args()

    csv_file, table_name = args.path, args.table

    if not(os.path.exists(csv_file) and os.path.isfile(csv_file)):
        print(f'{csv_file} wrong path to .csv file. Please check path.')
        sys.exit(1)

    db_path = DATABASES['default']['NAME']
    db_engine = DATABASES['default']['ENGINE']

    if db_engine != 'django.db.backends.sqlite3':
        print('Sorry, script allow only sqlite3 engine')
        sys.exit(0)

    db_connection = sqlite3.connect(db_path)
    cursor = db_connection.cursor()

    with open(csv_file, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row.pop('id', None)
            keys = "','".join(row.keys())
            values_list = row.values()
            values_list = list(map(lambda x: re.sub("'", '"', x), values_list))
            values = "','".join(values_list)
            cursor.execute(
                f"insert into {table_name} ('{keys}') values ('{values}')"
            )

    db_connection.commit()
    db_connection.close()
    print('Imported successfully!')


if __name__ == "__main__":
    main()
