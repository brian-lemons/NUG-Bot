import sqlite3
import csv
from helper import database

#This will be used to preload the database with stats that will be precoded and won't change.

def create_tables(table_name, table_string):
    database.add_table(table_name, table_string)

def store_data_without_kecheck(data_tuple: tuple, table_name: str): 
    database.add_to_database_without_keycheck(data_tuple, table_name)

def store_data_with_keycheck(id, id_column_name: str, data_tuple: tuple, table_name: str):
    database.add_to_database(id, id_column_name, data_tuple, table_name)

def load_tables():
    with open('datafiles/tables.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            table_name = row['table_name']
            table_string = row['table_string']

            create_tables(table_name, table_string)
            

def populate_database():
    connection = sqlite3.connect("game.db")
    load_tables()

    connection.close()