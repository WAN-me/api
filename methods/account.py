from methods import utils, db, mail
from methods.utils import TOKENR, secure
from methods.users import get
import time
import json
import requests
import cfg


def auth(args):
    type = args.get('type', 'pass')
    if type == 'pass':
        ss = utils.notempty(args, ['email', 'password'])
        if ss == True:
            # time.sleep(1)
            args['cursor'].execute(
            '''select id,token from users where email = :email and password = :pass''', {
                'email': args['email'], 'pass': utils.dohash(
                    args['password'])})
            user = args['cursor'].fetchall()
            if not user or len(user) == 0:
                return utils.error(401, "Login or password is incorrect")
            else:
                return {'id': user[0][0], 'token': user[0][1]}
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

                    args['cursor'].execute(
                        f'''select (user) from accounts where ac_id = {user['id']}''')
                    user_id = args['cursor'].fetchall()

                    if len(user_id) < 1:
                        return utils.error(
                            401, "Access denided for this account")

                    args['cursor'].execute(
                        '''select id,token from users where id = :id''',
                        {'id': user_id[0]})
                    user = args['cursor'].fetchall()

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
        user = _gett(token, cursor=args['cursor'])
        if 'error' in user:
            return user
        args['cursor'].execute('''DELETE FROM users
            WHERE token = ?;''', (token,))
        args['connection'].commit()
        return {'state': 'ok'}
    else:
        return ss


def _sendcode(code, args):
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
        password = utils.dohash(f"{args['password']}")
        token = utils.dohash(f'{name}_{time.time()}_{password}')
        if args.get('secret','SecretKeyForReg') == cfg.SecretKeyForReg:
            args['cursor'].execute(f'''insert into users (name, token, email, password, image, verifi)
            values (:name, :token, :email, :password, :image, :verifi)''',
                    {'name': secure(name),
                    'token': token,
                    'email': args['email'],
                    'verifi': 3,
                    'password': password,
                    'image': args.get('image','default.png')})
            sc = "verifi level set on 3(maximum)"
        else:
            code = utils.random_string(6)
            args['cursor'].execute(f'''insert into users (name, token, email, password, image, code)
            values (:name, :token, :email, :password, :image, :code)''',
                    {'name': secure(name),
                    'token': token,
                    'email': args['email'],
                    'code': code,
                    'password': password,
                    'image': args.get('image','default.png')})
            sc = _sendcode(code, args)
        args['connection'].commit()
        user = get({'accesstoken': token, 'cursor': args['cursor']})
        user['advanced'] = sc
        user['token'] = token
        return user
    else:
        return ss


def _gett(token, needVerif=0,cursor=None):
    cursor.execute(f'''select id, verifi from users where token = ? ''', (token,))
    user = cursor.fetchall()
    if not user or len(user) != 1:
        return utils.error(400, "'accesstoken' is invalid")
    elif user[0][1] < needVerif:
        return utils.error(403, "You need to confirm your email")
    else:
        return user[0]


def changepass(args):
    ss = utils.notempty(args, ['accesstoken', 'oldpass', 'newpass'])
    if ss == True:
        oldtoken = args['accesstoken']
        user = _gett(oldtoken,cursor=args['cursor'])
        if 'error' in user:
            return user
        oldpass = utils.dohash(f"{args['oldpass']}")
        newpass = utils.dohash(f"{args['newpass']}")
        args['cursor'].execute('''select id, verifi from users where token = :token and password = :pass''', {
                        'token': oldtoken, 'pass': oldpass})
        result = args['cursor'].fetchall()
        if len(result) == 0:
            return utils.error(401, "password is incorrect")
        token = utils.dohash(f'{time.time()}_{newpass}')
        args['cursor'].execute(
            f'''update users set token = :token, password = :newpass where token = :oldtoken''', {
                        'token': token, 'newpass': newpass, 'oldtoken': oldtoken})
        args['connection'].commit()
        return {"token": token}
    else:
        return ss


def _verif(id, level,args):
    try:
        args['cursor'].execute(f'''update users set verifi = {level} where id={id}''')
        args['connection'].commit()
        return {'state': 'ok'}
    except Exception as ex:
        return utils.error(500, ex)


def verif(args):
    ss = utils.notempty(args, ['accesstoken', 'code'])
    if ss == True:
        token = args['accesstoken']
        user = _gett(token, cursor=args['cursor'])
        if 'error' in user:
            return user
        if user[1] != 0:
            return utils.error(208, 'Already verifed')
        args['cursor'].execute(f'''select code from users where token = ?''', (token,))
        result = args['cursor'].fetchall()
            
        code = result[0]
        if code == args["code"]:
            return _verif(user, 1,args)
        else:
            return utils.error(401, "Incorrect verify code")
    else:
        return ss


def addsocial(args):
    ss = utils.notempty(args, ['accesstoken', 'social_token', 'social_name'])
    if ss == True:
        token = args['accesstoken']
        user = _gett(token, 1,args['cursor'])
        if 'error' in user:
            return user
        social_name = str(args['social_name']).lower()
        social_token = args['social_token']
        if social_name == 'vk':
            response = json.loads(requests.get(
                f"https://api.vk.com/method/users.get?access_token={social_token}&v=5.101").content)
            if 'response' in response:
                user = response['response'][0]
                args['cursor'].execute(
                    f'''inert into accounts (user, ac_token, ac_id, ac_email, social_name)
                    values ({user[0]},"{social_token}",{user['id']},"{user.get('email','none@wan-group.ru')}","{user['first_name']} {user['last_name']}")''')
                args['connection'].commit()
                return {'state': "ok"}
            return utils.error(
                400, f'Error while get data from token: "{response}"')
        return utils.error(400, 'Unknown social_name')
    else:
        return ss
