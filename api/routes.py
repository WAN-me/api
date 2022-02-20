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

@api.route('/method/<method>/<submethod>', methods=['GET',"POST"])
@api.route('/method/<method>/<submethod>/', methods=['GET',"POST"])
@api.route('/method/<method>.<submethod>', methods=['GET',"POST"])
@api.route('/method/<method>.<submethod>/', methods=['GET',"POST"])
def methodhandler(method,submethod):
    params = request.args.to_dict()
    form = request.form.to_dict()
    args = ((params|form))
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