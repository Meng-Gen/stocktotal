# coding: utf-8

import os
import sys
    
def main():
    SQL_SCRIPT_FILE = '../db/postgres/pg_dump.sql'
    # In Windows platform, please add PostgreSQL bin directory to the environment variables `PATH`
    CMDLINE = '''pg_dump --host=localhost --port=5432 --username=postgres --password --role=stocktotal --file="{file}" --schema-only stocktotal'''.format(
        file=SQL_SCRIPT_FILE
    )
    os.system(CMDLINE)
        


if __name__ == '__main__':
    sys.exit(main())
