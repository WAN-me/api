
from api import api
import methods.messages
import methods.utils
import methods.users
import methods.pool
import methods.chats
import methods.bugs
import methods.groups
import methods.account
import methods.achive
from flask import request
from werkzeug import utils

ERRORS = {
    "404": 'Page not found',
    "500": 'Internal server error',
    "400": 'Unknown method passed'}


@api.errorhandler(404)
def page_not_found(error):
    return methods.utils.error(404, ERRORS['404']), 404


@api.errorhandler(500)
def ISE(error):
    return methods.utils.error(500, ERRORS['500']), 500


@api.route('/method/<method>/<submethod>', methods=['GET', "POST"])
@api.route('/method/<method>/<submethod>/', methods=['GET', "POST"])
@api.route('/method/<method>.<submethod>', methods=['GET', "POST"])
@api.route('/method/<method>.<submethod>/', methods=['GET', "POST"])
def method_handler(method, submethod):
    params = request.args.to_dict()
    form = request.form.to_dict()
    args = ((params | form))
    method = method.lower()
    submethod = submethod.lower()
    res = "Unknown", 200
    if method.startswith("user"):
        if submethod.startswith('get'):
            res = methods.users.get(args)
        else:
            res = methods.utils.error(400, ERRORS['400']), 400

    elif method.startswith("mess"):  # messages section
        if submethod.startswith('send'):
            res = methods.messages.send(args)
        elif submethod == 'get':
            res = methods.messages.get(args)
        elif submethod.startswith('gethistory'):
            res = methods.messages.gethistory(args)
        elif submethod.startswith('del'):
            res = methods.messages.delete(args)
        elif submethod.startswith('edit'):
            res = methods.messages.edit(args)
        elif submethod.startswith('chats'):
            res = methods.chats.get(args)
        else:
            res = methods.utils.error(400, ERRORS['400']), 400

    elif method.startswith("ach"):  # achive section
        if submethod.startswith('give'):
            res = methods.achive.give(args)
        elif submethod.startswith('get'):
            res = methods.achive.get(args)
        elif submethod.startswith('new'):
            res = methods.achive.new(args)
        else:
            res = methods.utils.error(400, ERRORS['400']), 400

    elif method.startswith("group"):  # groups section
        if submethod == 'get': #
            res = methods.groups.get(args)
        elif submethod.startswith('new'): #
            res = methods.groups.new(args)
        elif submethod.startswith('join'): #
            res = methods.groups.join(args)
        elif submethod.startswith('del'): 
            res = methods.groups.delete(args)
        elif submethod.startswith('getbyname'): #
            res = methods.groups.getbyname(args)
        elif submethod.startswith('adduser'): #
            res = methods.groups.adduser(args)
        elif submethod.startswith('leave'): #
            res = methods.groups.leave(args)
        elif submethod.startswith('addadmin'): #
            res = methods.groups.addadmin(args)
        elif submethod.startswith('edit'): #
            res = methods.groups.edit(args)
        else:
            res = methods.utils.error(400, ERRORS['400']), 400

    elif method.startswith("acc"):  # accounts section
        if submethod.startswith('changepass'):
            res = methods.account.changepass(args)
        elif submethod.startswith('addsocial'):
            res = methods.account.addsocial(args)
        elif submethod.startswith('reg'):
            res = methods.account.reg(args)
        elif submethod.startswith('auth'):
            res = methods.account.auth(args)
        elif submethod.startswith('del'):
            res = methods.account.delete(args)
        elif submethod.startswith('verif'):
            res = methods.account.verif(args)
        else:
            res = methods.utils.error(400, ERRORS['400']), 400

    elif method.startswith("bug"):  # bugs section
        if submethod.startswith('new'):
            res = methods.bugs.new(args)
        elif submethod.startswith('get'):
            res = methods.bugs.get(args)
        elif submethod.startswith('comment'):
            res = methods.bugs.new(args)
        elif submethod.startswith('getcomments'):
            res = methods.bugs.get(args)
        elif submethod.startswith('changestat'):
            res = methods.bugs.changestat(args)
        elif submethod.startswith('edit'):
            res = methods.bugs.edit(args)
        else:
            res = methods.utils.error(400, ERRORS['400']), 400

    elif method.startswith("pool"):  # pool section
        if submethod.startswith('get'):
            res = methods.pool.get(args)
        elif submethod.startswith('read'):
            res = methods.pool.read(args)
    else:
        res = methods.utils.error(400, ERRORS['400']), 400

    if "error" in res:
        return res, res["error"]["code"]

    else:
        return res
