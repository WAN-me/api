from methods import utils, db, groups, account, poll
from methods.utils import secure
import tmp

def get(args: dict):
    ss = utils.notempty(args, ['accesstoken', 'id'])
    if ss == True:
        token = args['accesstoken']
        id = args.get('id', 0)
        user = account._gett(token, 1)
        if 'error' in user:
            return user
        bug = _get(id)
        if 'error' in bug:
            return bug
        product = groups._get(bug['product'])
        if "error" in product:
            return product
        if(product['type'] < 1):
            if user[0] in product['users']:
                return bug
            return utils.error(403, "You are not tester for this product")

    else:
        return ss


def _get(id):
    if False == utils.validr(id, utils.IDR):
        return utils.error(400, "'id' is invalid")
    tmp.vars['cursor'].execute('''select id, title, priority, steps, actual, expected, user_id, status, product from bugs where id = :id ''', {
                'id': id})
    bug = tmp.vars['cursor'].fetchall()
    if len(bug) == 0:
        return utils.error(404, "This bug not exists(yet)")
    else:
        bug = bug[0]
        product = groups._get(bug[8])
        if "error" in product:
            return product
    return {
        'id': bug[0], 'title': secure(
            bug[1]), 'priority': bug[2], 'steps': secure(
            bug[3]), 'actual': secure(
                bug[4]), 'expected': secure(
                    bug[5]), "user_id": bug[6], "status": bug[7], "product": bug[8]}


def new(args):
    ss = utils.notempty(args,
                        ['accesstoken',
                         'title',
                         'priority',
                         'steps',
                         'actual',
                         'expected',
                         'product'])
    if ss == True:
        token = args['accesstoken']
        user = account._gett(token, 1)
        if 'error' in user:
            return user
        product = groups._get(args['product'])
        if "error" in product:
            return product
        elif(product['type'] < 1):
            if not(user[0] in product['users'] or user[0]
                   in product['admins'] or user[0] == product['owner_id']):
                return utils.error(403, "you are not tester for this product")
            else:
                tmp.vars['cursor'].execute(
                    '''insert into bugs (title, priority, steps, actual, expected, user_id, product)
                values (?,?,?,?,?,?,?)''',
                    (args['title'],
                    args['priority'],
                    args['steps'],
                    args['actual'],
                    args['expected'],
                    user[0],
                    args['product'],
                     ))
                tmp.vars['db'].commit()
                tmp.vars['cursor'].execute('''select seq from sqlite_sequence where name="bugs"''')[0][0]
                bug_id = tmp.vars['cursor'].fetchall
                    
                return {'id': bug_id}
    else:
        return ss


def comment(args):
    ss = utils.notempty(args, ['accesstoken', 'id', ])
    if ss == True:
        token = args['accesstoken']
        user = account._gett(token, 1)
        if 'error' in user:
            return user
        text = args.get("text", "")
        bug = _get(id)
        product = groups._get(bug['product'])
        if "error" in product:
            return product
        elif(product['type'] < 1):
            if args.get("status", None) is not None:
                if user[0] in product['admins'] or user[0] == product['owner_id']:
                    tmp.vars['cursor'].execute(
                        '''insert into comments (from_id, post_id, text, status)
                        values (?,?,?,?)''', (user[0], args['id'], text, args["status"],))
                    tmp.vars['db'].commit()
                    tmp.vars['cursor'].execute('''select seq from sqlite_sequence where name="comments"''')
                    comment_id = tmp.vars['cursor'].fetchall()[0][0]
                    if not bug['user_id'] == user[0]:
                        poll._set(
                            3, bug['id'], bug['user_id'], {
                                'id': comment_id, 'from_id': user[0], 'text': text, 'extra': args["status"]})
                    return {"id": comment_id}
                elif user[0] in product['users'] and bug['user_id'] == user[0]:
                    if args['status'] in [5, 6, 11]:
                        tmp.vars['cursor'].execute(
                            '''insert into comments (from_id, post_id, text, status)
                        values (?,?,?,?)''', (user[0], args['id'], text, args["status"],))
                        tmp.vars['db'].commit
                        tmp.vars['cursor'].execute(
                            '''select seq from sqlite_sequence where name="comments"''')
                        comment_id = tmp.vars['cursor'].fetchall()[0][0]
                        if not bug['user_id'] == user[0]:
                            poll._set(3,
                                      bug['id'],
                                      bug['user_id'],
                                      {'id': comment_id,
                                          'from_id': user[0],
                                          'text': secure(text),
                                          'extra': args["status"]})
                        return {"id": comment_id}
                    else:
                        return utils.error(403, "You can't set this status")
                else:
                    return utils.error(
                        403, "You are havn't access to this bug")
            elif text != "":
                if user[0] in product['users']:
                    tmp.vars['cursor'].execute('''insert into comments (from_id, post_id, text)
                    values (?,?,?)''', (user[0], args['id'], text,))
                    tmp.vars['db'].commit
                    tmp.vars['cursor'].execute(
                        '''select seq from sqlite_sequence where name="comments"''')
                    comment_id = tmp.vars['cursor'].fetchall()[0][0]
                    if not bug['user_id'] == user[0]:
                        poll._set(
                            3, bug['id'], bug['user_id'], {
                                'id': comment_id, 'from_id': user[0], 'text': secure(text)})
                    return {"id": comment_id}
                else:
                    return utils.error(
                        403, "You are havn't access to this bug")
            else:
                return utils.notempty(args, ['text', 'status', ])
        else:
            return utils.error(404, "This is not product")
    else:
        return ss


