from methods import utils,db,users
import time,json
from methods.users import _gett
from methods.utils import secure
def get(args):
    ss = utils.notempty(args,['accesstoken','id'])
    if ss == True: 
        token = args['accesstoken']
        id = args['id']
        res = _gett(token)
        return res if 'error' in res else _get(id)
    else:
        return ss
def _get(id):
    if False == utils.validr(id,utils.IDR):
        return utils.error(400,"'id' is invalid")
    group = (db.exec('''select id,name,owner_id,users,type,admins from groups where id = :id ''',{'id':id}))
    if len(group) == 0:
        return utils.error(404,"this group not exists")
    else:
        group = group[0]
        return {'id':group[0],'name':secure(group[1]),'owner_id':group[2],'users':json.loads(group[3]),'admins':json.loads(group[5]),'type':group[4]}



def getbyname(args):
    ss = utils.notempty(args,['accesstoken','name'])
    if ss == True: 
        token = args['accesstoken']
        name = args['name']
        thisuser = _gett(token)
        if False == utils.validr(name,utils.NAMER):
            return utils.error(400,"'name' is invalid")
        if 'error' in thisuser:
            return thisuser 
        group = (db.exec('''select id,name,owner_id,users,type from groups where name = :name ''',{'name':name}))
        if len(group) == 0:
            return utils.error(404,"this group not exists")
        else:
            group = group[0]
            return {'id':group[0],'name':secure(group[1]),'owner_id':group[2],'users':json.loads(group[3]),'type':group[4]}
    else:
        return ss

def new(args):
    ss = utils.notempty(args,['accesstoken','name','type'])
    if ss == True: 
        token = args['accesstoken']
        name = args['name']
        thisuser = _gett(token)
        if 'error' in thisuser:
            return thisuser 
        db.exec('''insert into groups (owner_id,name,type,users)
        values (?,?,?,?)''',(thisuser[0],name,args['type'],str([thisuser[0],]),))
        groupid = db.exec('''select seq from sqlite_sequence where name="groups"''')[0][0]
        return {'id':groupid}
    else:
        return ss

def edit(args):
    ss = utils.notempty(args,['accesstoken','id'])
    if ss == True: 
        token = args['accesstoken']
        thisuser = _gett(token)
        if 'error' in thisuser:
            return thisuser 
        group = _get(args['id'])
        if "error" in group:
            return group
        name = args.get("name",group['name'])
        type = args.get("type",group['type'])
        if thisuser[0] == group['owner_id']:
            db.exec('''UPDATE groups
                SET name = :name
                ,type = :type

                WHERE id = :id''',
                
                {
                    'id':args['id'],
                    'name':name,
                    'type':type,
                }
                )
            return {'state':'ok'}
    else:
        return ss

def delete(args):
    ss = utils.notempty(args,['accesstoken','id'])
    if ss == True: 
        token = args['accesstoken']
        thisuser = _gett(token)
        if 'error' in thisuser:
            return thisuser 
        group = _get(args['id'])
        if "error" in group:
            return group
        if thisuser[0] == group['owner_id']:
            db.exec('''DELETE FROM groups
                WHERE id = :id''',
                
                {
                    'id':args['id']
                }
                )
            return {'state':'ok'}
    else:
        return ss

def adduser(args):
    ss = utils.notempty(args,['accesstoken','id','user_id'])
    if ss == True: 
        token = args['accesstoken']
        id = args['id']
        user_id=args['user_id']
        thisuser = _gett(token)
        if 'error' in thisuser:
            return thisuser 
        group = _get(args['id'])
        if thisuser[0] in group['admins'] or thisuser[0] == group['owner_id']:
            users = list(json.loads(group['users']))
            if not user_id in users:
                users.append(user_id)
            db.exec('''UPDATE groups
                    SET users = :nusers
                    WHERE id = :id''',{'id':id,'nusers':str(users)})
            return {'state':'ok'}
        return utils.error(403,"access denided for this group")
    else:
        return ss

def join(args):
    ss = utils.notempty(args,['accesstoken','id'])
    if ss == True: 
        token = args['accesstoken']
        id = args['id']
        thisuser = _gett(token)
        if 'error' in thisuser:
            return thisuser 
        group = _get(args['id'])
        if group['type'] == 0 and not thisuser[0] in group['users']:
            users = list(group['users'])
            if not thisuser[0] in users:
                users.append(thisuser[0])
            db.exec('''UPDATE groups
                    SET users = :nusers
                    WHERE id = :id''',{'id':id,'nusers':str(users)})
            return {'state':'ok'}
        return utils.error(403,"access denided for this group")
    else:
        return ss

def addadmin(args):
    ss = utils.notempty(args,['accesstoken','id','user_id'])
    if ss == True: 
        token = args['accesstoken']
        id = args['id']
        user_id=args['user_id']
        thisuser = _gett(token)
        if 'error' in thisuser:
            return thisuser 
        group = _get(args['id'])
        if thisuser[0] in group['admins'] or thisuser[0] == group['owner_id']:
            admins = list(group['admins'])
            if not user_id in admins:
                admins.append(user_id)
            users = list(group['users'])
            if not user_id in users:
                users.append(user_id)
            db.exec('''UPDATE groups
                    SET admins = :nadmins
                    users = :nusers
                    WHERE id = :id''',{'id':id,'nadmins':admins,'nusers':str(users)})
            return {'state':'ok'}
        return utils.error(403,"access denided for this group")
    else:
        return ss