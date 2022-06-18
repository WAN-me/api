from methods import utils, db, mail
from methods.utils import TOKENR, secure
from methods.users import get, _get
from callback import send
import time
import json
import requests
import cfg
import re

def _overdue_token(user_id):
    db.exec('''update auth set expire_in = strftime('%s', 'now') where user_id == ?;''', (user_id,))


def auth(args):
    type = args.get('type', 'pass')
    if type == 'pass':
        ss = utils.notempty(args, ['email', 'password'])
        if ss == True:
            time.sleep(1.5)
            user = db.exec(
            '''select id from users where email = :email and password = :pass''', {
                'email': args['email'], 'pass': utils.dohash(args['password'])})


            if not user or len(user) == 0:
                return utils.error(401, "Login or password is incorrect")

            device = args.get('ip', 'unknown')
            token = utils.dohash(f"{args['password']}_{device}_{time.time_ns()}")
            db.exec(
            '''insert into auth (user_id, device, token) values(:user_id, :device, :token)''', {
                'user_id': user[0][0], 'device': device, 'token': token})
            
            res = get({'accesstoken':token})
            res['token'] = token
            return res
        else:
            return ss


    elif type == 'vk':
        ss = utils.notempty(args, ['token'])
        if ss == True:
            token = args['token']
            if utils.validr(token, TOKENR):
                response = json.loads(requests.get(
                    f"https://api.vk.com/method/users.get?access_token={token}&v=5.101").content)
                if 'response' in response:
                    user = response['response'][0]

                    
                    user_id = db.exec(
                        f'''select (user) from accounts where ac_id = {user['id']}''')

                    if len(user_id) < 1:
                        return utils.error(
                            401, "Access denided for this account")

                    
                    user = db.exec(
                        '''select id,token from users where id = :id''',
                        {'id': user_id[0]})

                    return {'id': user[0][0], 'token': user[0][1]}
                return utils.error(
                    400, f'Error while get data from token: {response}')
            return utils.error(400, "'token' is invalid")
        else:
            return ss
    else:
        return utils.error(400, "'type' is invalid")


def delete(args):
    ss = utils.notempty(args, ['accesstoken'])
    if ss == True:
        token = args['accesstoken']
        user = _gett(token)
        if 'error' in user:
            return user
        db.exec('''DELETE FROM users
            WHERE id = ?;''', (user[0],))
        send(args['ip'], 'user_del', args)
        return {'state': 'ok'}
    else:
        return ss


def _sendcode(code, args):
    send(args['ip'], 'send_code', args)
    response = requests.get(
        'http://rd.wan-group.ru:3555/method/utils.capcha', {
            'data': code, 'file': utils.dohash(
                args['email'] + f"{time.time_ns()}")}).json()
    url = "http://rd.wan-group.ru"
    if 'error' in response:
        response = requests.get(
            'http://wan-group.ru:3555/method/utils.capcha', {
                'data': code, 'file': utils.dohash(
                    args['email'] + f"{time.time_ns()}")}).json()
        url = "http://wan-group.ru"
    if 'error' in response:
        return utils.error(
            500, 'failed to generate captcha. Try again or contact as')
    else:
        url = url + f"/capcha/{response['file']}.png"
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
        send_status = mail.send(args['email'], cont)
        if send_status:
            return {"advanced": 'Please check you mailbox'}
        else:
            return {"advanced": 'Failed to send mail'}


def reg(args):
    ss = utils.notempty(args, ['name', 'email', 'password'])
    if ss == True:
        name = args['name']
        email = str(args['email']).strip()
        
        if len(re.findall(r'[a-z0-9]+@[a-z]+\.[a-z]{2,3}',email)) > 0:
            password = utils.dohash(f"{args['password']}")
            
            if len(db.exec('''select email from users where email=:email''', {'email': email})) < 1:
                token = utils.dohash(f'{name}_{time.time()}_{password}')
                invite_hash = args.get('invitation','')
                device = args.get('ip', 'unknown')

                
                res = db.exec('''select invite_hash, user_id from invites where invite_hash=:invite_hash''', {'invite_hash': invite_hash}) # manage invite
                if invite_hash == cfg.eternal_invite:
                    res = [[0,-1],]
                if len(res) > 0:
                    if args.get('secret','SecretKeyForReg') == cfg.SecretKeyForReg:

                        db.exec(f'''insert into users (name, email, password, image, verifi, invited_by)
                        values (:name, :email, :password, :image, :verifi, :invited_by)''',
                                {'name': secure(name),
                                'email': email,
                                'verifi': 3,
                                'invited_by': res[0][1],
                                'password': password,
                                'image': args.get('image','default.png')})
                        
                        sc = "verifi level set on 3(maximum)"

                    else:
                        code = utils.random_string(6)
                        db.exec(f'''insert into users (name, email, password, image, code, invited_by)
                        values (:name, :email, :password, :image, :code, :invited_by)''',
                                {'name': secure(name),
                                'email': email,
                                'code': code,
                                'invited_by': res[0][1],
                                'password': password,
                                'image': args.get('image','default.png')})
                        sc = _sendcode(code, args)
                    db.exec(f'''delete from invites where invite_hash=:invite_hash''', {'invite_hash': invite_hash})

                else:
                    return utils.error(400, 'Incorrect invitation')
                user = auth(args)
                user['advanced'] = sc
                send(args['ip'], 'user_reg', args)
                return user
            else:
                return utils.error(400, 'Email already used')
        else: return utils.error(400, 'Invalid email')
    else:
        return ss


