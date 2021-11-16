from methods import utils,db,messages,users
import json
def set(type:int,user,id:int=None,object:dict=None):
    db.exec('''insert into updates(type,object_id,user_id,object) 
            values(?,?,?,?)''',(type,id,user,json.dumps(object),))

def get(args):
    ss = utils.notempty(args,['accesstoken'])
    if ss == True: 
        token = args['accesstoken']
        count = args.get('count',10)
        ofset = args.get('ofset',0)
        thisuser = users._gett(token)
        if 'error' in thisuser:
            return thisuser 
        updates = []
        raw_updates = db.exec('''select type,object_id,time,object,id from updates where user_id=:userId 
                order by id desc limit :ofset,:count''',
                {'userId':thisuser[0],'count':count,'ofset':ofset})
        if len(raw_updates)<1:
            return {'count':len(raw_updates),'items':raw_updates}
        for i in raw_updates:
            updates.append({'event_id':i[3],'type':i[0],'object_id':i[1],'time':i[2],'object':json.loads(i[3])})

        return {'count':len(updates),'items':updates}
    else:
        return ss
