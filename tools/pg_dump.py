import os
import sys

def pg_dump_win():
    PG_DUMP = 'pg_dump' # Add PostgreSQL bin directory to the environment variables `PATH`
    SQL_SCRIPT_FILE = '../db/postgres/pg_dump.sql'
    CMDLINE = '''{pg_dump} --host=localhost --port=5432 --username=postgres --password --role=stocktotal --file="{file}" --schema-only stocktotal'''.format(
        pg_dump=PG_DUMP,
        file=SQL_SCRIPT_FILE
    )
    print(CMDLINE)
    os.system(CMDLINE)

    
    
def pg_dump_mac():
    raise NotImplementedError

    
    
def main():
    import platform
    curr_platform = platform.system()
    if curr_platform == 'Windows':
        pg_dump_win()
    elif curr_platform == 'Darwin':
        pg_dump_mac()
    else:
        raise Exception('Please add support for your platform')
        


if __name__ == '__main__':
    sys.exit(main())
