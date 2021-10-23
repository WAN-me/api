from methods import utils,db,updates
def send(args):
    ss = utils.notempty(args,['accesstoken','text','to_id'])
    if ss == True: 
        token = args['accesstoken']
        text = args['text']
        toId = args['to_id']
        thisuser = (db.exec(f'''select id from users where token = ? ''',(token,)))
        if not thisuser or len(thisuser)!=1:
            return utils.error(2,"'accesstoken' is invalid")
        else:
            thisuser = thisuser[0]
            db.exec('''insert into messages (from_id,to_id,text)
            values (?,?,?)''',(thisuser[0],toId,text,))
            msgid = db.exec('''select seq from sqlite_sequence where name="messages"''')[0][0]
            updates.set(1,toId,msgid)
            updates.set(2,thisuser[0],msgid)
            return {'id':msgid}
    else:
        return ss

def get(args):
    ss = utils.notempty(args,['accesstoken','id'])
    if ss == True: 
        token = args['accesstoken']
        id = args['id']
        thisuser = (db.exec(f'''select id from users where token = ? ''',(token,)))
        if not thisuser or len(thisuser)!=1:
            return utils.error(2,"'accesstoken' is invalid")
        else:
            thisuserid = thisuser[0][0]
            msg = db.exec('''select from_id,text,to_id from messages where id = ?''',(id,))
            if not msg or len(msg)!=1:
                return utils.error(2,"'id' is invalid")
            msg = msg[0]
            if msg[0] != thisuserid and msg[2] != thisuserid:
                return utils.error(7,'access denided for this action')
            return {'from_id':msg[0],'to_id':msg[2],'text':msg[1]}
    else:
        return ss
