from api import api,methods
from api.methods import db as db
from flask import request
import time,hashlib

@api.route('/dropdb', methods=['GET',"POST"])
def dropdb():
    user = methods.userget(request.args)
    print(user)
    if not 'error' in user:
        if user['id'] == 1:
            return str(db('''drop * from users '''))
        else:
            return {'error':{"code":4,"text":"access denided for this method"}}
    else: return user
@api.route('/', methods=['GET',"POST"])
def m():
    return {'message':'welcome to the WAN-m api!'}
@api.route('/index', methods=['GET',"POST"])
def index():
    return "You in index"
@api.route('/user', methods=['GET',"POST"])
def user():
    return methods.userget(request.args)
@api.route('/reg', methods=['GET',"POST"])
def register():
    c = db.create_connection('db.sqlite3')
    args = request.args
    name = args.get('name')
    if not name or name=='':
        return {'error':{"code":3,"text":"'name' is empty"}}
    token = hashlib.sha256(f'{name}_{time.time_ns}'.encode()).hexdigest()
    db.execute_query(c,
    f'''insert into users (name,token)
    values ('{name}','{token}')''')
    user = (db.execute_read_query(c,f'''select * from users where token = "{token}" '''))
    return {'id':user[0][0],'name':user[0][2],'token':user[0][1],}