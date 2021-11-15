from methods import utils,db
import time
def get(args):
    ss = utils.notempty(args,['accesstoken'])
    if ss == True: 
        token = args['accesstoken']
        res = _gett(token)
        id = args.get('id',res[0])
        return res if 'error' in res else _get(id)

    else:
        return ss

def _get(id):
    user = (db.exec('''select id,name,online_state,image from users where id = :id ''',{'id':id}))
    if len(user) == 0:
        return utils.error(404,"this user not exists")
    else:
        user = user[0]
        return {'id':user[0],'name':user[1],'online_state':user[2],'image':user[3]}

def _gett(token):
    thisuser = (db.exec(f'''select id from users where token = ? ''',(token,)))
    if not thisuser or len(thisuser)!=1:
        return utils.error(400,"'accesstoken' is invalid")
    else:
        return thisuser[0]
def auth(args):
    ss = utils.notempty(args,['login','password'])
    if ss == True: 
        #time.sleep(1)
        user = (db.exec(
            '''select id,token from users where email = :login and password = :pass''',
            {'login':args['login'],'pass':utils.dohash(args['password'])}))
        if not user or len(user)!=1:
            return utils.error(401,"login or password is incorrect")
        else:
            return {'id':user[0][0],'token':user[0][1]}
    else:
        return ss

def delete(args):
    ss = utils.notempty(args,['accesstoken'])
    if ss == True: 
        token = args['accesstoken']
        thisuser = _gett(token)
        if 'error' in thisuser:
            return thisuser 
        db.exec('''DELETE FROM users
            WHERE token = ?;''',(
            token,))
        return {'state':'ok'}
    else:
        return ss

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
