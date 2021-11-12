from sqlite3 import Error, connect

NEW_TBL_USERS = '''CREATE TABLE users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        token TEXT NOT NULL,
        email TEXT,
        image TEXT,
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
        object JSON,
        object_id INT);
        '''

NEW_TBL_CHATS = '''CREATE TABLE chats(
        id INTEGER NOT NULL,
        user_id INT NOT NULL
        );
        '''

        
NEW_TBL_BUGS = '''CREATE TABLE bugs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INT NOT NULL,
        title TEXT NOT NULL,
        priority INTEGER NOT NULL,
        steps TEXT NOT NULL,
        actual TEXT NOT NULL,
        expected TEXT NOT NULL,
        status INT NOT NULL default 0
        );
        '''
NEW_TBL_GROUPS = '''CREATE TABLE groups(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_id INT NOT NULL,
        name TEXT NOT NULL,
        users TEXT NOT NULL default "[]",
        admins TEXT NOT NULL default "[]",
        type INT NOT NULL
        );
        '''
INIT_ADMIN='''insert into users (id,name,token)
    values (0,'admin','{token}')'''

def exec(query,s=""):
    res = ""
    cn = connect('/databases/db.sqlite3')
    c=cn.cursor()
    if s == "":
        c.execute(query)
    else: c.execute(query,s)
    cn.commit()
    res = c.fetchall()
    c.close
    return res

def drop(yes:str,admintoken="admin"):
    exec('''DROP TABLE IF EXISTS users;''')
    exec(NEW_TBL_USERS)
    exec(INIT_ADMIN.replace("{token}",admintoken))
    exec('''DROP TABLE IF EXISTS messages;''')
    exec(NEW_TBL_MESSAGES)
    exec('''DROP TABLE IF EXISTS updates;''')
    exec(NEW_TBL_UPDATES)
    exec('''DROP TABLE IF EXISTS chats;''')
    exec(NEW_TBL_CHATS)
    exec('''DROP TABLE IF EXISTS bugs;''')
    exec(NEW_TBL_BUGS)
    exec('''DROP TABLE IF EXISTS groups;''')
    exec(NEW_TBL_GROUPS)
def update():
        ...
