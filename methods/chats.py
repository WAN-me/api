from methods import utils, db, users
import json


def _set(user, id: int, name="dialog"):
    db.exec('''insert into chats(id,user_id,name)
            values(?,?,?)''', (id, user, name))


def get(args):
    ss = utils.notempty(args, ['accesstoken'])
    if ss == True:
        token = args['accesstoken']
        count = args.get('count', 10)
        ofset = args.get('ofset', 0)
        user = users._gett(token, 1)
        if 'error' in user:
            return user
        chats = []
        raw_chats = db.exec(
            '''select DISTINCT id, name from chats where user_id=:userId
                    order by id desc limit :ofset,:count''', {
                'userId': user[0], 'count': count, 'ofset': ofset})
        if len(raw_chats) < 1:
            return {'count': len(raw_chats), 'items': raw_chats}
        for raw_chat in raw_chats:
            chats.append({'id': raw_chat[0], "name": raw_chat[1]})

        return {'count': len(chats), 'items': chats}
    else:
        return ss
