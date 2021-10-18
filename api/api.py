from flask import Flask
import methods
from flask import request,redirect
api = Flask(__name__)

@api.route('/', methods=['GET',"POST"])
def m():
    return {'message':'welcome to the WAN-m api!'}
@api.route('/favicon.ico')
def favicon():
    return redirect("https://wan-group.ru/favicon.svg", code=302)
@api.route('/index', methods=['GET',"POST"])
def index():
    return "You in index"
@api.route('/user', methods=['GET',"POST"])
def user():
    return methods.users.get(request.args)
@api.route('/reg', methods=['GET',"POST"])
def register():
    return methods.users.reg(request.args.to_dict())

if __name__ == '__main__':
    api.run(host="0.0.0.0")