from api import api
import methods.messages
import methods.utils
import methods.users
import methods.updates
import methods.chats
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
        method = args['method'].lower()
        res = {}
        if method == 'user.get':
            res = methods.users.get(args)
        elif method == 'user.reg':
            res = methods.users.reg(args)

        elif method == 'user.auth':
            res = methods.users.auth(args)

        elif method == 'user.del':
            res = methods.users.delete(args)

        elif method == 'message.send':
            res = methods.messages.send(args)

        elif method == 'message.get':
            res = methods.messages.get(args)

        elif method == 'message.chats':
            res = methods.chats.get(args)

        elif method == 'updates.get':
            res = methods.updates.get(args)

        else: res = methods.utils.error(400,'unknown method passed'),400

        if "error" in res:
            return res,res["error"]["code"]
        else: return res
    else: return ss,400