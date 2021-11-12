from api import api
import methods.messages
import methods.utils
import methods.users
import methods.updates
import methods.chats
import methods.bugs
import methods.groups
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

@api.route('/method', methods=['GET',"POST"])
def methodhandler():
    args = request.args.to_dict()
    ss = methods.utils.notempty(args,['method'])
    if ss == True:
        method = str(args['method'].lower())
        submethod = method.split('.')[1]
        res = {}
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
            elif submethod == 'chats':
                res = methods.chats.get(args)
            else: res = methods.utils.error(400,'unknown method passed'),400

        elif method.startswith("group"):
            if submethod == 'get':
                res = methods.groups.get(args)
            elif submethod == 'new':
                res = methods.groups.new(args)
            elif submethod == 'join':
                res = methods.groups.join(args)
            elif submethod == 'getbyname':
                res = methods.groups.getbyname(args)
            elif submethod == 'adduser':
                res = methods.groups.adduser(args)
            elif submethod == 'addadmin':
                res = methods.groups.addadmin(args)
            else: res = methods.utils.error(400,'unknown method passed'),400

        elif method.startswith("bug"):
            if submethod == 'new':
                res = methods.bugs.new(args)
            elif submethod == 'get':
                res = methods.bugs.get(args)
            elif submethod == 'changestat':
                res = methods.bugs.changestat(args)
            else: res = methods.utils.error(400,'unknown method passed'),400

        elif method == 'updates.get':
            res = methods.updates.get(args)

        else: res = methods.utils.error(400,'unknown method passed'),400

        if "error" in res:
            return res,res["error"]["code"]
        else: return res
    else: return ss,400