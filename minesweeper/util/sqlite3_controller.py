import sqlite3


class SQLController:
    def __init__(self, db_file):
        self.PATH = db_file

        self.conn = sqlite3.connect(self.PATH)
        self.c = self.conn.cursor()

    def add(self, table, keys, values):

        # create the string for the command to be executed if the table exists
        if self.check_table_existence(table):
            command = 'INSERT INTO ' + table + ' ('
            for count, key in enumerate(keys):
                if count != 0:
                    command += ', '
                command += key
            command += ') VALUES ('
            for count in range(len(values)):
                if count != 0:
                    command += ', '
                command += '?'
            command += ')'

            # execute the command
            self.c.execute(command, tuple(values))
            self.conn.commit()

    def add_table(self, table_name, columns):

        # create the string for the command to be executed
        command = 'CREATE TABLE IF NOT EXISTS ' + table_name + ' ('
        for count, key in enumerate(columns):
            if count != 0:
                command += ', '
            command += key + ' ' + columns[key]
        command += ')'

        # execute the command
        self.c.execute(
            str(command)
        )
        self.conn.commit()

    def get_item(self, table, column, row_identifier):

        # read out and return an item
        if self.check_table_existence(table):
            self.c.execute(f'''SELECT {column} FROM {table} WHERE {row_identifier[0]} = ?''', (row_identifier[1],))
            return self.c.fetchall()[0]

    def get_row(self, table, identifier):

        # read out and return a row
        if self.check_table_existence(table):
            self.c.execute(f'''SELECT * FROM {table} WHERE {identifier[0]} = ?''', (identifier[1],))
            return self.c.fetchall()[0]

    def get_table(self, table):

        # read out and return a full table
        if self.check_table_existence(table):
            self.c.execute(f'''SELECT * FROM {table}''')
            return self.c.fetchall()

    def get_row_count(self, table):

        # read out the number of rows in the table
        if self.check_table_existence(table):
            self.c.execute(f'''SELECT COUNT(*) FROM {table}''')
            count = self.c.fetchall()
            return count[0][0]

    def check_row_existence(self, table, row):

        # check if a row in a specific table
        self.c.execute(f'SELECT * FROM {table} WHERE name="{row}"')
        return self.c.fetchall()

    def check_table_existence(self, table):

        # check if a table exists and return True or False
        self.c.execute(f'''SELECT name FROM sqlite_master WHERE type="table" AND name="{table}"''')
        if self.c.fetchall() == 0:
            return False
        else:
            return True

    def end(self):
        self.conn.close()
