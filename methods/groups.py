from methods import utils, db
import json
from methods.account import _gett
from methods.utils import secure


def get(args):
    ss = utils.notempty(args, ['accesstoken', 'id'])
    if ss == True:
        token = args['accesstoken']
        id = args['id']
        user = _gett(token, 1, cursor=args['cursor'])
        return user if 'error' in user else _get(id, args['cursor'])
    else:
        return ss


def _get(id,cursor):
    if False == utils.validr(id, utils.IDR):
        return utils.error(400, "'id' is invalid")
    cursor.execute('''select id, name, owner_id, users, type, admins from groups where id = :id ''', {
                'id': id})
    raw_group = cursor.fetchall()
            
    if len(raw_group) == 0:
        return utils.error(404, "This group not exists")
    else:
        raw_group = raw_group[0]
        return {
            'id': raw_group[0], 'name': secure(
                raw_group[1]), 'owner_id': raw_group[2], 'users': json.loads(str(
                raw_group[3])), 'admins': json.loads(str(
                raw_group[5])), 'type': raw_group[4]}


def getbyname(args):
    ss = utils.notempty(args, ['accesstoken', 'name'])
    if ss == True:
        token = args['accesstoken']
        name = args['name']
        user = _gett(token, 1, cursor=args['cursor'])
        if 'error' in user:
            return user
        args['cursor'].execute('''select id, name, owner_id, users, type from groups where name = :name ''', {
                    'name': name})
        raw_group = args['cursor'].fetchall()
        if len(raw_group) == 0:
            return utils.error(404, "This group not exists")
        else:
            raw_group = raw_group[0]
            return {
                'id': raw_group[0],
                'name': secure(
                    raw_group[1]),
                'owner_id': raw_group[2],
                'users': json.loads(
                    raw_group[3]),
                'type': raw_group[4]}
    else:
        return ss


def new(args):
    ss = utils.notempty(args, ['accesstoken', 'name', 'type'])
    if ss == True:
        token = args['accesstoken']
        name = args['name']
        user = _gett(token, 1, cursor=args['cursor'])
        if 'error' in user:
            return user
        args['cursor'].execute('''insert into groups (owner_id, name, type, users)
        values (?,?,?,?)''', (user[0], name, args['type'], str([user[0], ]),))
        args['connection'].commit()
        args['cursor'].execute('''select seq from sqlite_sequence where name="groups"''')
        group_id = args['cursor'].fetchall()[0][0]
            
        return {'id': group_id}
    else:
        return ss


def edit(args):
    ss = utils.notempty(args, ['accesstoken', 'id'])
    if ss == True:
        token = args['accesstoken']
        user = _gett(token, 1, cursor=args['cursor'])
        if 'error' in user:
            return user
        group = _get(args['id'], args['cursor'])
        if "error" in group:
            return group
        name = args.get("name", group['name'])
        type = args.get("type", group['type'])
        if user[0] == group['owner_id']:
            args['cursor'].execute('''UPDATE groups
                SET name = :name 
                ,type = :type

                WHERE id = :id''',

                    {
                        'id': args['id'],
                        'name': name,
                        'type': type,
                    }
                    )
            args['connection'].commit()
            return {'state': 'ok'}
    else:
        return ss


def delete(args):
    ss = utils.notempty(args, ['accesstoken', 'id'])
    if ss == True:
        token = args['accesstoken']
        user = _gett(token, 1, cursor=args['cursor'])
        if 'error' in user:
            return user
        group = _get(args['id'], args['cursor'])
        if "error" in group:
            return group
        if user[0] == group['owner_id']:
            args['cursor'].execute('''DELETE FROM groups
                WHERE id = :id''',

                    {
                        'id': args['id']
                    }
                    )
            args['connection'].commit()
            return {'state': 'ok'}
    else:
        return ss


def adduser(args):
    ss = utils.notempty(args, ['accesstoken', 'id', 'user_id'])
    if ss == True:
        token = args['accesstoken']
        id = args['id']
        user_id = args['user_id']
        user = _gett(token, 1, cursor=args['cursor'])
        if 'error' in user:
            return user
        group = _get(args['id'], args['cursor'])
        if user[0] in group['admins'] or user[0] == group['owner_id']:
            users = list(group['users'])
            if user_id not in users:
                users.append(int(user_id))
            args['cursor'].execute('''UPDATE groups
                    SET users = :nusers
                    WHERE id = :id''', {'id': id, 'nusers': str(users)})
            args['connection'].commit()
            return {'state': 'ok'}
        return utils.error(403, "Access denided for this group")
    else:
        return ss

def leave(args):    
    ss = utils.notempty(args, ['accesstoken', 'id'])
    if ss == True:
        token = args['accesstoken']
        id = args['id']
        user = _gett(token, 1, cursor=args['cursor'])
        if 'error' in user:
            return user
        group = _get(args['id'], args['cursor'])
        if user[0] in group['users']:
            users = list(group['users'])
            users.remove(user[0])
            args['cursor'].execute('''UPDATE groups
                    SET users = :nusers
                    WHERE id = :id''', {'id': id, 'nusers': str(users)})
            args['connection'].commit()
            return {'state': 'ok'}
        print((user[0],group['users']))
        return utils.error(403, "You are not member this group")
    else:
        return ss

def join(args):
    ss = utils.notempty(args, ['accesstoken', 'id'])
    if ss == True:
        token = args['accesstoken']
        id = args['id']
        user = _gett(token, 1, cursor=args['cursor'])
        if 'error' in user:
            return user
        group = _get(args['id'], args['cursor'])
        if group['type'] == 0 and not user[0] in group['users']:
            users = list(group['users'])
            if not user[0] in users:
                users.append(int(user[0]))
            args['cursor'].execute('''UPDATE groups
                    SET users = :nusers
                    WHERE id = :id''', {'id': id, 'nusers': str(users)})
            args['connection'].commit()
            return {'state': 'ok'}
        return utils.error(403, "Access denided for this group")
    else:
        return ss


def addadmin(args):
    ss = utils.notempty(args, ['accesstoken', 'id', 'user_id'])
    if ss == True:
        token = args['accesstoken']
        id = args['id']
        user_id = int(args['user_id'])
        user = _gett(token, 1, cursor=args['cursor'])
        if 'error' in user:
            return user
        group = _get(args['id'], args['cursor'])
        if user[0] in group['admins'] or user[0] == group['owner_id']:
            admins = list(group['admins'])
            if user_id not in admins:
                admins.append(user_id)
            users = list(group['users'])
            if user_id not in users:
                users.append(user_id)
            args['cursor'].execute('''UPDATE groups
                    SET admins = :nadmins,
                    users = :nusers
                    WHERE id = :id''', {'id': id, 'nadmins': str(admins), 'nusers': str(users)})
            args['connection'].commit()
            return {'state': 'ok'}
        return utils.error(403, "Access denided for this group")
    else:
        return ss
