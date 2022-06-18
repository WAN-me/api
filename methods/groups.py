from methods import utils, db, messages
import json
from methods import users as uusers
from methods.account import _gett
from methods.utils import secure


def get(args):
    ss = utils.notempty(args, ['accesstoken', 'id'])
    if ss == True:
        token = args['accesstoken']
        id = args['id']
        user = _gett(token, 1)
        return user if 'error' in user else _get(id)
    else:
        return ss


def _get(id):
    if False == utils.validr(id, utils.IDR):
        return utils.error(400, "'id' is invalid")
    raw_group = db.exec('''select id, name, owner_id, type, admins from groups where id = :id ''', {
                'id': id})
    if len(raw_group) == 0:
        return utils.error(404, "This group not exists")
    else:
        raw_group = raw_group[0]
        userss = db.exec('''select user_id from members where object_id = :id ''', {
                'id': id})
        users = [x[0] for x in userss]
        return {
            'id': raw_group[0], 
            'name': secure(raw_group[1]), 
            'owner_id': raw_group[2], 
            'users': users, 
            'admins': json.loads(str(raw_group[4])), 
            'type': raw_group[3]}


def getbyname(args):
    ss = utils.notempty(args, ['accesstoken', 'name'])
    if ss == True:
        token = args['accesstoken']
        name = args['name']
        user = _gett(token, 1)
        if 'error' in user:
            return user
        raw_group = db.exec('''select id, name, owner_id, type from groups where name = :name ''', {
                    'name': name})
        if len(raw_group) == 0:
            return utils.error(404, "This group not exists")
        else:
            raw_group = raw_group[0]
            users = db.exec('''select user_id from members where object_id = :id ''', {
                'id': raw_group[0]})[0]
            return {
                'id': raw_group[0],
                'name': secure(
                    raw_group[1]),
                'owner_id': raw_group[2],
                'users': users,
                'type': raw_group[3]}
    else:
        return ss


def new(args):
    ss = utils.notempty(args, ['accesstoken', 'name', 'type'])
    if ss == True:
        token = args['accesstoken']
        name = args['name']
        user = _gett(token, 1)
        if 'error' in user:
            return user
        db.exec('''insert into groups (owner_id, name, type)
        values (?, ?, ?)''', (user[0], name, args['type'],))
        group_id = db.exec('''select seq from sqlite_sequence where name="groups"''')[0][0]
        db.exec('''insert into members (user_id, object_id, type) 
        values (?, ?, ?)''', (user[0], group_id, args['type'])) # в список членов групп добавляем создателя
            
        return {'id': group_id}
    else:
        return ss


def edit(args):
    ss = utils.notempty(args, ['accesstoken', 'id'])
    if ss == True:
        token = args['accesstoken']
        user = _gett(token, 1)
        if 'error' in user:
            return user
        group = _get(args['id'])
        if "error" in group:
            return group
        name = args.get("name", group['name'])
        type = args.get("type", group['type'])
        if user[0] == group['owner_id']:
            db.exec('''UPDATE groups
                SET name = :name 
                ,type = :type

                WHERE id = :id''',

                    {
                        'id': args['id'],
                        'name': name,
                        'type': type,
                    }
                    )
            return {'state': 'ok'}
    else:
        return ss


def delete(args):
    ss = utils.notempty(args, ['accesstoken', 'id'])
    if ss == True:
        token = args['accesstoken']
        user = _gett(token, 1)
        if 'error' in user:
            return user
        group = _get(args['id'])
        if "error" in group:
            return group
        if user[0] == group['owner_id']:
            db.exec('''DELETE FROM groups
                WHERE id = :id''',

                    {
                        'id': args['id']
                    }
                    )
            db.exec('''DELETE FROM members
                WHERE object_id = :id''',

                    {
                        'id': args['id']
                    }
                    )
            return {'state': 'ok'}
    else:
        return ss


def adduser(args):
    ss = utils.notempty(args, ['accesstoken', 'id', 'user_id'])
    if ss == True:
        token = args['accesstoken']
        id = args['id']
        user_id = args['user_id']
        user = _gett(token, 1)
        if 'error' in user:
            return user
        group = _get(args['id'])
        if user[0] in group['admins'] or user[0] == group['owner_id']:
            users = list(group['users'])
            if user_id not in users:
                users.append(int(user_id))
            db.exec('''insert OR IGNORE into members
            (user_id, object_id, type)
            values (?, ?, ?)''', (user_id, id, group['type']))
            return {'state': 'ok'}
        return utils.error(403, "Access denided for this group")
    else:
        return ss

def leave(args):    
    ss = utils.notempty(args, ['accesstoken', 'id'])
    if ss == True:
        token = args['accesstoken']
        id = args['id']
        user = _gett(token, 1)
        if 'error' in user:
            return user
        group = _get(id)
        if user[0] in group['users']:
            db.exec('''delete from members
            where user_id = ? and object_id = ?''', (user[0], id,))
            if group['type'] == 1:
                    username = uusers._get(user[0])['name']
                    messages._send(-1, int(id), f'Пользователь {username} покинул группу.')
            return {'state': 'ok'}
        return utils.error(403, "You are not member this group")
    else:
        return ss
def join(args):
    ss = utils.notempty(args, ['accesstoken', 'id'])
    if ss == True:
        token = args['accesstoken']
        id = args['id']
        user = _gett(token, 1)
        if 'error' in user:
            return user
        group = _get(id)
        id = int(id)
        if group['type'] >= 0:
            users = group['users']
            if not user[0] in users:
                db.exec('''insert into members (user_id, object_id, type)
                values (?, ?, ?)''', (user[0], id, group['type'],)) # записываем в список членов

                if group['type'] == 1:
                    username = uusers._get(user[0])['name'] # получаем доп инфу о пользователе
                    messages._send(-1, -id, f'Пользователь {username} вступил в группу.')

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
        user = _gett(token, 1)
        if 'error' in user:
            return user
        group = _get(id)
        if user[0] in group['admins'] or user[0] == group['owner_id']:
            admins = list(group['admins'])
            if user_id not in admins:
                admins.append(user_id)
            users = list(group['users'])
            if user_id not in users:
                db.exec('''insert into members (user_id, object_id, type)
                values (?, ?, ?)''', (user_id, id, group['type'],))
            db.exec('''UPDATE groups
                    SET admins = :nadmins
                    WHERE id = :id''', {'id': id, 'nadmins': str(admins)})
            return {'state': 'ok'}
        return utils.error(403, "Access denided for this group")
    else:
        return ss
