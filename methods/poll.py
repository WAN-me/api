from methods import utils, db, account
import json
import time
import cfg
def _set(event_type: int, user, id: int = None, object: dict = None):
    print(id)
    db.exec('''insert into poll(type, object_id, user_id, object)
            values(?,?,?,?)''', (event_type, id, user, json.dumps(object),))


def get(args):
    ss = utils.notempty(args, ['accesstoken'])
    if ss == True:
        token = args['accesstoken']
        timeout = int(args.get("timeout", 10))
        count = args.get('count', 10)
        id = args.get('id', None)
        user = account._gett(token, 1)
        if 'error' in user:
            return user
        updates = []
        if id is None:
            res = db.exec(
                '''select id from poll where user_id=:user_id
                    order by id DESC limit :count''', {
                    'user_id': user[0], 'count': 1})
            if len(res) == 0:
                return {"id": 0}
            return {"id":res[0][0]}
        else:
            while timeout > 0:
                
                raw_updates = db.exec(
                    '''select type, object_id, time, object, id from poll where user_id=:userId and id>:id
                        order by id limit :count''', {
                        'userId': user[0], 'count': count, 'id':id})
                if len(raw_updates) > 0:
                    for raw_update in raw_updates:
                        updates.append({'event_id': raw_update[4],
                                        'type': raw_update[0],
                                        'object_id': raw_update[1],
                                        'time': raw_update[2],
                                        'object': json.loads(raw_update[3])})

                    return {'count': len(updates), 'items': updates}
                timeout -= cfg.poll_step
                time.sleep(cfg.poll_step)
            return {'count': 0, 'items': []}
    else:
        return ss

