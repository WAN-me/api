from tkinter.tix import Tree
import requests
import os
import time

def test(method,params={},msg='task'):
    result = (method(params))
    if 'error' in result:
        print(f"{RED}failed {msg}: {result['error']}{ENDC}")
    else: 
        print(f"{GREEN}ok {msg}{ENDC}")
    return result,'error' not in result

api_uri = "http://localhost:3000"
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
need = ['account','users',"messages",'groups','pool']
if __name__ == "__main__":
    os.system("fuser 3000/tcp -k >> /dev/null")
    os.system('rm db.sqlite3')
    os.system('python3 initdb.py &')
    os.system("python3 test_start.py >> api.log &")
    time.sleep(2)
    try:    

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

            # messages gethistory

            history1 = test(api.messages.gethistory,{
                'accesstoken': user1[0]['token'],
                'user_id': user2[0]['id']
            },'gethistory msg')
            
            ok.append(history1[1])

            for item in history1[0]['items']:
                if (item['from_id'] == msg1[0]['from_id'] and item['to_id'] == msg1[0]['to_id'] and item['text'] == msg1[0]['text']) or (item['from_id'] == msg2[0]['from_id'] and item['to_id'] == msg2[0]['to_id'] and item['text'] == msg2[0]['text']):
                    print(f"{GREEN}msg gethistory{ENDC}")
                    ok.append(True)
                else:
                    print(f"{GREEN}msg gethistory failed{ENDC}")
                    ok.append(False)

            # messages chats

            chats = test(api.messages.chats,{
                'accesstoken': user1[0]['token']
            },'chats')
            ok.append(chats[1])

            for item in chats[0]['items']:
                if (item['id'] == user2[0]['id'] and item['name'] == user2[0]['name']):
                    print(f"{GREEN}msg chats{ENDC}")
                    ok.append(True)
                else:
                    print(f"{GREEN}msg chats failed{ENDC}")
                    ok.append(False)
            
            # messages edit
            edit = test(api.messages.edit,{
                'accesstoken': user1[0]['token'],
                "text": msg1[0]['text']+'_edited',
                "id": message1[0]['id']},'msg edit')
            ok.append(edit[1])
            newmsg = test(api.messages.get,{
                'accesstoken': user1[0]['token'],
                "id": message1[0]['id']},'get edited msg')
            ok.append(newmsg[0]["text"] == msg1[0]['text']+'_edited')

            # messages del
            dell = test(api.messages.delete,{
                'accesstoken': user1[0]['token'],
                "id": message1[0]['id']},'del msg')
            ok.append(dell[1])
            print(f"messages - {GREEN}{ok.count(True)}{ENDC}/{RED}{ok.count(False)}{ENDC}")
        
        if 'groups' in need:
            ok = []

            # new group
            group = test(api.groups.new,{
                'accesstoken': user1[0]['token'],
                'name': 'test_group',
                "type":0
            },'new group')
            ok.append(group[1])
            group_id = group[0]['id']

            # join to group
            join = test(api.group.join,{
                'accesstoken': user2[0]['token'],
                'id': group_id
            }, 'join group')
            ok.append(join[1])
            
            # edit group
            edit = test(api.groups.edit,{
                'accesstoken': user1[0]['token'],
                'name': 'test_group2',
                'id': group_id
            }, 'get group')
            ok.append(edit[1])

            # get group
            group = test(api.groups.get,{
                'accesstoken': user2[0]['token'],
                'id': group_id
            }, 'get group')
            ok.append(len(group[0]['users']) == 2 and group[0]['name'] == "test_group2")

            leave = test(api.groups.leave,{         
                'accesstoken': user2[0]['token'],
                'id': group_id
            },'leave group')
            ok.append(leave[1])

            group = test(api.groups.getbyname,{
                'accesstoken': user1[0]['token'],
                'name': "test_group2"
            },'getbyname group')
            ok.append(group[0]['id'] == group_id and len(group[0]['users']) == 1)

            adduser = test(api.groups.adduser,{
                'accesstoken': user1[0]['token'],
                'id': group_id,
                "user_id": user2[0]['id']
            },'adduser group')

            addadmin = test(api.groups.addadmin,{
                'accesstoken': user1[0]['token'],
                'id': group_id,
                "user_id": user2[0]['id']
            },'addadmin group')

            result = test(api.groups.get,{
                'accesstoken': user2[0]['token'],
                'id': group_id
            }, 'get group')
            ok.append(len(result[0]['users']) == 2 and len(result[0]['admins']) == 1)

            dell = test(api.groups.dell,{
                'accesstoken': user1[0]['token'],
                'id': group_id
            }, 'del group')
            ok.append(dell[1])


            print(f"groups - {GREEN}{ok.count(True)}{ENDC}/{RED}{ok.count(False)}{ENDC}")

        if "pool" in need:
            ok = []
            get = test(api.pool.get, {
                "accesstoken": user1[0]['token']
            },'get pool')
            ok.append(get[1] and get[0]['count'] == 2)

            read = test(api.pool.read, {
                "accesstoken": user1[0]['token']
            },'read pool')
            ok.append(read[1])

            get = test(api.pool.get, {
                "accesstoken": user1[0]['token']
            },'get pool')
            ok.append(get[1] and get[0]['count'] == 0)

            print(f"pool - {GREEN}{ok.count(True)}{ENDC}/{RED}{ok.count(False)}{ENDC}")
    except Exception as e:
        raise e




    print(f"{BLUE}tests ended{ENDC}")
    os.system("fuser 3000/tcp -k >> /dev/null")
    os.remove('db.sqlite3')