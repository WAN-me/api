from methods import utils, db, account
import json


def _set(type: int, user, id: int = None, object: dict = None, args = None):
    args['cursor'].execute('''insert into pool(type, object_id, user_id, object)
            values(?,?,?,?)''', (type, id, user, json.dumps(object),))
    args['connection'].commit()


def get(args):
    ss = utils.notempty(args, ['accesstoken'])
    if ss == True:
        token = args['accesstoken']
        count = args.get('count', 10)
        user = account._gett(token, 1, cursor=args['cursor'])
        if 'error' in user:
            return user
        updates = []
        args['cursor'].execute(
            '''select type, object_id, time, object, id from pool where user_id=:userId and readed=0
                order by id limit :count''', {
                'userId': user[0], 'count': count})
        raw_updates = args['cursor'].fetchall()
        if len(raw_updates) < 1:
            return {'count': len(raw_updates), 'items': raw_updates}
        for raw_update in raw_updates:
            updates.append({'event_id': raw_update[4],
                            'type': raw_update[0],
                            'object_id': raw_update[1],
                            'time': raw_update[2],
                            'object': json.loads(raw_update[3])})

        return {'count': len(updates), 'items': updates}
    else:
        return ss


def read(args):
    ss = utils.notempty(args, ['accesstoken'])
    if ss == True:
        token = args['accesstoken']
        id = args.get('id', 9223372036854775807) # Почему именно это число!? что я курил?
        user = account._gett(token, 1, cursor=args['cursor'])
        if 'error' in user:
            return user
        args['cursor'].execute(
            '''update pool set readed = 1 where user_id=:user_id and id<:id''', {
                'user_id': user[0], 'id': id})
        args['connection'].commit()
        return {'state': 'ok'}
    else:
        return ss
