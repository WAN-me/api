from methods import utils,db,messages
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
        thisuser = (db.exec(f'''select id from users where token = ? ''',(token,)))
        if not thisuser or len(thisuser)!=1:
            return utils.error(2,"'accesstoken' is invalid")
        else:
            thisuser = thisuser[0]
            updates = []
            raw_updates = db.exec('''select type,object_id,time,object from updates where user_id=:userId 
                    order by id desc limit :ofset,:count''',
                    {'userId':thisuser[0],'count':count,'ofset':ofset})
            if len(raw_updates)<1:
                return {'count':len(raw_updates),'items':raw_updates}
            for i in raw_updates:
                updates.append({'type':i[0],'object_id':i[1],'time':i[2],'object':json.loads(i[3])})

            return {'count':len(updates),'items':updates}
    else:
        return ss
