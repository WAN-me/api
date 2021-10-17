from flask import Flask
import methods
from flask import request
api = Flask(__name__)

@api.route('/dropdb', methods=['GET',"POST"])
def dropdb():
    return methods.dropdatabase(request.args)
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
    return methods.reg(request.args)

if __name__ == '__main__':
    api.run(host="0.0.0.0")