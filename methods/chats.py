from methods import utils,db,messages,users
import json
def _set(user,id:int):
    db.exec('''insert into chats(id,user_id) 
            values(?,?)''',(id,user,))

def get(args):
    ss = utils.notempty(args,['accesstoken'])
    if ss == True: 
        token = args['accesstoken']
        count = args.get('count',10)
        ofset = args.get('ofset',0)
        thisuser = users._gett(token)
        print("consts init")
        if 'error' in thisuser:
            return thisuser 
        chats = []
        raw_chats = db.exec('''select DISTINCT id from chats where user_id=:userId 
                order by id desc limit :ofset,:count''',
                {'userId':thisuser[0],'count':count,'ofset':ofset})
        print("raw_chats init")
        if len(raw_chats)<1:
            return {'count':len(raw_chats),'items':raw_chats}
        for i in raw_chats:
            chats.append({'id':i[0]})

        return {'count':len(chats),'items':chats}
    else:
        return ss
