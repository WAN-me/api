from api import api
import api.methods.messages
import api.methods.utils
import api.methods.users
import api.methods.updates
from flask import request,redirect

@api.errorhandler(404)
def pageNotFound(error):
    return api.methods.utils.error(404,'page not found')
@api.errorhandler(500)
def pageNotFound(error):
    return api.methods.utils.error(500,'internal server error')
@api.route('/', methods=['GET',"POST"])
def m():
    return {'message':'welcome to the WAN-m api!'}
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
    ss = api.methods.utils.notempty(args,['method'])
    if ss == True:
        method = args['method'].lower()

        if method == 'user.get':
            return api.methods.users.get(args)

        elif method == 'user.reg':
            return api.methods.users.reg(args)

        elif method == 'user.auth':
            return api.methods.users.auth(args)

        elif method == 'user.del':
            return api.methods.users.delete(args)

        elif method == 'message.send':
            return api.methods.messages.send(args)

        elif method == 'message.get':
            return api.methods.messages.get(args)

        elif method == 'updates.get':
            return api.methods.updates.get(args)

        else: return api.methods.utils.error(5,'unknown method passed')
    else: return ss