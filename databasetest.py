
from sqlite3 import Error, connect


def create_connection(path):
    """
    Generates connection to database under specified path.

    :param path: path to database
    :return: connection to database
    """

    connection = None

    try:
        connection = connect(path)
    except Error as error:
        print(f"The error '{error}' occurred")

    return connection
def execute_query(connection, query, data=None):
    """
    Performs given query in specified database.

    :param connection: connection to database
    :param query: string of query to execute
    :param data: dict of additional data to paste in query
    """

    cursor = connection.cursor()

    try:
        if data:
            cursor.execute(query, data)
            connection.commit()
            cursor.close()

        else:
            cursor.execute(query)
            connection.commit()
            cursor.close()

    except Error as error:
        print(f"The error '{error}' occurred")
def execute_read_query(connection, query, flag=1, data=None):
    """
    Collects data from database which match to given query

    :param connection: connection to database
    :param query: string of query to execute
    :param flag: switch, 1 - get list of the matching rows,
                         0 - retrieve a single matching row
    :param data: dict of additional data to paste in query
    :return: depending on :param flag: matching query data
    """

    cursor = connection.cursor()
    result = None

    try:
        if data:
            cursor.execute(query, data)
            result = cursor.fetchall() if flag else cursor.fetchone()
            cursor.close()
            return result

        else:
            print(query)
            cursor.execute(query)
            result = cursor.fetchall() if flag else cursor.fetchone()
            cursor.close()
            return result

    except Error as error:
        print(f"The error '{error}' occurred")


c = create_connection('db.sqlite3')

crtbl = '''CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token TEXT NOT NULL,
    name TEXT NOT NULL);'''

useradd = '''insert into users (name,token)
values ('user','testokentipohesh')'''


#db.execute_query(c,crtbl)
#db.execute_query(c,useradd)
D = execute_query(c,'''select * from users where token = "testokentipohesh" ''')

print(D)