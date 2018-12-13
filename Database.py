import sqlite3
from sqlite3 import *
import pandas as pd


class Table:
    """
    DB initializes and manipulates SQLite3 tables.
    """

    def __init__(self, database='Database', table_name='Error', attributes='column1, column2', excel_file=None):
        """
        Creates a table with connection in the given database without inserting it.
        """
        self.__database = str(database)
        self.__connection = sqlite3.connect(self.__database + '.db')
        self.__cursor = self.__connection.cursor()
        self.__table_name = str(table_name)
        self.__attributes = str(attributes)
        self.__excel_file = str(excel_file) if excel_file is not None else None

    def get_database(self):
        """
        Returns the database of the table.
        """
        return self.__database

    def get_connection(self):
        """
        Returns the connection of the table.
        """
        return self.__connection

    def get_cursor(self):
        """
        Returns the cursor of the table.
        """
        return self.__cursor

    def get_table_name(self):
        """
        Returns the name of the table.
        """
        return self.__table_name

    def get_attributes(self):
        """
        Returns the attributes of the table.
        """
        return self.__attributes

    def get_excel_file(self):
        """
        Returns the excel_file of the table. Returns None if there is no file.
        """
        return self.__excel_file

    def close_connection(self):
        """
        Closes the connection with the given database.
        """
        self.__connection.commit()
        self.__connection.close()

    def convert_to_value_or_list(self, list_of_tuples):
        """
        Converts a given list of tuples in a list or a value if the list contains one value.
        """
        if len(list_of_tuples) == 1:
            return list_of_tuples[0][0]
        else:
            new_list = []
            for element in range(len(list_of_tuples)):
                new_list.append(list_of_tuples[element][0])
            return new_list

    def add_data(self, data):
        """
        Inserts data in a given table. The data is a list of tuples.
        """
        try:
            for row in range(len(data)):
                if len(data[row]) == 1:
                    query = 'INSERT INTO ' + self.__table_name + ' VALUES' + '(' + str(data[row]) + ')'
                    self.__cursor.execute(query)
                    self.__connection.commit()
                else:
                    query = 'INSERT INTO ' + self.__table_name + ' VALUES' + str(data[row])
                    self.__cursor.execute(query)
                    self.__connection.commit()
        except Error:
            print('Data insertion failed')

    def delete_data(self, attribute, data):
        """
        Deletes data in a given table.
        """
        try:
            query = 'DELETE FROM ' + self.__table_name + ' WHERE ' + str(attribute) + '=' + "'" + str(data) + "'"
            self.__cursor.execute(query)
            self.__connection.commit()
        except Error:
            print('Data deletion failed')

    def read_variable(self, data):
        """
        Reads the value of a variable.
        """
        query = 'SELECT ' + str(data) + ' FROM ' + self.__table_name
        self.__cursor.execute(query)
        variable = self.convert_to_value_or_list(self.__cursor.fetchall())
        return variable

    def select_data(self, select, attribute, data):
        """
        Searches data in the table given a list of data.
        """
        query = 'SELECT ' + str(select) + ' FROM ' + self.__table_name + ' WHERE ' + str(attribute) + '=' + "'" + str(data) + "'"
        self.__cursor.execute(query)
        fetched_data = self.convert_to_value_or_list(self.__cursor.fetchall())
        return fetched_data

    def select_data_of_date(self, select, date):
        """
        Selects data of a given date.
        """
        query = 'SELECT ' + str(select) + ' FROM ' + self.__table_name + ' WHERE ' + "datetime between '" + str(
            date) + " 00:00' and '" + str(date) + " 23:00'"
        self.__cursor.execute(query)
        data = self.__cursor.fetchall()
        fetched_data = self.convert_to_value_or_list(data)
        return fetched_data

    def select_data_last_hour(self, select, date):
        """
        Selects the data from the last hour of the day.
        """
        query = 'SELECT ' + str(select) + ' FROM ' + self.__table_name + ' WHERE ' + "datetime='" + str(date) + " 23:00'"
        self.__cursor.execute(query)
        data = self.__cursor.fetchall()
        fetched_data = self.convert_to_value_or_list(data)
        return fetched_data

    def print_table(self):
        """
        Prints every row in a given table.
        """
        try:
            query = 'SELECT * FROM ' + self.__table_name
            self.__cursor.execute(query)
            [print(row) for row in self.__cursor.fetchall()]
        except Error:
            print('No such table found')

    def update_variable(self,attribute, data):
        """
        Updates a variable in the table.
        """
        query = 'UPDATE ' + self.__table_name + ' SET ' + str(attribute) + '=' + "'" + str(
            data) + "'"
        self.__cursor.execute(query)
        self.__connection.commit()

    def update_data(self, attribute, data, key):
        """
        Updates data in the table.
        """
        query = 'UPDATE ' + self.__table_name + ' SET ' + str(attribute) + '=' + "'" + str(data) + "'" + ' WHERE ' + str(key)
        self.__cursor.execute(query)
        self.__connection.commit()

    def copy_column1_to_column2(self, column1, column2):
        """
        Copies the data of first column to the second column in the same table.
        """
        query = 'UPDATE ' + self.__table_name + ' SET ' + str(column2) + '=' + str(column1)
        self.__cursor.execute(query)
        self.__connection.commit()

    def create_view(self, attribute, condition, view_name):
        """
        Creates a view.
        """
        query = 'CREATE VIEW ' + str(view_name) + ' AS SELECT ' + str(attribute) + ' FROM ' + self.__table_name + ' WHERE ' + str(condition)
        self.__cursor.execute(query)

    def create_index(self, attribute):
        """
        Creates an index in the table.
        """
        index = str(attribute) + '_index'
        query = 'CREATE INDEX IF NOT EXISTS ' + index + ' ON ' + self.__table_name + '(' + str(attribute) + ')'
        self.__cursor.execute(query)

    def add_column(self, column_name, column_definition):
        """
        Adds the given column in the table with a column definition.
        The column definition must be TEXT, BLUB, INTEGER ...
        """
        try:
            query = 'AlTER TABLE ' + self.__table_name + ' ADD ' + str(column_name) + ' ' + str(column_definition)
            self.__cursor.execute(query)
            return True
        except Error:
            return False


