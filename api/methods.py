from sqlite3 import Error, connect
import hashlib,time

class users():
    def get(args):
        ss = utils.notempty(args,['accesstoken'])
        if ss == True: 
            token = args['accesstoken']
            user = (db.exec(f'''select id,name,token,online_state from users where token = %s ''',token))
            if not user or len(user)!=1:
                return utils.error(2,"'accesstoken' is invalid")
            else:
                return {'id':user[0][0],'name':user[0][1],'token':user[0][2],'online_state':user[0][3]}
        else:
            return ss

    def reg(args):
        ss = utils.notempty(args,['name','email','password'])
        if ss == True:
            name = args['name']
            password = hashlib.sha256(f"{args['password']}".encode()).hexdigest()
            token = hashlib.sha256(f'{name}_{time.time()}_{password}'.encode()).hexdigest()
            db.exec(f'''insert into users (name,token,email,password)
            values (%(name)s,%(token)s,%(email)s,%(password)s)''',
            {'name': name,'token':token,'email':args['email'],'password':password})
            return users.get({'accesstoken':token})
        else: return ss

class utils():
    def notempty(args,need):
        print(args)
        empty=[]
        for key in need:
            name = args.get(key)
            if not name or name=='':
                empty.append(key)
        if len(empty)==0:
            return True
        else: return utils.error(3,f"this keys is empty: {empty}")


    def error(code,text):
        return {'error':{"code":code,"text":text}}

class db():

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

    def drop(yes:str):
        db.exec('''DROP TABLE IF EXISTS users;''')
        db.exec(db.NEW_TBL_USERS)
        db.exec(db.INIT_ADMIN)
        return {'state':'done'}


