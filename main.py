#!/usr/bin/python3
import sbeaver
import cfg
from sqlite3 import connect
import tmp
import jdb



block = jdb.Db('blacklist.json').data
from methods import messages, utils, users, poll, chats, bugs, groups, account, achive
ERRORS = {
    "404": 'Page not found',
    "500": 'Internal server error',
    "400": 'Unknown method passed'}

server = sbeaver.Server("0.0.0.0", port=3000, sync=False)


tmp.vars['db'] = connect(cfg.dataBaseFile, check_same_thread=False)
tmp.vars['cursor'] = tmp.vars['db'].cursor()

@server.sbind('/info')
def info(req):
     return 200, req.dict

@server.ebind(r'/poll[/|\.]<method>')
def poll_handler(request, method):
    request.parse_all()
    params = request.args
    form = request.data
    args = ((params | form))
    if method == "get":
        res = poll.get(args)
    elif method == "read":
        res = poll.read(args)
    return res.get('error', {'code': 200})['code'], res
    

@server.code404()
def page_not_found(error):
    return utils.error(404, ERRORS['404'])

@server.code500()
def ISE(req, error):
    return utils.error(500, ERRORS['500'])

method_list = {
    'user': {
        'get':users.get,
        'reg': account.reg,
        'auth': account.auth,
        'del': account.delete
        }, 
    'message': {
        'get': messages.get,
        'send': messages.send,
        'gethistory': messages.gethistory,
        'del': messages.delete,
        'delete': messages.delete,
        'edit': messages.edit,
        'chats': chats.get
        }, 
    'achive': {
        'give': achive.give,
        'get': achive.get,
        'new': achive.new
    },
    'group': {
        'get': groups.get,
        'new': groups.new,
        'join': groups.join,
        'del': groups.delete,
        'delete': groups.delete,
        'getbyname': groups.getbyname,
        'adduser': groups.adduser,
        'leave': groups.leave,
        'addadmin': groups.addadmin,
        'edit': groups.edit
    }, 
    'account': {
        'changepass': account.changepass,
        'addsocial': account.addsocial,
        'reg': account.reg,
        'auth': account.auth,
        'del': account.delete,
        'delete': account.delete,
        'verif': account.verif,
        'invite': account.invite
    },
    'poll': {
        'get': poll.get,
        'read': poll.read,
    }
}

@server.ebind(r'/method/<method>[/|\.]<submethod>$')
def method_handler(request, method, submethod):
    params = request.args
    form = request.data
    args = ((params | form))
    args['ip'] = request.ip
    res = utils.error(400, ERRORS['400'])
    if request.ip in block:
        res = utils.error(403, 'Ip in blacklist')
    else:
        submethod = submethod.lower()
        method = str(method.lower())
        method = method[:-1] if method.endswith('s') else method
        print(submethod,method)
        if method in method_list:
            if submethod in method_list[method]:
                res = method_list[method][submethod](args)
            else:
                res = utils.error(400, ERRORS['400'])
        elif method in ("poll", "pool"):  # poll section #
            return sbeaver.redirect(307,f'/poll/{submethod}')

    if "error" in res:
        return res["error"]["code"], res
    else:
        return 200, res

server.start()