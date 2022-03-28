from methods import utils, db, account
import tmp


def _set(user, id: int, name="dialog"):
    tmp.vars['cursor'].execute('''insert OR IGNORE into chats(id, user_id, name)
            values(?,?,?)''', (id, user, name))
    tmp.vars['db'].commit()


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
        tmp.vars['cursor'].execute('''select DISTINCT id, name from chats where user_id=:user_id
                    order by id desc limit :ofset,:count''', {
                'user_id': user[0], 'count': count, 'ofset': ofset})
        raw_chats = tmp.vars['cursor'].fetchall()
            
        if len(raw_chats) < 1:
            return {'count': len(raw_chats), 'items': raw_chats}
        for raw_chat in raw_chats:
            chats.append({'id': raw_chat[0], "name": raw_chat[1]})

        return {'count': len(chats), 'items': chats}
    else:
        return ss
