from requests.models import Response
from methods import utils,db,users
import time,json,requests
def changepass(args):
    ss = utils.notempty(args,['accesstoken','oldpass','newpass'])
    if ss == True: 
        atoken = args['accesstoken']
        res = users._gett(atoken)
        if 'error' in res:
            return res 
        oldpass = utils.dohash(f"{args['oldpass']}")
        newpass = utils.dohash(f"{args['newpass']}")
        token = utils.dohash(f'{time.time()}_{newpass}')
        userss = db.exec('''select from users where password={oldpass} and token={atoken}''')
        if not len(userss)==1:
            return utils.error(401,"password is incorrect")
        db.exec(f'''update users set token={token},password={newpass} where password={oldpass} and token={atoken}''')
        return {"state":'ok'}
    else:
        return ss

def addsocial(args):
    ss = utils.notempty(args,['accesstoken','social_token','social_name'])
    if ss == True: 
        atoken = args['accesstoken']
        res = users._gett(atoken)
        if 'error' in res:
            return res 
        sname = str(args['social_name']).lower()
        stoken = args['social_token']
        if sname == 'vk':
            resp = json.loads(requests.get(f"https://api.vk.com/method/users.get?access_token={stoken}&v=5.101").content)
            if 'response' in resp:
                user = resp['response'][0]
                db.exec(f'''inert into accounts (user,ac_token,ac_id,ac_email,social_name)
                    values ({res[0]},"{stoken}",{user['id']},"{user.get('email','none@wan-group.ru')}","{user['first_name']} {user['last_name']}")''')
                return {'state':"ok"}
            return utils.error(400,f'error while get data from token: {resp}')
        return utils.error(400,'unknown social_name')
    else:
        return ss