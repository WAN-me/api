import json
from methods import utils, db, poll, chats, account, users, groups
from methods.utils import secure
import tmp

def send(args):
    ss = utils.notempty(args, ['accesstoken', 'text', 'to_id'])
    if ss == True:
        token = args['accesstoken']
        text = args['text']
        to_id = args['to_id']
        user = account._gett(token, 1)
        if 'error' in user:
            return user
        if False == utils.validr(str(to_id), utils.IDR):
            return utils.error(400, "'to_id' is invalid")

        to_id = int(to_id)
        tmp.vars['cursor'].execute('''insert into messages (from_id, to_id, text)
        values (?,?,?)''', (user[0], to_id, text,))
        tmp.vars['db'].commit()
        tmp.vars['cursor'].execute('''select seq from sqlite_sequence where name="messages"''')
        msg_id = tmp.vars['cursor'].fetchall()[0][0]
        text = secure(text)
        if to_id < 0: # сообщение в чат
            group = groups._get(-to_id)
            if 'error' in group:
                return group
            if not user[0] in group['users']: # пользователь не учатсник чата
                return utils.error(403,"access denided for this chat")

            tmp.vars['cursor'].execute(f'''insert into poll (type, user_id, object_id, object)
                select 1, user_id, {msg_id}, ?
                from members
                where object_id = {-to_id} and user_id != {user[0]};''', (json.dumps({'id': msg_id,
                    'from_id': user[0],
                    'to_id': to_id,
                    'text': text}),))

            tmp.vars['cursor'].execute(f'''insert into chats (id, user_id, name)
                select user_id, {to_id}, ?
                from members
                where object_id = {-to_id};''', (group['name'], ))

            tmp.vars['db'].commit()
        else:
            poll._set(1,
                  to_id,
                  msg_id,
                  {'id': msg_id,
                   'from_id': user[0],
                   'to_id': to_id,
                   'text': text})  # добавляем события
            chats._set(to_id, user[0], users._get(user[0])['name'])
        poll._set(2,
                  user[0],
                  msg_id,
                  {'id': msg_id,
                   'from_id': user[0],
                   'to_id': to_id,
                   'text': secure(text)}) # Сообщение доставленно

        # Добавляем в список чатов
        return {'id': msg_id}
    else:
        return ss


def gethistory(args):
    ss = utils.notempty(args, ['accesstoken', 'user_id'])
    if ss == True:
        token = args['accesstoken']
        user_id = args['user_id']
        count = args.get('count', 20)
        ofset = args.get('ofset', 0)
        if False == utils.validr(token, utils.TOKENR):
            return utils.error(400, "'accesstoken' is invalid")
        if False == utils.validr(user_id, utils.IDR):
            return utils.error(400, "'user_id' is invalid")
        if False == utils.validr(count, utils.IDR):
            return utils.error(400, "'count' is invalid")
        if False == utils.validr(ofset, utils.IDR):
            return utils.error(400, "'ofset' is invalid")
        user = account._gett(token, 1)
        if 'error' in user:
            return user

        messages = []
        if int(user_id) < 0: # this chat!
            tmp.vars['cursor'].execute(
            '''select id, from_id, to_id, text, time from messages where
                (to_id=:userid)
                order by id desc limit :ofset,:count''', {
                'count': count, 'ofset': ofset, 'userid': user_id})
        else:
            tmp.vars['cursor'].execute(
                '''select id, from_id, to_id, text, time from messages where
                    (to_id=:this and from_id=:userid)
                    or
                    (to_id=:userid and from_id=:this)
                    order by id desc limit :ofset,:count''', {
                    'this': user[0], 'count': count, 'ofset': ofset, 'userid': user_id})
        
        raw_messages = tmp.vars['cursor'].fetchall()
        if len(raw_messages) < 1:
            return {'count': len(raw_messages), 'items': raw_messages}
        for raw_message in raw_messages:
            messages.append({'id': raw_message[0],
                             'from_id': raw_message[1],
                             'to_id': raw_message[2],
                             'text': secure(raw_message[3]),
                             'time': raw_message[4]})

        return {'count': len(messages), 'items': messages}
    else:
        return ss


def get(args):
    ss = utils.notempty(args, ['accesstoken', 'id'])
    if ss == True:
        token = args['accesstoken']
        id = args['id']
        if False == utils.validr(token, utils.TOKENR):
            return utils.error(400, "'accesstoken' is invalid")
        if False == utils.validr(id, utils.IDR):
            return utils.error(400, "'id' is invalid")
        user = account._gett(token, 1)
        msg = _get(id)
        print(msg)
        if msg['from_id'] != user[0] and msg['to_id'] != user[0]:
            return utils.error(403, 'Access denided for this action')
        if 'error' in user:
            return user
        return msg
    else:
        return ss


def _get(id):
    tmp.vars['cursor'].execute(
        '''select from_id, text, to_id from messages where id = ?''', (id,))
    msg = tmp.vars['cursor'].fetchall()
    if not msg or len(msg) != 1:
        return utils.error(400, "This message not exists")
    msg = msg[0]
    return {'from_id': msg[0], 'to_id': msg[2], 'text': secure(msg[1])}


def edit(args):
    ss = utils.notempty(args, ['accesstoken', 'id'])
    if ss == True:
        token = args['accesstoken']
        user = account._gett(token, 1)
        if 'error' in user:
            return user
        message = _get(args['id'])
        if "error" in message:
            return message
        text = args.get("text", message['text'])
        if user[0] == message['from_id']:
            tmp.vars['cursor'].execute('''UPDATE messages
                SET text = :text
                WHERE id = :id''',

                    {
                        'id': args['id'],
                        'text': text,
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
        user = account._gett(token, 1)
        if 'error' in user:
            return user
        message = _get(args['id'])
        if "error" in message:
            return message
        if user[0] == message['from_id']:
            tmp.vars['cursor'].execute('''DELETE FROM messages
                WHERE id = :id''',

                    {
                        'id': args['id']
                    }
                    )
            tmp.vars['db'].commit()
            return {'state': 'ok'}
    else:
        return ss

