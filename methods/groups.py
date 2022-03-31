from methods import utils, db
import json
from methods import users as uusers
from methods.account import _gett
from methods.utils import secure
import tmp


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
    tmp.vars['cursor'].execute('''select id, name, owner_id, type, admins from groups where id = :id ''', {
                'id': id})
    raw_group = tmp.vars['cursor'].fetchall()
    if len(raw_group) == 0:
        return utils.error(404, "This group not exists")
    else:
        raw_group = raw_group[0]
        tmp.vars['cursor'].execute('''select user_id from members where object_id = :id ''', {
                'id': id})
        userss = tmp.vars['cursor'].fetchall()
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
        tmp.vars['cursor'].execute('''select id, name, owner_id, type from groups where name = :name ''', {
                    'name': name})
        raw_group = tmp.vars['cursor'].fetchall()
        if len(raw_group) == 0:
            return utils.error(404, "This group not exists")
        else:
            raw_group = raw_group[0]
            tmp.vars['cursor'].execute('''select user_id from members where object_id = :id ''', {
                'id': raw_group[0]})
            users = tmp.vars['cursor'].fetchall()[0]
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
        tmp.vars['cursor'].execute('''insert into groups (owner_id, name, type)
        values (?, ?, ?)''', (user[0], name, args['type'],))
        tmp.vars['cursor'].execute('''select seq from sqlite_sequence where name="groups"''')
        group_id = tmp.vars['cursor'].fetchall()[0][0]
        tmp.vars['cursor'].execute('''insert into members (user_id, object_id, type)
        values (?, ?, ?)''', (user[0], group_id, args['type']))
        tmp.vars['db'].commit()
            
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
            tmp.vars['cursor'].execute('''UPDATE groups
                SET name = :name 
                ,type = :type

                WHERE id = :id''',

                    {
                        'id': args['id'],
                        'name': name,
                        'type': type,
                    }
                    )
            tmp.vars['db'].commit()
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
            tmp.vars['cursor'].execute('''DELETE FROM groups
                WHERE id = :id''',

                    {
                        'id': args['id']
                    }
                    )
            tmp.vars['cursor'].execute('''DELETE FROM members
                WHERE object_id = :id''',

                    {
                        'id': args['id']
                    }
                    )
            tmp.vars['db'].commit()
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
            tmp.vars['cursor'].execute('''insert OR IGNORE into members
            (user_id, object_id, type)
            values (?, ?, ?)''', (user_id, id, group['type']))
            tmp.vars['db'].commit()
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
            tmp.vars['cursor'].execute('''delete from members
            where user_id = ? and object_id = ?''', (user[0], id,))
            tmp.vars['db'].commit()
            if group['type'] == 1:
                    username = uusers._get(user[0])['name']
                    _send_admin(id, f'Пользователь {username} покинул группу.', group['name'])
            return {'state': 'ok'}
        return utils.error(403, "You are not member this group")
    else:
        return ss

def _send_admin(to_id, text, group_name):
    tmp.vars['cursor'].execute('''insert into messages (from_id, to_id, text)
        values (?,?,?)''', (-1, -to_id, text,))

    tmp.vars['db'].commit()

    tmp.vars['cursor'].execute('''select seq from sqlite_sequence where name="messages"''')
    msg_id = tmp.vars['cursor'].fetchall()[0][0]

    tmp.vars['cursor'].execute(f'''insert into poll (type, user_id, object_id, object)
        select 1, user_id, {msg_id}, ?
        from members
        where object_id = {to_id} ;''', (json.dumps({'id': msg_id,
            'from_id': -1,
            'to_id': -to_id,
            'text': text}),))

    tmp.vars['cursor'].execute(f'''insert into chats (id, user_id, name)
        select {-to_id}, user_id, ?
        from members
        where object_id = {to_id};''', (group_name, ))

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
                tmp.vars['cursor'].execute('''insert into members (user_id, object_id, type)
                values (?, ?, ?)''', (user[0], id, group['type'],))

                if group['type'] == 1:
                    username = uusers._get(user[0])['name']
                    _send_admin(id, f'Пользователь {username} вступил в группу.', group['name'])
                    

                tmp.vars['db'].commit()
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
                tmp.vars['cursor'].execute('''insert into members (user_id, object_id, type)
                values (?, ?, ?)''', (user_id, id, group['type'],))
            tmp.vars['cursor'].execute('''UPDATE groups
                    SET admins = :nadmins
                    WHERE id = :id''', {'id': id, 'nadmins': str(admins)})
            tmp.vars['db'].commit()
            return {'state': 'ok'}
        return utils.error(403, "Access denided for this group")
    else:
        return ss
