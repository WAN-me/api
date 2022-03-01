from crypt import methods
import json
import random

import requests
from methods import utils,db,mail
from methods.utils import TOKENR, error, secure
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
    user = (db.exec('''select id,name,online_state,image,verifi from users where id = :id ''',{'id':id}))
    if len(user) == 0:
        return utils.error(404,"this user not exists")
    else:
        user = user[0]
        return {'id':user[0],'name':secure(user[1]),'online_state':user[2],'image':user[3],'verifi':user[4]}

def _gett(token,needVerif=0):
    thisuser = (db.exec(f'''select id, verifi from users where token = ? ''',(token,)))
    if not thisuser or len(thisuser)!=1:
        return utils.error(400,"'accesstoken' is invalid")
    elif thisuser[0][1]<needVerif:
        return utils.error(403,"You need to confirm your email")
    else:
        return thisuser[0]
def auth(args):
    type = args.get('type','pass')
    if type == 'pass':
        ss = utils.notempty(args,['login','password'])
        if ss == True: 
            #time.sleep(1)
            user = (db.exec(
                '''select id,token from users where email = :login and password = :pass''',
                {'login':args['login'],'pass':utils.dohash(args['password'])}))
            if not user or len(user)==0:
                return utils.error(401,"login or password is incorrect")
            else:
                return {'id':user[0][0],'token':user[0][1]}
        else:
            return ss
    elif type == 'vk':
        ss = utils.notempty(args,['token'])
        if ss == True:
            token = args['token'] 
            if utils.validr(token,TOKENR):
                resp = json.loads(requests.get(f"https://api.vk.com/method/users.get?access_token={token}&v=5.101").content)
                if 'response' in resp:
                    user = resp['response'][0]
                    ex = db.exec(f'''select (user) from accounts where ac_id = {user['id']}''')
                    if len(ex) < 1:
                        return utils.error(401, "access denided for this account")
                    user = (db.exec(
                '''select id,token from users where id = :id''',
                {'id':ex[0]}))
                    return {'id':user[0][0],'token':user[0][1]}
                return utils.error(400,f'error while get data from token: {resp}')
            return utils.error(400,"'token' is invalid")
        else:
            return ss
    else: return utils.error(400,"'type' is invalid")

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

def _sendcode(code,args):
    res = requests.get('http://rd.wan-group.ru:3555/method/utils.capcha',{'data':code,'file':utils.dohash(args['email'])}).json()
    url = "http://rd.wan-group.ru"
    if 'error' in res:
        res = requests.get('http://wan-group.ru:3555/method/utils.capcha',{'data':code,'file':utils.dohash(args['email'])}).json()
        url = "http://wan-group.ru"
    if 'error' in res:
        return utils.error(500,'failed to generate captcha. Try again or contact as')
    else:
        url = url+f"/capcha/{res['file']}.png"
        cont = f"""\
                    <html>
                        <head></head>
                        <body>
                            <h1>Регистрация в WAN Group</h1>
                            <p>Привет! Спасибо за регистрацию в наших сервисах. Используйте код с картинки для продолжения регистрации</p>
                            <img src="{url}" >
                        </body>
                    </html>
                """
        sent = mail.send(args['email'],cont)
        if sent == True:
            return {"advanced": 'please check you mailbox'}
        elif sent == False:
            return {"advanced": 'Failed to send mail'}



def reg(args):
    ss = utils.notempty(args,['name','email','password'])
    if ss == True:
        name = args['name']
        password = utils.dohash(f"{args['password']}")
        token = utils.dohash(f'{name}_{time.time()}_{password}')
        code = str(random.randint(100000,99999999))
        db.exec(f'''insert into users (name,token,email,password,image,code)
        values (:name,:token,:email,:password,:image,:code)''',
        {'name': secure(name),'token':token,'email':args['email'],'code':code,'password':password,'image':args.get('image','default.png')})
        sc = _sendcode(code,args)
        user = get({'accesstoken':token})
        user['advanced'] = sc['advanced']
        return user
    else: return ss
