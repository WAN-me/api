from methods import utils,db,updates,chats,users
def send(args):
    ss = utils.notempty(args,['accesstoken','text','to_id'])
    if ss == True: 
        token = args['accesstoken']
        text = args['text']
        toId = int(args['to_id'])
        thisuser = users._gett(token)
        if 'error' in thisuser:
            return thisuser 
        db.exec('''insert into messages (from_id,to_id,text)
        values (?,?,?)''',(thisuser[0],toId,text,))
        msgid = db.exec('''select seq from sqlite_sequence where name="messages"''')[0][0]
        updates.set(1,toId,msgid,{'id':msgid,'from_id':thisuser[0],'to_id':toId,'text':text})
        updates.set(2,thisuser[0],msgid,{'id':msgid,'from_id':thisuser[0],'to_id':toId,'text':text})
        chats._set(thisuser[0],toId)
        chats._set(toId,thisuser[0])
        return {'id':msgid}
    else:
        return ss

def gethistory(args):
    ss = utils.notempty(args,['accesstoken','user_id'])
    if ss == True: 
        token = args['accesstoken']
        user_id = args['user_id']
        count = args.get('count',20)
        ofset = args.get('ofset',0)
        thisuser = users._gett(token)
        if 'error' in thisuser:
            return thisuser 
        messages = []
        raw_messages = db.exec('''select id,from_id,to_id,text,time from messages where 
                (to_id=:this and from_id=:userid)
                or
                (to_id=:userid and from_id=:this)
                order by id desc limit :ofset,:count''',
                {'this':thisuser[0],
                'count':count,
                'ofset':ofset,
                'userid':user_id})
        if len(raw_messages)<1:
            return {'count':len(raw_messages),'items':raw_messages}
        for i in raw_messages:
            messages.append({'id':i[0],'from_id':i[1],'to_id':i[2],'text':i[3],'time':i[4]})

        return {'count':len(messages),'items':messages}
    else:
        return ss

def get(args):
    ss = utils.notempty(args,['accesstoken','id'])
    if ss == True: 
        token = args['accesstoken']
        id = args['id']
        thisuser = users._gett(token)
        if 'error' in thisuser:
            return thisuser 
        msg = db.exec('''select from_id,text,to_id from messages where id = ?''',(id,))
        if not msg or len(msg)!=1:
            return utils.error(400,"this message not exists")
        msg = msg[0]
        if msg[0] != thisuser[0] and msg[2] != thisuser[0]:
            return utils.error(403,'access denided for this action')
        return {'from_id':msg[0],'to_id':msg[2],'text':msg[1]}
    else:
        return ss

