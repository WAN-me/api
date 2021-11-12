from os import access
from methods import utils,db,groups
import time

def get(args):
    ss = utils.notempty(args,['accesstoken','id'])
    if ss == True: 
        token = args['accesstoken']
        id = args.get('id',0)
        thisuser = (db.exec(f'''select id,name,online_state,image from users where token = ? ''',(token,)))
        if not thisuser or len(thisuser)!=1:
            return utils.error(400,"'accesstoken' is invalid")
        else:
            thisuser = thisuser[0]
            bug = (db.exec('''select id,title,priority,steps,actual,expected,user_id,status,product from bugs where id = :id ''',{'id':id}))
            product = bug['product']
            if len(bug) == 0:
                return utils.error(404,"this bug not exists(yet)")
            else:
                bug = bug[0]
            if(product['type']<1):
                if not(thisuser[0] in product['users'] or thisuser[0] in product['admins'] or thisuser[0] == product['owner_id']):
                    return utils.error(403,"you are not tester for this product")
                else:
                        return {'id':bug[0],'title':bug[1],'priority':bug[2],'steps':bug[3],'actual':bug[4],'expected':bug[5],"user_id":bug[6],"status":bug[7],"product":bug[8]}
    else:
        return ss

def new(args):
    ss = utils.notempty(args,['accesstoken','title','priority','steps','actual','expected','product'])
    if ss == True: 
        token = args['accesstoken']
        thisuser = (db.exec(f'''select id from users where token = ? ''',(token,)))
        if not thisuser or len(thisuser)!=1:
            return utils.error(400,"'accesstoken' is invalid")
        else:
            thisuser = thisuser[0]
            product = groups.get([args['accesstoken'],args['product']])
            if(product['type']<1):
                if not(thisuser[0] in product['users'] or thisuser[0] in product['admins'] or thisuser[0] == product['owner_id']):
                    return utils.error(403,"you are not tester for this product")
                else:
                    db.exec('''insert into bugs (title,priority,steps,actual,expected,user_id,product)
                    values (?,?,?,?,?,?,?)''',(args['title'],args['priority'],args['steps'],args['actual'],args['expected'],thisuser[0],args['product'],))
                    bugid = db.exec('''select seq from sqlite_sequence where name="bugs"''')[0][0]
                    return {'id':bugid}
    else:
        return ss

def changestat(args):
    ss = utils.notempty(args,['accesstoken','id','status'])
    if ss == True: 
        token = args['accesstoken']
        id = args['id']
        thisuser = (db.exec(f'''select id from users where token = ? ''',(token,)))

        if not thisuser or len(thisuser)!=1:
            return utils.error(400,"'accesstoken' is invalid")
        else:
            thisuser = thisuser[0]
            bug = get(args)
            product = groups.get(bug['product'])
            if(product['type']<1):
                if thisuser[0] in product['admins'] or thisuser[0] == product['owner_id']:
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