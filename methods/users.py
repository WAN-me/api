from methods import utils,db
import time
def get(args):
    ss = utils.notempty(args,['accesstoken'])
    if ss == True: 
        token = args['accesstoken']
        id = args.get('id',0)
        thisuser = (db.exec(f'''select id,name,online_state,image from users where token = ? ''',(token,)))
        if not thisuser or len(thisuser)!=1:
            return utils.error(2,"'accesstoken' is invalid")
        else:
            thisuser = thisuser[0]
            if id == 0:
                return  {'id':thisuser[0],'name':thisuser[1],'online_state':thisuser[2]}
            user = (db.exec('''select id,name,online_state,image from users where id = :id ''',{'id':id}))
            if len(user) == 0:
                return utils.error(4,"this user not exists")
            else:
                user = user[0]
                return {'id':user[0],'name':user[1],'online_state':user[2],'image':user[3]}
    else:
        return ss

def auth(args):
    ss = utils.notempty(args,['login','password'])
    if ss == True: 
        #time.sleep(1)
        user = (db.exec(
            '''select id,token from users where email = :login and password = :pass''',
            {'login':args['login'],'pass':utils.dohash(args['password'])}))
        if not user or len(user)!=1:
            return utils.error(6,"login or password is incorrect")
        else:
            return {'id':user[0][0],'token':user[0][1]}
    else:
        return ss

def delete(args):
    db.exec('''DELETE FROM users
    WHERE token = ?;''',(
    args.get('accesstoken','null'),))
    return {'state':'ok'}

def reg(args):
    ss = utils.notempty(args,['name','email','password'])
    if ss == True:
        name = args['name']
        password = utils.dohash(f"{args['password']}")
        token = utils.dohash(f'{name}_{time.time()}_{password}')
        db.exec(f'''insert into users (name,token,email,password,image)
        values (:name,:token,:email,:password,:image)''',
        {'name': name,'token':token,'email':args['email'],'password':password,'image':args.get('image','default.png')})
        return get({'accesstoken':token})
    else: return ss