def _gett(token, needVerif=0):
    "аовзвращает список (id, verif, expire_in)"
    
    user = db.exec(f'''select id, verifi, expire_in from users, auth where id == auth.user_id and token = ?;''', (token,))
    
    if not user or len(user) != 1:
        return utils.error(400, "'accesstoken' is invalid")
    elif user[0][1] < needVerif:
        return utils.error(403, "You need to confirm your email")
    elif user[0][2] < time.time():
        return utils.error(401, "The token is expired")
    else:
        return user[0]


def changepass(args):
    ss = utils.notempty(args, ['accesstoken', 'oldpass', 'newpass'])
    if ss == True:
        oldtoken = args['accesstoken']
        user = _gett(oldtoken)
        if 'error' in user:
            return user
        oldpass = utils.dohash(f"{args['oldpass']}")
        newpass = utils.dohash(f"{args['newpass']}")
        result = db.exec('''select id, verifi from users, auth where users.password = :pass and users.id == auth.user_id and auth.token = :token''', {
                        'token': oldtoken, 'pass': oldpass})
        if len(result) == 0:
            return utils.error(401, "password is incorrect")
        token = utils.dohash(f'{time.time()}_{newpass}')
        db.exec(
            f'''update users set password = :newpass where id = :id''', {
                        'token': token, 'newpass': newpass, 'id': user[0]})
        _overdue_token(user[0])
        db.exec(
            f'''insert into auth (user_id, token, device) values(:user_id, :token, :device)''', {
                        'token': token, 'user_id': user[0], 'device': args.get('ip', 'unknown'),})
        return {"token": token}
    else:
        return ss


def _verif(id, level):
    try:
        db.exec(f'''update users set verifi = {level} where id={id}''')
        return {'state': 'ok'}
    except Exception as ex:
        return utils.error(500, ex)


def verif(args):
    ss = utils.notempty(args, ['accesstoken', 'code'])
    if ss == True:
        token = args['accesstoken']
        user = _gett(token)
        if 'error' in user:
            return user
        if user[1] != 0:
            return utils.error(208, 'Already verifed')
        result = db.exec(f'''select code from users where token = ?''', (token,))
            
        code = result[0]
        if code == args["code"]:
            return _verif(user, 1)
        else:
            return utils.error(401, "Incorrect verify code")
    else:
        return ss


def edit(args):
    ss = utils.notempty(args, ['accesstoken'])
    if ss == True:
        token = args['accesstoken']
        user = _gett(token, 1)
        if 'error' in user:
            return user
        user = _get(user[0])
        if 'error' in user:
            return user
        name = args.get("name", user['name'])
        image = args.get("image", user['image'])
        db.exec('''UPDATE users
            SET name = :name,
            image = :image
            WHERE id = :id''',

                {
                    'id': user['id'],
                    'name': name,
                    'image': image,
                }
                )
        return {'state': 'ok'}
    else:
        return ss


def invite(args):
    ss = utils.notempty(args, ['accesstoken'])
    if ss == True:
        token = args['accesstoken']
        user = _gett(token, 1)
        if 'error' in user:
            return user
        hash = utils.dohash(f'{str(user)}_{time.time_ns()}', 10)
        db.exec(f'''insert into invites (user_id, invite_hash)
                    values (:user_id, :invite_hash)''',
                            {'user_id': user[0],
                            'invite_hash': hash})
        return {'hash': hash}
    else:
        return ss
        

def addsocial(args):
    ss = utils.notempty(args, ['accesstoken', 'social_token', 'social_name'])
    if ss == True:
        token = args['accesstoken']
        user = _gett(token, 1)
        if 'error' in user:
            return user
        social_name = str(args['social_name']).lower()
        social_token = args['social_token']
        if social_name == 'vk':
            response = json.loads(requests.get(
                f"https://api.vk.com/method/users.get?access_token={social_token}&v=5.101").content)
            if 'response' in response:
                user = response['response'][0]
                db.exec(
                    f'''inert into accounts (user, ac_token, ac_id, ac_email, social_name)
                    values ({user[0]},"{social_token}",{user['id']},"{user.get('email','none@wan-group.ru')}","{user['first_name']} {user['last_name']}")''')
                return {'state': "ok"}
            return utils.error(
                400, f'Error while get data from token: "{response}"')
        return utils.error(400, 'Unknown social_name')
    else:
        return ss
