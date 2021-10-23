from api import api
import methods.messages
import methods.utils
import methods.users
import methods.updates
from flask import request,redirect


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

        if method == 'user.get':
            return methods.users.get(args)

        elif method == 'user.reg':
            return methods.users.reg(args)

        elif method == 'user.auth':
            return methods.users.auth(args)

        elif method == 'user.del':
            return methods.users.delete(args)

        elif method == 'message.send':
            return methods.messages.send(args)

        elif method == 'message.get':
            return methods.messages.get(args)

        elif method == 'updates.get':
            return methods.updates.get(args)

        else: return methods.utils.error(5,'unknown method passed')
    else: return ss