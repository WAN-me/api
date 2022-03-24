from methods import utils, db, account
import json
import time
import tmp

def _set(type: int, user, id: int = None, object: dict = None):
    tmp.vars['cursor'].execute('''insert into poll(type, object_id, user_id, object)
            values(?,?,?,?)''', (type, id, user, json.dumps(object),))
    tmp.vars['db'].commit()


def get(args):
    ss = utils.notempty(args, ['accesstoken'])
    if ss == True:
        token = args['accesstoken']
        timeout = args.get("timeout", 10)
        count = args.get('count', 10)
        user = account._gett(token, 1)
        if 'error' in user:
            return user
        updates = []
        while timeout > 0:
            tmp.vars['cursor'].execute(
                '''select type, object_id, time, object, id from poll where user_id=:userId and readed=0
                    order by id limit :count''', {
                    'userId': user[0], 'count': count})
            raw_updates = tmp.vars['cursor'].fetchall()
            if len(raw_updates) > 0:
                for raw_update in raw_updates:
                    updates.append({'event_id': raw_update[4],
                                    'type': raw_update[0],
                                    'object_id': raw_update[1],
                                    'time': raw_update[2],
                                    'object': json.loads(raw_update[3])})

                return {'count': len(updates), 'items': updates}
            timeout -= 0.5
            time.sleep(0.5)
        return {'count': 0, 'items': []}
    else:
        return ss


def read(args):
    ss = utils.notempty(args, ['accesstoken'])
    if ss == True:
        token = args['accesstoken']
        id = args.get('id', 9223372036854775807) # Число - максимальное интовское значение в бд
        user = account._gett(token, 1)
        if 'error' in user:
            return user
        tmp.vars['cursor'].execute(
            '''update poll set readed = 1 where user_id=:user_id and id<:id''', {
                'user_id': user[0], 'id': id})
        tmp.vars['db'].commit()
        return {'state': 'ok'}
    else:
        return ss
