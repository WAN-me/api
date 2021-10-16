from sqlite3 import Error, connect
import hashlib,time
############################
###user
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

def userget(args):
    token = args.get('accesstoken')
    user = (db(f'''select id,name,token from users where token = "{token}" '''))
    if not token or token=="":#токена нет
        return {'error':{'code':1,'text':'\'accesstoken\' is empty'}}

    elif not user or len(user)!=1:
        return {'error':{"code":2,"text":"'accesstoken' is invalid"}}

    else:
        return {'id':user[0][0],'name':user[0][1],'token':user[0][2],}

def reg(args):
    name = args.get('name')
    if not name or name=='':
        return {'error':{"code":3,"text":"'name' is empty"}}
    token = hashlib.sha256(f'{name}_{time.time()}'.encode()).hexdigest()
    print(db(f'''insert into users (name,token)
    values ('{name}','{token}')'''))
    return userget({'accesstoken':token})


############################
###database
############################
def dropdatabase(args):
    user = userget(args)
    print(user)
    if not 'error' in user:
        if user['id'] == 1:
            db('''DROP table users ''')
            db('''CREATE TABLE users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT NOT NULL,
            name TEXT NOT NULL);''')
            return {'state':'done'}
        else:
            return {'error':{"code":4,"text":"access denided for this method"}}
    else: return user

def dropdatabase(yes:str):
    db('''DROP table users ''')
    db('''CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token TEXT NOT NULL,
    name TEXT NOT NULL);''')
    return {'state':'done'}