from sqlite3 import Error, connect
import hashlib,time

NEW_TBL_USERS = '''CREATE TABLE users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            token TEXT NOT NULL,
            email,
            password,
            online_state TEXT);
            '''

INIT_ADMIN='''insert into users (id,name,token)
        values (0,'admin','admin')'''


############################
###user
############################
def userget(args):
    ss = notempty(args,['accesstoken'])
    if ss == True: 
        token = args['accesstoken']
        user = (db(f'''select id,name,token,online_state from users where token = "{token}" '''))
        if not user or len(user)!=1:
            return error(2,"'accesstoken' is invalid")
        else:
            return {'id':user[0][0],'name':user[0][1],'token':user[0][2],'online_state':user[0][3]}
    else:
        return ss
def reg(args):
    ss = notempty(args,['name','email','password'])
    if ss == True:
        name = args['name']
        token = hashlib.sha256(f'{name}_{time.time()}'.encode()).hexdigest()
        password = hashlib.sha256(f"{args['password']}".encode()).hexdigest()
        db(f'''insert into users (name,token,email,password)
        values ('{name}','{token}','{args['email']}','{password}')''')
        return userget({'accesstoken':token})
    else: return ss


############################
###database
############################
def db(query):
    print(query)
    res = ""
    cn = connect('/databases/db.sqlite3')
    c=cn.cursor()
    c.execute(query)
    cn.commit()
    res = c.fetchall()
    c.close
    return res


def dropdatabase(yes:str):
    db('''DROP TABLE IF EXISTS users;''')
    db(NEW_TBL_USERS)
    db(INIT_ADMIN)
    return {'state':'done'}


############################
###utils
############################

def error(code,text):
    return {'error':{"code":code,"text":text}}


def notempty(args,need):
    print(args)
    empty=[]
    for key in need:
        name = args.get(key)
        if not name or name=='':
            empty.append(key)
    if len(empty)==0:
        return True
    else: return error(3,f"this keys is empty: {empty}")