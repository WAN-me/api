from methods import utils,db,messages
import json
def set(user,id:int):
    db.exec('''insert into chats(id,user_id) 
            values(?,?)''',(id,user,))

def get(args):
    ss = utils.notempty(args,['accesstoken'])
    if ss == True: 
        token = args['accesstoken']
        count = args.get('count',10)
        ofset = args.get('ofset',0)
        thisuser = (db.exec(f'''select id from users where token = ? ''',(token,)))
        if not thisuser or len(thisuser)!=1:
            return utils.error(400,"'accesstoken' is invalid")
        else:
            thisuser = thisuser[0]
            chats = []
            raw_chats = db.exec('''select DISTINCT id from chats where user_id=:userId 
                    order by id desc limit :ofset,:count''',
                    {'userId':thisuser[0],'count':count,'ofset':ofset})
            if len(raw_chats)<1:
                return {'count':len(raw_chats),'items':raw_chats}
            for i in raw_chats:
                chats.append({'id':i[0]})

            return {'count':len(chats),'items':chats}
    else:
        return ss
