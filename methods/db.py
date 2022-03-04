import os
from sqlite3 import connect
import cfg
NEW_TBL_USERS = '''CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        token TEXT NOT NULL,
        email TEXT,
        image TEXT,
        password TEXT,
        code TEXT,
        verifi INT default 0,
        online_state TEXT);
        '''

NEW_TBL_ACCOUNTS = '''CREATE TABLE IF NOT EXISTS accounts(
    user INT NOT NULL,
    ac_token TEXT NOT NULL,
    ac_id INT NOT NULL,
    ac_email TEXT,
    ac_number INT,
    social_name TEXT NOT NULL);
'''

NEW_TBL_MESSAGES = '''CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_id INT NOT NULL,
        to_id INT NOT NULL,
        time integer(6) not null default (strftime('%s','now')),
        text TEXT);
        '''

NEW_TBL_COMMENTS = '''CREATE TABLE IF NOT EXISTS comments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_id INT NOT NULL,
        post_id INT NOT NULL,
        etxra INT,
        time integer(6) not null default (strftime('%s','now')),
        text TEXT);
        '''

NEW_TBL_POOL = '''CREATE TABLE IF NOT EXISTS pool(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INT NOT NULL,
        type INT NOT NULL,
        time integer(6) not null default (strftime('%s','now')),
        object JSON,
        readed BOOLEAN default 0,
        object_id INT);
        '''

NEW_TBL_CHATS = '''CREATE TABLE IF NOT EXISTS chats(
        id INTEGER NOT NULL,
        name TEXT NOT NULL,
        user_id INT NOT NULL);
        '''


NEW_TBL_BUGS = '''CREATE TABLE IF NOT EXISTS bugs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INT NOT NULL,
        title TEXT NOT NULL,
        priority INTEGER NOT NULL,
        steps TEXT NOT NULL,
        actual TEXT NOT NULL,
        expected TEXT NOT NULL,
        product INT NOT NULL,
        status INT NOT NULL default 0);
        '''
NEW_TBL_GROUPS = '''CREATE TABLE IF NOT EXISTS groups(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_id INT NOT NULL,
        name TEXT NOT NULL,
        users TEXT NOT NULL default "[]",
        admins TEXT NOT NULL default "[]",
        type INT NOT NULL);
        '''

NEW_TBL_VUL = '''CREATE TABLE IF NOT EXISTS vul(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text INT NOT NULL);
        '''

NEW_TBL_ACH = '''CREATE TABLE IF NOT EXISTS achivs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        groupid INT NOT NULL,
        image TEXT);
        '''

INIT_ADMIN = '''insert into users (id,name,token)
    values (0,'admin','{token}')'''


def exec(query, s=""):
    res = ""
    print(">> " + str((query, s)) + "\n" + str(res))
    cn = connect(cfg.dataBaseFile)
    c = cn.cursor()
    if s == "":
        c.execute(query)
    else:
        c.execute(query, s)
    cn.commit()
    res = c.fetchall()
    c.close
    return res


def drop(yes: str):
    os.remove(cfg.dataBaseFile)


def update(admintoken="admin"):
    exec(NEW_TBL_USERS)
    # exec(INIT_ADMIN.replace("{token}",admintoken))
    exec(NEW_TBL_MESSAGES)
    exec(NEW_TBL_POOL)
    exec(NEW_TBL_ACH)
    exec(NEW_TBL_CHATS)
    exec(NEW_TBL_BUGS)
    exec(NEW_TBL_GROUPS)
    exec(NEW_TBL_COMMENTS)
    exec(NEW_TBL_ACCOUNTS)
    exec(NEW_TBL_VUL)
