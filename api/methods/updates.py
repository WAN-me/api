from methods import utils,db
def set(type,user,id=None):
    db.exec('''insert into updates(type,object_id,user_id) 
            values(?,?,?)''',(type,id,user,))

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
            raw_updates = db.exec('''select type,object_id,time from updates where user_id=:userId 
                    order by id desc limit :count,:ofset''',
                    {'userId':thisuser[0],'count':count,'ofset':ofset})
            for i in len(raw_updates):
                updates.append({'type':i[0],'object_id':i[1],'time':i[2]})

            return updates
    else:
        return ss
