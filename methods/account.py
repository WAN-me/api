from requests.models import Response
from methods import utils, db, users
import time
import json
import requests


def changepass(args):
    ss = utils.notempty(args, ['accesstoken', 'oldpass', 'newpass'])
    if ss == True:
        token = args['accesstoken']
        user = users._gett(token)
        if 'error' in user:
            return user
        oldpass = utils.dohash(f"{args['oldpass']}")
        newpass = utils.dohash(f"{args['newpass']}")
        token = utils.dohash(f'{time.time()}_{newpass}')
        result = db.exec(
            f'''select from users where password={oldpass} and token={token}''')
        if len(result) == 0:
            return utils.error(401, "password is incorrect")
        db.exec(
            f'''update users set token={token}, password={newpass} where password={oldpass} and token={token}''')
        return {"state": 'ok'}
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
        user = users._gett(token)
        if 'error' in user:
            return user
        if user[1] != 0:
            return utils.error(208, 'Already verifed')
        result = db.exec(
            f'''select code from users where token = ?''', (token,))
        code = result[0]
        print((result, code, args['code']))
        if code == args["code"]:
            return _verif(user, 1)
        else:
            return utils.error(401, "Incorrect verify code")
    else:
        return ss


def addsocial(args):
    ss = utils.notempty(args, ['accesstoken', 'social_token', 'social_name'])
    if ss == True:
        token = args['accesstoken']
        user = users._gett(token, 1)
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
