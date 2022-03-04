from tkinter.tix import Tree
import requests
import os
import time

def test(method,params={},msg='task'):
    result = (method(
        params))
    if 'error' in result:
        print(f"{RED}failed {msg}: {result['error']}{ENDC}")
    else: 
        print(f"{GREEN}ok {msg}{ENDC}")
    return result,'error' not in result

os.system("python3 test_start.py >> api.log &")

api_uri = "http://localhost:3000"
time.sleep(2)
class Api(object):
    __slots__ = ('_method')

    def __init__(self, method=None):
        self._method = method

    def __getattr__(self, method):
        return Api(
            (self._method + '.' if self._method else '') + method
        )

    def __call__(self, params={},**kwargs):
        for k, v in kwargs.items():
            if isinstance(v, (list, tuple)):
                kwargs[k] = ','.join(str(x) for x in v)
        result = requests.post(api_uri+"/method/"+str(self._method), data = kwargs | params)
        try:
            return result.json()
        except:
            return result.text


BLUE="\033[94m"
GREEN= "\033[92m"
RED= "\033[91m"
ENDC= "\033[0m"

api = Api()
['account.reg','account.auth','account.changepass','account.del',
'users.get',
'messages.send','messages.get']
need = ['account','users',"messages"]
if __name__ == "__main__":

    # start account test
    if 'account' in need:
        ok = []
        # account reg
        user = test(api.account.reg,{
                'name': 'test_user',
                'email': 'email',
                'password': 'password'
                },"reg user")
        ok.append(user[1])

        # account auth
        user = test(api.account.auth,{
                'email': 'email',
                'password': 'password'
                },"auth user")
        ok.append(user[1])
        token = user[0]['token']


        # account changepass
        user = test(api.account.changepass, {
                'oldpass': 'password',
                'newpass': 'password1',
                'accesstoken': token
                },"changepass user")
        ok.append(user[1])
        token = user[0]['token']

        # account del
        user = test(api.account.delete,{
                'accesstoken': token
                },"del user")
        ok.append(user[1])
        print(f"account - {GREEN}{ok.count(True)}{ENDC}/{RED}{ok.count(False)}{ENDC}")

    # start account test
    if 'users' in need:
        ok = []
        # tmp reg
        user1 = test(api.account.reg,{
                'name': 'tmp',
                'email': 'email',
                'password': 'password'
                },"reg tmp user")
        ok.append(user1[1])
        # tmp2 reg
        user2 = test(api.account.reg,{
                'name': 'tmp2',
                'email': 'email2',
                'password': 'password'
                },"reg 2 tmp user")
        ok.append(user2[1])
        # users get
        getuser = test(api.users.get,{
                'accesstoken': user1[0]['token'],
                'id': user2[0]['id']
                },"get user")
        if not getuser[0]['name'] == "tmp2":
            ok.append(False)
            print(f"{RED}no right user getted{ENDC}")
        else:
            ok.append(getuser[1])
        print(f"users - {GREEN}{ok.count(True)}{ENDC}/{RED}{ok.count(False)}{ENDC}")

    if 'messages' in need:
        ok = []
        # messages send
        message1 = test(api.messages.send,{
                'accesstoken': user1[0]['token'],
                'to_id': user2[0]['id'],
                "text":"test_msg"
                },"send user1->user2")
        ok.append(message1[1])
        # messages send2
        message2 = test(api.messages.send,{
                'accesstoken': user2[0]['token'],
                'to_id': user1[0]['id'],
                "text":"test_msg2"
                },"send user2->user1")
        ok.append(message2[1])
        # messages get
        msg1 = test(api.messages.get,{
            'accesstoken': user1[0]['token'],
            'id': message1[0]['id']},"get msg1")

        if not msg1[0]['text'] == "test_msg":
            ok.append(False)
            print(f"{RED}no right msg getted{ENDC}")
        else:
            ok.append(msg1[1])

        msg2 = test(api.messages.get,{
            'accesstoken': user1[0]['token'],
            'id': message2[0]['id']},"get msg2")

        if not msg2[0]['text'] == "test_msg2":
            ok.append(False)
            print(f"{RED}no right msg getted{ENDC}")
        else:
            ok.append(msg2[1])

        history1 = test(api.messages.gethistory,{
            'accesstoken': user1[0]['token'],
            'user_id': user2[0]['id']
        })
        print(msg2)
        print(history1[0]['items'])

        print(f"messages - {GREEN}{ok.count(True)}{ENDC}/{RED}{ok.count(False)}{ENDC}")





    print(f"{BLUE}tests ended{ENDC}")
    os.system("fuser 3000/tcp -k >> /dev/null")