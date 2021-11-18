import os
from api import api
import methods.messages
import methods.utils
import methods.users
import methods.updates
import methods.chats
import methods.bugs
import methods.groups
import methods.kino
import methods.vul
from flask import request,redirect


@api.errorhandler(404)
def pageNotFound(error):
    return methods.utils.error(404,'page not found'),404
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
@api.route('/cloud', methods=['GET',"POST"])
def upload():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        path = os.path.join(api.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)
        return redirect("https://cloud.wan-group.ru/upload/"+path.split('/var/www/cloud/upload/',1)[1], code=301)

        return 'ok'
    return '''
    <h1>Upload new File</h1>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file1">
      <input type="submit">
    </form>
    '''
@api.route('/method', methods=['GET',"POST"])
def methodhandler():
    args = request.args.to_dict()
    args['password'] = request.headers.get('password',args.get("password"))
    ss = methods.utils.notempty(args,['method'])
    if ss == True:
        method = str(args['method'].lower())
        submethod = method.split('.')[1]
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
            elif submethod == 'chats':
                res = methods.chats.get(args)
            else: res = methods.utils.error(400,'unknown method passed'),400

        elif method.startswith("kino"):
            if submethod == 'search':
                return methods.kino.search(args)
            elif submethod == 'films':
                return methods.kino.films(args)
                
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

        elif method.startswith("upd"):
            if submethod == 'get':
                res = methods.updates.get(args)

        else: res = methods.utils.error(400,'unknown method passed'),400
        print(res)
        if "error" in res:
            return res,res["error"]["code"]
        else: return res
    else: return ss,400