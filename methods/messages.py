import json
from methods import utils, db, poll, chats, account, users, groups, online
from methods.utils import secure

def send(args):
    ss = utils.notempty(args, ['accesstoken', 'text', 'to_id'])
    if ss == True:
        token = args['accesstoken']
        text = args['text']
        to_id = args['to_id']
        user = account._gett(token, 1)
        if 'error' in user:
            return user
        online._set(user[0])
        if False == utils.validr(str(to_id), utils.IDR):
            return utils.error(400, "'to_id' is invalid")

        to_id = int(to_id)
        text = secure(text)
        
        return _send(user[0], to_id, text)
    else:
        return ss


def _send(from_id, to_id, text):
    db.exec('''insert into messages (from_id, to_id, text)
    values (?,?,?)''', (from_id, to_id, text,))


    msg_id = db.exec('''select seq from sqlite_sequence where name="messages"''')[0][0]

    if to_id < 0: # сообщение в чат
        group = groups._get(-to_id)
        if 'error' in group:
            return group
        group['users'].append(-1)
        if not from_id in group['users']: # пользователь не учатсник чата
            return utils.error(403,"access denided for this chat")

        db.exec(f'''insert into poll (type, user_id, object_id, object)
            select 1, user_id, {msg_id}, ?
            from members
            where object_id = {-to_id} and not user_id = {from_id};''', (json.dumps({'id': msg_id,
                'from_id': from_id,
                'to_id': to_id,
                'text': text}),))

        db.exec(f'''insert into chats (id, user_id, name)
            select {to_id}, user_id, ?
            from members
            where object_id = {-to_id} and 
        not user_id in (
            select user_id from chats 
            where id={to_id});''', (group['name'], ))

    else:
        poll._set(1,
                to_id,
                msg_id,
                {'id': msg_id,
                'from_id': from_id,
                'to_id': to_id,
                'text': text})  # добавляем события
        chats._set(to_id, from_id, users._get(from_id)['name'])
    poll._set(2,
                from_id,
                msg_id,
                {'id': msg_id,
                'from_id': from_id,
                'to_id': to_id,
                'text': text}) # Сообщение доставленно

    return {'id': msg_id}


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
        online._set(user[0])
        messages = []
        raw_messages = []
        if int(user_id) < 0: # this chat!
            raw_messages = db.exec(
            '''select id, from_id, to_id, text, time from messages where
                (to_id=:userid)
                order by id desc limit :ofset,:count''', {
                'count': count, 'ofset': ofset, 'userid': user_id})
        else:
            raw_messages = db.exec(
                '''select id, from_id, to_id, text, time from messages where
                    (to_id=:this and from_id=:userid)
                    or
                    (to_id=:userid and from_id=:this)
                    order by id desc limit :ofset,:count''', {
                    'this': user[0], 'count': count, 'ofset': ofset, 'userid': user_id})
        
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
        if 'error' in user:
            return user
        online._set(user[0])
        msg = _get(id)
        if msg['from_id'] != user[0] and msg['to_id'] != user[0]:
            return utils.error(403, 'Access denided for this action')
        return msg
    else:
        return ss


def _get(id):
    msg = db.exec(
        '''select from_id, text, to_id from messages where id = ?''', (id,))
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
        online._set(user[0])
        message = _get(args['id'])
        if "error" in message:
            return message
        text = args.get("text", message['text'])
        if user[0] == message['from_id']:
            db.exec('''UPDATE messages
                SET text = :text
                WHERE id = :id''',

                    {
                        'id': args['id'],
                        'text': text,
                    }
                    )
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
            db.exec('''DELETE FROM messages
                WHERE id = :id''',

                    {
                        'id': args['id']
                    }
                    )
            return {'state': 'ok'}
    else:
        return ss

