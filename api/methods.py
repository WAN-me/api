from sqlite3 import Error, connect
import hashlib,time

NEW_BD = '''CREATE TABLE users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT NOT NULL,
            online_state TEXT,
            name TEXT NOT NULL);'''


############################
###user
############################
def userget(args):
    ss = notempty(args,['accesstoken'])
    if ss == True: 
        token = args['accesstoken']
        user = (db(f'''select id,name,token,online_state from users where token = "{token}" '''))
        print(user)
        if not user or len(user)!=1:
            return error(2,"'accesstoken' is invalid")
        else:
            return {'id':user[0][0],'name':user[0][1],'token':user[0][2],'online_state':user[0][3]}
    else:
        return ss
def reg(args):
    ss = notempty(args,['name'])
    if ss == True:
        name = args['name']
        token = hashlib.sha256(f'{name}_{time.time()}'.encode()).hexdigest()
        db(f'''insert into users (name,token)
        values ('{name}','{token}')''')
        return userget({'accesstoken':token})
    else: return ss


############################
###database
############################
def db(query):
    print(query)
    res = ""
    cn = connect('db.sqlite3')
    c=cn.cursor()
    c.execute(query)
    cn.commit()
    res = c.fetchall()
    c.close
    return res


def dropdatabase(args):
    user = userget(args)
    print(user)
    if not 'error' in user:
        if user['id'] == 1:
            db('''DROP table users ''')
            db(NEW_BD)
            return {'state':'done'}
        else:
            return error(4,"access denided for this method")
    else: return user

def dropdatabase(yes:str):
    db('''DROP TABLE IF EXISTS users;''')
    db(NEW_BD)
    db(f'''insert into users (id,name,token)
        values (0,'admin','admin')''')
    return {'state':'done'}


############################
###utils
############################

def error(code,text):
    return {'error':{"code":code,"text":text}}


def notempty(args,need):
    empty=[]
    for key in need:
        name = args.get(key)
        if not name or name=='':
            empty.append(key)
    if len(empty)==0:
        return True
    else: return error(3,f"this keys is empty: {empty}")