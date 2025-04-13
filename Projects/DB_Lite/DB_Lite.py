import os
import sqlite3
from tabulate import tabulate

class Database:
    def __init__(self, filename):
        current_path = os.path.dirname(os.path.abspath(__file__))
        self.path = os.path.join(current_path, 'Databases')
        if not os.path.exists(self.path): os.makedirs(self.path)
        self.filename = os.path.join(self.path, filename)
        self.create_database()

    def database_exists(self):
        return os.path.exists(self.filename)
    
    def create_database(self):
        if self.database_exists():
            print(f'The database "{self.filename}" already exists.')
        else:
            conn = sqlite3.connect(self.filename)
            conn.close()

    def open(self):
        if self.database_exists():
            return sqlite3.connect(self.filename)
        else:
            print(f'The database "{self.filename}" does not exist.')
    def table_exists(self, table):
        database = self.open()
        database = database.execute(f'PRAGMA table_info({table})')
        if database.fetchone() is None:
            database.close()
            return False
        database.close()
        return True
    
    def create_table(self, table, sql_command):
        database = self.open()
        if self.table_exists(table):
            print(f'The table "{table}" already exists.')
        else:
            database.execute(f'CREATE TABLE IF NOT EXISTS {table} ({sql_command})')
            database.close()

    def delete_table(self, table):
        database = self.open()
        if self.table_exists(table):
            database.execute(f'DROP TABLE {table}')
            database.commit()
            database.close()
        else:
            print(f'The table "{table}" does not exist in order to be deleted.')

    def insert_into_table(self, table, values):
        if self.table_exists(table):
            database = self.open()
            database.execute(f'INSERT INTO {table} VALUES {values}')
            database.commit()
            database.close()
        else:
            print(f'The table "{table}" does not exist in order to be inserted.')

    def print_table(self, table):
        if self.table_exists(table):
            database = self.open()
            database = database.execute(f'SELECT rowid, * FROM {table}')
            os.system('cls')
            print()
            print(f'Table: {table}')
            print(tabulate(database, headers='keys', tablefmt='fancy_grid', numalign="center",stralign = "center"))
            database.close()
            print()
        else:
            print(f'The table "{table}" does not exist in order to be printed.')

    def row_hash(self,table, row):
        database = self.open()
        database = database.execute(f'SELECT * FROM {table}')
        string = ""
        rows = database.fetchall()
        if row > len(rows):  return f"Row {row} does not exist in the table."
        string = string.join(map(str, rows[row]))
        string = hashlib.sha224(string.encode()).hexdigest()    
        return string

    def update_hashes(self, table):
        database = self.open()
        database = database.execute(f'SELECT rowid, * FROM {table}')
        rows = database.fetchall()
        database.close()
        database = self.open()
        for row in rows:
            database.execute(f'UPDATE {table} SET hash_id = "{self.row_hash(table, row[0]-1)}" WHERE rowid = {row[0]}')
        database.commit()
        database.close()