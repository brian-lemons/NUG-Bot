import sqlite3
import uuid


def add_to_database(id, column_name: str, data: tuple, table_name: str):
    #Get place holders
    placeholder_text="("
    for i in range(len(data)-1):
        new_text = "?,"
        placeholder_text = placeholder_text + new_text
    
    placeholder_text = placeholder_text + "?)"

    list = [data]

    connection = sqlite3.connect("game.db")
    cursor = connection.cursor()

    cursor.execute("SELECT rowid FROM "+ table_name + " WHERE "+ str(column_name) + "= ?", (id, ))
    data= cursor.fetchone()
  
    if data is None:
        cursor.executemany("INSERT INTO "+ table_name + " VALUES "+ placeholder_text + "", list)
  
        connection.commit()
    else:
        print("This data already exists key: " + str(column_name) + " id "  + str(id) + " table " + table_name)

    connection.close()


def add_to_database_type_sensitive(id, column_name: str, data: tuple, table_name: str):
    #Get place holders
    placeholder_text="("
    for i in range(len(data)-1):
        new_text = "?,"
        placeholder_text = placeholder_text + new_text
    
    placeholder_text = placeholder_text + "?)"

    list = [data]

    connection = sqlite3.connect("game.db",detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cursor = connection.cursor()

    cursor.execute("SELECT rowid FROM "+ table_name + " WHERE "+ str(column_name) + "= ?", (id, ))
    data= cursor.fetchone()
  
    if data is None:
        cursor.executemany("INSERT INTO "+ table_name + " VALUES "+ placeholder_text + "", list)
  
        connection.commit()
    else:
        print("This data already exists key: " + str(column_name) + " id "  + str(id) + " table " + table_name)

    connection.close()

def add_to_database_without_keycheck(data: tuple, table_name: str):
    #Get place holders
    placeholder_text="("
    for i in range(len(data)-1):
        new_text = "?,"
        placeholder_text = placeholder_text + new_text
    
    placeholder_text = placeholder_text + "?)"

    list = [data]

    connection = sqlite3.connect("game.db")
    cursor = connection.cursor()
 
    cursor.executemany("INSERT INTO "+ table_name + " VALUES "+ placeholder_text + "", list)
    connection.commit()

    connection.close()

def get_data_by_name(name, data_to_retrieve: str, table: str, column_name: str):
    connection = sqlite3.connect("game.db")
    cursor = connection.cursor()

    cursor.execute("SELECT "+ data_to_retrieve +" FROM " + table + " WHERE "+ str(column_name) +"=?",(name, ))
    item_row = cursor.fetchone()
    data = item_row[0]
    connection.commit()

    connection.close()

    return data

def get_data_by_id(id: str, data_to_retrieve: str, table: str, column_name: str):
    connection = sqlite3.connect("game.db")
    cursor = connection.cursor()
    cursor.execute("SELECT "+ data_to_retrieve +" FROM " + table + " WHERE "+ str(column_name) + "=?", (id, ))
    
    item_row = cursor.fetchone()
    data = item_row[0]

    connection.close()

    return data

def get_data_from_column(table: str, data_to_retrieve: str):
    connection = sqlite3.connect("game.db")
    connection.row_factory 
    cursor = connection.cursor()
    cursor.execute("SELECT "+ data_to_retrieve +" FROM " + table +"")

    data = cursor.fetchall()

    connection.close()

    data_list = convert_tuple_data_into_list(data)

    return data_list

def check_if_data_exists(id, table_name: str, column_name: str):
    connection = sqlite3.connect("game.db")
    cursor = connection.cursor()

    cursor.execute("SELECT rowid FROM "+ table_name +" WHERE "+ column_name +" = ?", (id, ))
    data= cursor.fetchone()

    if data == None:
        connection.close()
        return False
    else:
        connection.close()
        return True


def generate_random_id():
    id = str(uuid.uuid4().int)[:15]
    return id

def update_data(table_name: str, set_column: str, where_column: str, data_to_update, id):
    with sqlite3.connect("game.db") as connection:
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE "+ table_name +" SET "+ set_column +"= ? WHERE "+ where_column +"= ?", (data_to_update, id))
            connection.commit()
        except Exception as e:
            print(f"Error updating data: {e}")


def get_all_data_filter_col(id, table_name, column_name: str):
    connection = sqlite3.connect("game.db")
    connection.row_factory 
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM " + table_name + " WHERE " + column_name + " = ?", (id, ))
    data= cursor.fetchall()

    connection.close()

    return data

#Pulls single information only
def convert_tuple_data_into_list(data_tuple: tuple, location=0) -> list:
    data_list = []
    for row in data_tuple:
        record = row[location]
        data_list.append(record)
    return data_list

def custom_excute(sql: str, data_tuple: tuple):
    connection = sqlite3.connect("game.db")
    cursor = connection.cursor()

    cursor.execute(sql, data_tuple)

    connection.commit()
    connection.close()


def complex_query_fetchall(sql: str, binding_list: list):
    connection = sqlite3.connect("game.db")
    cursor = connection.cursor()

    data_list = []
    for i in range(len(binding_list)):
        data_list.append(binding_list[i])

    data_tuple = tuple(data_list)

    cursor.execute(sql, data_tuple, )
    
    result = cursor.fetchall()
    connection.close()
    return result

def add_table(table_name, table_string):
    connection = sqlite3.connect("game.db")
    cursor = connection.cursor()
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='" + table_name + "'").fetchall()
    if tables == []:
        cursor.execute("CREATE TABLE " +  table_name + "(" + table_string + ")")
        connection.commit()
    connection.close()


def alter_table(table_name, column_name):
    connection = sqlite3.connect("game.db")
    cursor = connection.cursor()

    # Use string formatting to construct the SQL query
    query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
    table = cursor.execute(query).fetchone()

    # Use a try/except block to check if the table exists
    try:
        table_name = table[0]
    except TypeError:
        print("Table not found")
        return

    # Use string formatting to construct the SQL query
    query = f"ALTER TABLE {table_name} ADD {column_name}"
    cursor.execute(query)
    connection.commit()
    connection.close()