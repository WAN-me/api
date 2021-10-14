from sqlite3 import Error, connect

############################
###user
############################
def db(query):
    res = ""
    c=connect('db.sqlite3').cursor()
    c.execute(query)
    res = c.fetchall()
    c.close
    return res

def userget(args):
    token = args.get('accesstoken')
    user = (db(f'''select * from users where token = "{token}" '''))
    if not token or token=="":#токена нет
        return {'error':{'code':1,'text':'\'accesstoken\' is empty'}}

    elif not user or len(user)!=1:
        return {'error':{"code":2,"text":"'accesstoken' is invalid"}}

    else:
        return {'id':user[0][0],'name':user[0][2],'token':user[0][1],}