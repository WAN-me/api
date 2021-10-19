from os import error
from sqlite3 import Error, connect
import hashlib,time

class users():
    def get(args):
        ss = utils.notempty(args,['accesstoken'])
        if ss == True: 
            token = args['accesstoken']
            id = args.get('id',0)
            thisuser = (db.exec(f'''select id,name,online_state from users where token = ? ''',(token,)))
            if not thisuser or len(thisuser)!=1:
                return utils.error(2,"'accesstoken' is invalid")
            else:
                thisuser = thisuser[0]
                if id == 0:
                    return  {'id':thisuser[0],'name':thisuser[1],'online_state':thisuser[2]}
                user = (db.exec('''select id,name,online_state from users where id = :id ''',{'id':id}))
                if len(user) == 0:
                    return utils.error(4,"this user not exists")
                else:
                    user = user[0]
                    return {'id':user[0],'name':user[1],'online_state':user[2]}
        else:
            return ss

    def auth(args):
        ss = utils.notempty(args,['login','password'])
        if ss == True: 
            time.sleep(1)
            user = (db.exec(
                '''select id,token from users where email = :login and password = :pass''',
                {'login':args['login'],'pass':utils.dohash(args['password'])}))
            if not user or len(user)!=1:
                return utils.error(6,"login or password is incorrect")
            else:
                return {'id':user[0][0],'token':user[0][1]}
        else:
            return ss

    def reg(args):
        ss = utils.notempty(args,['name','email','password'])
        if ss == True:
            name = args['name']
            password = utils.dohash(f"{args['password']}")
            token = utils.dohash(f'{name}_{time.time()}_{password}')
            db.exec(f'''insert into users (name,token,email,password)
            values (:name,:token,:email,:password)''',
            {'name': name,'token':token,'email':args['email'],'password':password})
            return users.get({'accesstoken':token})
        else: return ss

class messages():
    def send(args):
        ss = utils.notempty(args,['accesstoken','text','to_id'])
        if ss == True: 
            token = args['accesstoken']
            text = args['text']
            toId = args['to_id']
            thisuser = (db.exec(f'''select id from users where token = ? ''',(token,)))
            if not thisuser or len(thisuser)!=1:
                return utils.error(2,"'accesstoken' is invalid")
            else:
                thisuser = thisuser[0]
                db.exec('''insert into messages (from_id,to_id,text)
                values (?,?,?)''',(thisuser[0],toId,text,))
                return {'state':'ok'}
        else:
            return ss

    def get(args):
        ss = utils.notempty(args,['accesstoken','id'])
        if ss == True: 
            token = args['accesstoken']
            id = args['id']
            thisuser = (db.exec(f'''select id from users where token = ? ''',(token,)))
            if not thisuser or len(thisuser)!=1:
                return utils.error(2,"'accesstoken' is invalid")
            else:
                thisuserid = thisuser[0][0]
                msg = db.exec('''select from_id,text,to_id from messages where id = ?''',(id,))
                if not msg or len(msg)!=1:
                    return utils.error(2,"'id' is invalid")
                msg = msg[0]
                if msg[0] != thisuserid and msg[2] != thisuserid:
                    return utils.error(7,'access denided for this action')
                return {'from_id':msg[0],'to_id':msg[2],'text':msg[1]}
        else:
            return ss


class utils():

    def dohash(input):
        return hashlib.sha256(input.encode()).hexdigest()

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
        db.exec('''DROP TABLE IF EXISTS messages;''')
        db.exec(db.NEW_TBL_MESSAGES)
        return {'state':'done'}


