import argparse
import os
import sqlite3
import sys

import pandas as pd

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
    data = pd.read_csv(csv_file)

    # Exclude id column and import to DB
    data = data.loc[:, data.columns != 'id']
    data.to_sql(table_name, db_connection, if_exists='append', index=False)

    print('Imported successfully!')


if __name__ == "__main__":
    main()
