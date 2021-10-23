from sqlite3 import Error, connect

NEW_TBL_USERS = '''CREATE TABLE users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        token TEXT NOT NULL,
        email TEXT,
        password TEXT,
        online_state TEXT);
        '''

NEW_TBL_MESSAGES = '''CREATE TABLE messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_id INT NOT NULL,
        to_id INT NOT NULL,
        text TEXT);
        '''

NEW_TBL_UPDATES = '''CREATE TABLE updates(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INT NOT NULL,
        type INT NOT NULL,
        time integer(6) not null default (strftime('%s','now')),
        object_id INT);
        '''

INIT_ADMIN='''insert into users (id,name,token)
    values (0,'admin','admin')'''

def exec(query,s=""):
    res = ""
    cn = connect('/databases/sqlite3')
    c=cn.cursor()
    if s == "":
        c.execute(query)
    else: c.execute(query,s)
    cn.commit()
    res = c.fetchall()
    c.close
    return res

def drop(yes:str):
    exec('''DROP TABLE IF EXISTS users;''')
    exec(NEW_TBL_USERS)
    exec(INIT_ADMIN)
    exec('''DROP TABLE IF EXISTS messages;''')
    exec(NEW_TBL_MESSAGES)
    exec('''DROP TABLE IF EXISTS updates;''')
    exec(NEW_TBL_UPDATES)
