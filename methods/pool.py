from methods import utils,db,users
import json

def _set(type:int,user,id:int=None,object:dict=None):
    db.exec('''insert into pool(type,object_id,user_id,object) 
            values(?,?,?,?)''',(type,id,user,json.dumps(object),))

def get(args):
    ss = utils.notempty(args,['accesstoken'])
    if ss == True: 
        token = args['accesstoken']
        count = args.get('count',10)
        user = users._gett(token,1)
        if 'error' in user:
            return user 
        updates = []
        raw_updates = db.exec('''select type,object_id,time,object,id from pool where user_id=:userId and readed=0
                order by id limit :count''',
                {'userId':user[0],'count':count})
        if len(raw_updates)<1:
            return {'count':len(raw_updates),'items':raw_updates}
        for raw_update in raw_updates:
            updates.append({'event_id':raw_update[4],'type':raw_update[0],'object_id':raw_update[1],'time':raw_update[2],'object':json.loads(raw_update[3])})

        return {'count':len(updates),'items':updates}
    else:
        return ss

def read(args):
    ss = utils.notempty(args,['accesstoken'])
    if ss == True: 
        token = args['accesstoken']
        id = args.get('id',9223372036854775807)
        user = users._gett(token,1)
        if 'error' in user:
            return user 
        db.exec('''update pool set readed = 1 where user_id=:user_id and id<:id''',
                {'user_id':user[0],'id':id})
        return {'state':'ok'}
    else:
        return ss
