from os import access
from methods import utils,db,groups,users
import time

def get(args:dict):
    ss = utils.notempty(args,['accesstoken','id'])
    if ss == True: 
        token = args['accesstoken']
        id = args.get('id',0)
        thisuser = users._gett(token)
        if 'error' in thisuser:
            return thisuser 
        bug = _get(id)
        if 'error' in bug:
            return bug 
        product = groups._get(bug['product'])
        if "error" in product:
            return product
        if(product['type']<1):
            if thisuser[0] in product['users']:
                return bug
            return utils.error(403,"you are not tester for this product")
                    
                        
    else:
        return ss

def _get(id):
    bug = (db.exec('''select id,title,priority,steps,actual,expected,user_id,status,product from bugs where id = :id ''',{'id':id}))
    if len(bug) == 0:
        return utils.error(404,"this bug not exists(yet)")
    else:
        bug = bug[0]
        product = groups._get(bug[8])
        if "error" in product:
            return product
    return {'id':bug[0],'title':bug[1],'priority':bug[2],'steps':bug[3],'actual':bug[4],'expected':bug[5],"user_id":bug[6],"status":bug[7],"product":bug[8]}

def new(args):
    ss = utils.notempty(args,['accesstoken','title','priority','steps','actual','expected','product'])
    if ss == True: 
        token = args['accesstoken']
        thisuser = users._gett(token)
        if 'error' in thisuser:
            return thisuser 
        product = groups._get(args['product'])
        if "error" in product:
            return product
        elif(product['type']<1):
            if not(thisuser[0] in product['users'] or thisuser[0] in product['admins'] or thisuser[0] == product['owner_id']):
                return utils.error(403,"you are not tester for this product")
            else:
                db.exec('''insert into bugs (title,priority,steps,actual,expected,user_id,product)
                values (?,?,?,?,?,?,?)''',(args['title'],args['priority'],args['steps'],args['actual'],args['expected'],thisuser[0],args['product'],))
                bugid = db.exec('''select seq from sqlite_sequence where name="bugs"''')[0][0]
                return {'id':bugid}
    else:
        return ss

def comment(args):
    ss = utils.notempty(args,['accesstoken','id',])
    if ss == True:
        token = args['accesstoken']
        thisuser = users._gett(token)
        if 'error' in thisuser:
            return thisuser 
        text = args.get("text","")
        bug = get(args)
        product = groups._get(bug['product'])
        if "error" in product:
            return product
        elif(product['type']<1):
            if args.get("status",None) != None:
                if thisuser[0] in product['admins'] or thisuser[0] == product['owner_id']:
                    db.exec('''insert into comments (from_id,post_id,text,status)
                        values (?,?,?,?)''',(thisuser[0],args['id'],text,args["status"],))
                    comid = db.exec('''select seq from sqlite_sequence where name="comments"''')[0][0]
                    return {"id":comid}
                elif thisuser[0] in product['users'] and bug['user_id']==thisuser[0]:
                    if args['status'] in [5,6,11]:
                        db.exec('''insert into comments (from_id,post_id,text,status)
                        values (?,?,?,?)''',(thisuser[0],args['id'],text,args["status"],))
                        comid = db.exec('''select seq from sqlite_sequence where name="comments"''')[0][0]
                        return {"id":comid}
                    else: return utils.error(403,"you can't set this status")
                else: return utils.error(403,"you are havn't access to this bug")
            elif text != "":
                if thisuser[0] in product['users']:
                    db.exec('''insert into comments (from_id,post_id,text)
                    values (?,?,?)''',(thisuser[0],args['id'],text,))
                    comid = db.exec('''select seq from sqlite_sequence where name="comments"''')[0][0]
                    return {"id":comid}
                else: return utils.error(403,"you are havn't access to this bug")
            else:
                return utils.notempty(args,['text','status',])
        else: return utils.error(404,"this is not product")
    else:
        return ss

def getcomments(args):
    ss = utils.notempty(args,['accesstoken','id'])
    if ss == True: 
        token = args['accesstoken']
        bug_id = args['id']
        thisuser = users._gett(token)
        if 'error' in thisuser:
            return thisuser 
        bug = _get(id)
        if 'error' in bug:
            return bug 
        product = groups._get(bug['product'])
        if "error" in product:
            return product
        elif(product['type']<1):
            if not(thisuser[0] in product['users']):
                return utils.error(403,"you are not tester for this product")
            else:
                comments = []
                raw_comments = db.exec('''select text,from_id,id,etxra from updates where post_id=:id 
                        order by id''',
                        {'id':bug_id,})
                if len(raw_comments)<1:
                    return {[]}
                for i in raw_comments:
                    comments.append({'text':i[0],'from_id':i[1],'id':i[2],'status':i[3]})

                return {comments}
    else:
        return ss

def changestat(args):
    ss = utils.notempty(args,['accesstoken','id','status'])
    if ss == True: 
        token = args['accesstoken']
        id = args['id']
        thisuser = users._gett(token)
        if 'error' in thisuser:
            return thisuser 
        bug = _get(id)
        if 'error' in bug:
            return bug 
        product = groups._get(bug['product'])
        if "error" in product:
            return product
        elif(product['type']<1):
            if thisuser[0] == product['owner_id']:
                db.exec('''UPDATE bugs
                SET status = :st
                WHERE id = :id''',{'id':id,'st':args['status']})
                return {'state':'ok'}
            elif thisuser[0] in product['users'] and bug['user_id']==thisuser[0]:
                if args['status'] in [5,6,11]:
                    db.exec('''UPDATE bugs
                SET status = :st
                WHERE id = :id''',{'id':id,'st':args['status']})
                    return {'state':'ok'}
                else: return utils.error(403,"you can't set this status")
            else: return utils.error(403,"you are havn't access to this bug")
        else: return utils.error(404,"this is not product")
    else:
        return ss

def edit(args):
    ss = utils.notempty(args,['accesstoken','id'])
    if ss == True: 
        token = args['accesstoken']
        id = args['id']
        thisuser = users._gett(token)
        if 'error' in thisuser:
            return thisuser 
        bug = _get(id)
        if 'error' in bug:
            return bug 
        title = args.get("title",bug['title'])
        priority = args.get("priority",bug['priority'])
        steps = args.get("steps",bug['steps'])
        actual = args.get("actual",bug['actual'])
        expected = args.get("expected",bug['expected'])
        product = groups._get(bug['product'])
        if "error" in product:
            return product
        elif(product['type']<1):
            if thisuser[0] in product['admins'] or thisuser[0] == product['owner_id']:
                db.exec('''UPDATE bugs
                SET title = :title
                ,priority = :priority
                ,steps = :steps
                ,actual = :actual
                ,expected = :expected

                WHERE id = :id''',
                
                {
                    'id':id,
                    'title':title,
                    'priority':priority,
                    'steps':steps,
                    'actual':actual,
                    'expected':expected
                }
                )
                return {'state':'ok'}
            elif thisuser[0] in product['users'] and bug['user_id']==thisuser[0]:
                db.exec('''UPDATE bugs
                SET title = :title,
                priority = :priority,
                steps = :steps,
                actual = :actual,
                expected = :expected

                WHERE id = :id''',
                
                {
                    'id':id,
                    'title':title,
                    'priority':priority,
                    'steps':steps,
                    'actual':actual,
                    'expected':expected
                }
                )
                return {'state':'ok'}
            else: return utils.error(403,"you are havn't access to this bug")
        else: return utils.error(404,"this is not product")
    else:
        return ss