def getcomments(args):
    ss = utils.notempty(args, ['accesstoken', 'id'])
    if ss == True:
        token = args['accesstoken']
        bug_id = args['id']
        user = account._gett(token, 1)
        if 'error' in user:
            return user
        bug = _get(id)
        if 'error' in bug:
            return bug
        product = groups._get(bug['product'])
        if "error" in product:
            return product
        elif(product['type'] < 1):
            if not(user[0] in product['users']):
                return utils.error(403, "You are not tester for this product")
            else:
                comments = []
                tmp.vars['cursor'].execute(
                    '''select text, from_id, id, etxra from comments where post_id=:id
                        order by id''', {
                        'id': bug_id, })
                raw_comments = tmp.vars['cursor'].fetchall()
                if len(raw_comments) < 1:
                    return {[]}
                for raw_comment in raw_comments:
                    comments.append(
                        {
                            'text': secure(
                                raw_comment[0]),
                            'from_id': raw_comment[1],
                            'id': raw_comment[2],
                            'status': raw_comment[3]})

                return {'count': len(comments), 'items': comments}
    else:
        return ss


def changestat(args):
    ss = utils.notempty(args, ['accesstoken', 'id', 'status'])
    if ss == True:
        token = args['accesstoken']
        id = args['id']
        user = account._gett(token, 1)
        if 'error' in user:
            return user
        bug = _get(id)
        if 'error' in bug:
            return bug
        product = groups._get(bug['product'])
        if "error" in product:
            return product
        elif(product['type'] < 1):
            if user[0] == product['owner_id']:
                tmp.vars['cursor'].execute('''UPDATE bugs
                SET status = :st
                WHERE id = :id''', {'id': id, 'st': args['status']})
                tmp.vars['db'].commit()
                return {'state': 'ok'}
            elif user[0] in product['users'] and bug['user_id'] == user[0]:
                if args['status'] in [5, 6, 11]:
                    tmp.vars['cursor'].execute('''UPDATE bugs
                    SET status = :st
                    WHERE id = :id''', {'id': id, 'st': args['status']})
                    tmp.vars['db'].commit()
                    return {'state': 'ok'}
                else:
                    return utils.error(403, "You can't set this status")
            else:
                return utils.error(403, "You are havn't access to this bug")
        else:
            return utils.error(404, "This is not product")
    else:
        return ss


def edit(args):
    ss = utils.notempty(args, ['accesstoken', 'id'])
    if ss == True:
        token = args['accesstoken']
        id = args['id']
        user = account._gett(token, 1)
        if 'error' in user:
            return user
        bug = _get(id)
        if 'error' in bug:
            return bug
        title = args.get("title", bug['title'])
        priority = args.get("priority", bug['priority'])
        steps = args.get("steps", bug['steps'])
        actual = args.get("actual", bug['actual'])
        expected = args.get("expected", bug['expected'])
        product = groups._get(bug['product'])
        if "error" in product:
            return product
        elif(product['type'] < 1):
            if user[0] in product['admins'] or user[0] == product['owner_id']:
                tmp.vars['cursor'].execute('''UPDATE bugs
                SET title = :title 
                ,priority = :priority 
                ,steps = :steps 
                ,actual = :actual 
                ,expected = :expected

                WHERE id = :id''',

                        {
                            'id': id,
                            'title': title,
                            'priority': priority,
                            'steps': steps,
                            'actual': actual,
                            'expected': expected
                        }
                        )
                tmp.vars['db'].commit()
                return {'state': 'ok'}
            elif user[0] in product['users'] and bug['user_id'] == user[0]:
                tmp.vars['cursor'].execute('''UPDATE bugs
                SET title = :title, 
                priority = :priority, 
                steps = :steps, 
                actual = :actual, 
                expected = :expected

                WHERE id = :id''',

                        {
                            'id': id,
                            'title': title,
                            'priority': priority,
                            'steps': steps,
                            'actual': actual,
                            'expected': expected
                        }
                        )
                tmp.vars['db'].commit()
                return {'state': 'ok'}
            else:
                return utils.error(403, "You are havn't access to this bug")
        else:
            return utils.error(404, "This is not product")
    else:
        return ss