class Database:
    """
    A database contains a list of tables.
    """

    def __init__(self, database_name):
        self.__tables = []
        self.__database_name = str(database_name)

    def get_tables(self):
        """
        Returns all tables that are in the database.
        """
        return self.__tables

    def add_table(self, new_table):
        """
        Adds the table to the list if it doesn't overlap with existing tables.
        """
        try:
            if new_table not in self.__tables:
                self.__tables.append(new_table)

                if new_table.get_excel_file() is None:
                    query = 'CREATE TABLE IF NOT EXISTS ' + new_table.get_table_name() + '(' + new_table.get_attributes() + ')'
                    new_table.get_cursor().execute(query)
                    return True
                else:
                    workbook = pd.read_excel(new_table.get_excel_file(), sheetname=False, header=0, name=None, index_col=None, parse_cols=None)
                    workbook.to_sql(name='Excel', con=new_table.get_connection(), schema=None, if_exists='replace')
                    query = 'CREATE TABLE IF NOT EXISTS ' + new_table.get_table_name() + '(' + new_table.get_attributes() + ')'
                    new_table.get_cursor().execute(query)
                    query1 = 'INSERT INTO ' + new_table.get_table_name() + ' SELECT ' + new_table.get_attributes() + ' FROM Excel'
                    new_table.get_cursor().execute(query1)
                    query2 = 'DROP TABLE IF EXISTS Excel'
                    new_table.get_cursor().execute(query2)
                    new_table.get_connection().commit()
                    return True
        except Error:
            return False

    def remove_table(self, old_table):
        """
        Removes a table from the database.
        """
        if old_table in self.get_tables():
            self.__tables.remove(old_table)
            query = 'DROP TABLE IF EXISTS ' + old_table.get_table_name()
            old_table.get_cursor().execute(query)
            return True
        return False

    def remove_all_tables(self):
        """
        Removes all tables in the database.
        """
        all_tables = self.get_tables()
        for i in range(len(all_tables)):
            self.remove_table(all_tables[0])
