from methods import utils,db,messages,users
import json
def _set(type:int,user,id:int=None,object:dict=None):
    db.exec('''insert into pool(type,object_id,user_id,object) 
            values(?,?,?,?)''',(type,id,user,json.dumps(object),))

def get(args):
    ss = utils.notempty(args,['accesstoken'])
    if ss == True: 
        token = args['accesstoken']
        count = args.get('count',10)
        thisuser = users._gett(token)
        if 'error' in thisuser:
            return thisuser 
        updates = []
        raw_updates = db.exec('''select type,object_id,time,object,id from pool where user_id=:userId and readed=0
                order by id limit :count''',
                {'userId':thisuser[0],'count':count})
        if len(raw_updates)<1:
            return {'count':len(raw_updates),'items':raw_updates}
        for i in raw_updates:
            updates.append({'event_id':i[4],'type':i[0],'object_id':i[1],'time':i[2],'object':json.loads(i[3])})

        return {'count':len(updates),'items':updates}
    else:
        return ss

def read(args):
    ss = utils.notempty(args,['accesstoken','id'])
    if ss == True: 
        token = args['accesstoken']
        id = args['id']
        thisuser = users._gett(token)
        if 'error' in thisuser:
            return thisuser 
        db.exec('''update pool set readed = 1 where user_id=:userId and id<:id''',
                {'userId':thisuser[0],'id':id})
        return {'state':'ok'}
    else:
        return ss
