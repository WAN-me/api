import queue
import sbeaver
import cfg
from sqlite3 import connect
from queue import Queue
import tmp

from methods import messages, utils, users, poll, chats, bugs, groups, account, achive

ERRORS = {
    "404": 'Page not found',
    "500": 'Internal server error',
    "400": 'Unknown method passed'}

server = sbeaver.Server("0.0.0.0", port=3000, sync=False)


tmp.vars['db'] = connect(cfg.dataBaseFile, check_same_thread=False)
tmp.vars['cursor'] = tmp.vars['db'].cursor()


@server.ebind(r'/poll[/|\.]<method>')
def poll_handler(request, method):
    request.parse_all()
    params = request.args
    form = request.data
    args = ((params | form))
    if method == "get":
        res = poll.get(args)
        return res.get('error', {'code': 200})['code'], res
    if method == "read":
        res = poll.read(args)
        return res.get('error', {'code': 200})['code'], res

@server.code404()
def page_not_found(error):
    return utils.error(404, ERRORS['404'])

@server.code500()
def ISE(req, error):
    return utils.error(500, ERRORS['500'])

@server.ebind(r'/method/<method>[/|\.]<submethod>$')
def method_handler(request, method, submethod):
    request.parse_all()
    params = request.args
    form = request.data
    args = ((params | form))
    method = method.lower()
    submethod = submethod.lower()
    res = "Unknown", 200
    if method.startswith("user"):
        if submethod.startswith('get'):
            res = users.get(args)
        else:
            res = utils.error(400, ERRORS['400']), 400
    elif method.startswith("mess"):  # messages section #
        if submethod.startswith('send'): #
            res = messages.send(args)
        elif submethod == 'get': # 
            res = messages.get(args)
        elif submethod.startswith('gethistory'):# 
            res = messages.gethistory(args)
        elif submethod.startswith('del'): #
            res = messages.delete(args)
        elif submethod.startswith('edit'): #
            res = messages.edit(args) 
        elif submethod.startswith('chats'): #
            res = chats.get(args)
        else:
            res = utils.error(400, ERRORS['400']), 400

    elif method.startswith("ach"):  # achive section
        if submethod.startswith('give'):
            res = achive.give(args)
        elif submethod.startswith('get'):
            res = achive.get(args)
        elif submethod.startswith('new'):
            res = achive.new(args)
        else:
            res = utils.error(400, ERRORS['400']), 400

    elif method.startswith("group"):  # groups section #
        if submethod == 'get': #
            res = groups.get(args)
        elif submethod.startswith('new'): #
            res = groups.new(args)
        elif submethod.startswith('join'): #
            res = groups.join(args)
        elif submethod.startswith('del'): #
            res = groups.delete(args)
        elif submethod.startswith('getbyname'): #
            res = groups.getbyname(args)
        elif submethod.startswith('adduser'): #
            res = groups.adduser(args)
        elif submethod.startswith('leave'): #
            res = groups.leave(args)
        elif submethod.startswith('addadmin'): #
            res = groups.addadmin(args)
        elif submethod.startswith('edit'): #
            res = groups.edit(args)
        else:
            res = utils.error(400, ERRORS['400']), 400

    elif method.startswith("acc"):  # accounts section
        if submethod.startswith('changepass'): #
            res = account.changepass(args)
        elif submethod.startswith('addsocial'):
            res = account.addsocial(args)
        elif submethod.startswith('reg'): #
            res = account.reg(args)
        elif submethod.startswith('auth'): #
            res = account.auth(args)
        elif submethod.startswith('del'): #
            res = account.delete(args)
        elif submethod.startswith('verif'):
            res = account.verif(args)
        else:
            res = utils.error(400, ERRORS['400']), 400

    elif method.startswith("bug"):  # bugs section
        if submethod.startswith('new'):
            res = bugs.new(args)
        elif submethod.startswith('get'):
            res = bugs.get(args)
        elif submethod.startswith('comment'):
            res = bugs.new(args)
        elif submethod.startswith('getcomments'):
            res = bugs.get(args)
        elif submethod.startswith('changestat'):
            res = bugs.changestat(args)
        elif submethod.startswith('edit'):
            res = bugs.edit(args)
        else:
            res = utils.error(400, ERRORS['400']), 400

    elif method.startswith("poll") or method.startswith("pool"):  # poll section #
        return sbeaver.redirect(307,f'/poll/{submethod}')
        if submethod.startswith('get'): #
            res = poll.get(args)
        elif submethod.startswith('read'): #
            res = poll.read(args)
    else:
        res = utils.error(400, ERRORS['400']), 400
    if "error" in res:
        return res["error"]["code"], res

    else:
        return 200, res

server.start()