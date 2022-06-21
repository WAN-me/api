from methods import utils, db, account, online


def _set(user, id: int, name="dialog"):
    db.exec('''insert into chats(id, user_id, name)
            select :id,:user,:name
        WHERE NOT EXISTS(SELECT 1 FROM chats WHERE id = :id AND user_id = :user);''', {'id': id, 'user': user, 'name': name})


def get(args):
    ss = utils.notempty(args, ['accesstoken'])
    if ss == True:
        token = args['accesstoken']
        count = args.get('count', 10)
        ofset = args.get('ofset', 0)
        user = account._gett(token, 1)
        if 'error' in user:
            return user
        chats = []
        raw_chats = db.exec('''select DISTINCT id, name from chats where user_id=:user_id
                    order by id desc limit :ofset,:count''', {
                'user_id': user[0], 'count': count, 'ofset': ofset})
        online._set(user[0])
        
        if len(raw_chats) < 1:
            return {'count': len(raw_chats), 'items': raw_chats}
        for raw_chat in raw_chats:
            chats.append({'id': raw_chat[0], "name": raw_chat[1]})

        return {'count': len(chats), 'items': chats}
    else:
        return ss
