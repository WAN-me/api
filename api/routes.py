import os,json

import requests
from api import api
import methods.messages
import methods.utils
import methods.users
import methods.pool
import methods.chats
import methods.bugs
import methods.groups
import methods.kino
import methods.vul
import methods.account
import methods.achive
from flask import request,redirect
from werkzeug import utils as uti

@api.errorhandler(404)
def pageNotFound(error):
    return methods.utils.error(404,'Page not found'),404
@api.errorhandler(500)
def ISE(error):
    return methods.utils.error(500,'internal server error'),500
@api.route('/favicon.ico')
def favicon():
    return redirect("https://wan-group.ru/favicon.svg", code=302)
@api.route('/index', methods=['GET',"POST"])
def index():
    return "You in index"
@api.route('/webpwnchat', methods=['GET',"POST"])
def webpwn():
    return "ООО, да вы программист на html"

@api.route('/kino/<method>/<params>', methods=['GET',"POST"])
def uu1(method,params):
    print(method+"/"+params)
    return methods.kino.universal(request.args.to_dict(),method+"/"+params)

@api.route('/kino/<method>/', methods=['GET',"POST"])
def uu2(method):
    print(method+"/")
    return methods.kino.universal(request.args.to_dict(),method+"/")

@api.route('/kino/<method>', methods=['GET',"POST"])
def uu3(method):
    print(method)
    return methods.kino.universal(request.args.to_dict(),method)

@api.route('/cloud', methods=['GET',"POST"])
def upload():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        print(dir(file1))
        path = os.path.join(api.config['UPLOAD_FOLDER'], uti.secure_filename(file1.filename))
        file1.save(path)
        return redirect("https://cloud.wan-group.ru/upload/"+path.split('/var/www/cloud/upload/',1)[1], code=301)
    return '''
    <h1>Upload new File</h1>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file1">
      <input type="submit">
    </form>
    '''
@api.route('/auth', methods=['GET',"POST"])
def auth():
    args = request.args.to_dict()
    if "code" in args:
        code = args['code']
        r = json.loads(requests.get('https://oauth.vk.com/access_token?client_id=8012324&client_secret=COH80Oy3E72Nhj7ChB7L&redirect_uri=http://test.api.wan-group.ru/auth&code='+code).content)
        user = json.loads(requests.get(f"https://api.vk.com/method/users.get?access_token={r['access_token']}&v=5.101").content)['response'][0]
        return f"Привет, {user['first_name']} {user['last_name']}\n{r['email']} - Это твоя почта?"
    else:
        return redirect("https://oauth.vk.com/authorize?client_id=8012324&display=page&redirect_uri=http://test.api.wan-group.ru/auth&scope=email&response_type=code&v=5.131", code=302)
@api.route('/method/<method>/<submethod>', methods=['GET',"POST"])
@api.route('/method/<method>/<submethod>/', methods=['GET',"POST"])
@api.route('/method/<method>.<submethod>', methods=['GET',"POST"])
@api.route('/method/<method>.<submethod>/', methods=['GET',"POST"])
def methodhandler(method,submethod):
    args = request.args.to_dict()
    args['password'] = request.headers.get('password',args.get("password"))
    method = method.lower()
    submethod = submethod.lower()
    res = "unknown"
    if method.startswith("user"):
        if submethod == 'get':
            res = methods.users.get(args)
        elif submethod == 'reg':
            res = methods.users.reg(args)
        elif submethod == 'auth':
            res = methods.users.auth(args)
        elif submethod == 'del':
            res = methods.users.delete(args)
        else: res = methods.utils.error(400,'unknown method passed'),400

    elif method.startswith("mess"):
        if submethod == 'send':
            res = methods.messages.send(args)
        elif submethod == 'get':
            res = methods.messages.get(args)
        elif submethod == 'gethistory':
            res = methods.messages.gethistory(args)
        elif submethod == 'del':
            res = methods.messages.delete(args)
        elif submethod == 'edit':
            res = methods.messages.edit(args)
        elif submethod == 'chats':
            res = methods.chats.get(args)
        else: res = methods.utils.error(400,'unknown method passed'),400

    elif method.startswith("ach"):
        if submethod == 'give':
            res = methods.achive.give(args)
        elif submethod == 'get':
            res = methods.achive.get(args)
        elif submethod == 'new':
            res = methods.achive.new(args)
        else: res = methods.utils.error(400,'unknown method passed'),400
            
    elif method.startswith("group"):
        if submethod == 'get':
            res = methods.groups.get(args)
        elif submethod == 'new':
            res = methods.groups.new(args)
        elif submethod == 'join':
            res = methods.groups.join(args)
        elif submethod == 'del':
            res = methods.groups.delete(args)
        elif submethod == 'getbyname':
            res = methods.groups.getbyname(args)
        elif submethod == 'adduser':
            res = methods.groups.adduser(args)
        elif submethod == 'addadmin':
            res = methods.groups.addadmin(args)
        elif submethod == 'edit':
            res = methods.groups.edit(args)
        else: res = methods.utils.error(400,'unknown method passed'),400

    elif method.startswith("vul"):
        if submethod == 'set':
            res = methods.vul.set(args)
        elif submethod == 'get':
            res = methods.vul.get(args)

    elif method.startswith("acc"):
        if submethod == 'changepass':
            res = methods.account.changepass(args)
        elif submethod == 'addsocial':
            res = methods.account.addsocial(args)

    elif method.startswith("bug"):
        if submethod == 'new':
            res = methods.bugs.new(args)
        elif submethod == 'get':
            res = methods.bugs.get(args)
        elif submethod == 'comment':
            res = methods.bugs.new(args)
        elif submethod == 'getcomments':
            res = methods.bugs.get(args)
        elif submethod == 'changestat':
            res = methods.bugs.changestat(args)
        elif submethod == 'edit':
            res = methods.bugs.edit(args)
        else: res = methods.utils.error(400,'unknown method passed'),400

    elif method.startswith("pool"):
        if submethod == 'get':
            res = methods.pool.get(args)
        elif submethod == 'read':
            res = methods.pool.read(args)

    else: res = methods.utils.error(400,'unknown method passed'),400
    print(res)
    if "error" in res:
        return res,res["error"]["code"]
    else: return res