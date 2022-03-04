from methods import utils, users, db, groups, pool, account
from methods.utils import secure


def _get(id):
    ach = (
        db.exec(
            '''select id, name, description, image, groupid from achivs where id = :id ''', {
                'id': id}))
    if len(ach) == 0:
        return utils.error(404, "This achivment not exists")
    else:
        ach = ach[0]
        return {
            'id': ach[0], 'name': secure(
                ach[1]), 'description': secure(
                ach[2]), 'image': ach[3], 'group': ach[4]}


def _new(name, description, image, group):
    db.exec(f'''insert into achivs (name, description, groupid, image)
        values (:name, :desc, :group, :image)''', {'name': name, 'desc': description, 'group': group, 'image': image})
    achvieid = db.exec(
        '''select seq from sqlite_sequence where name="achivs"''')[0][0]
    return {'id': achvieid}


def get(args):
    ss = utils.notempty(args, ['accesstoken', 'id'])
    if ss == True:
        token = args['accesstoken']
        id = args['id']
        if False == utils.validr(token, utils.TOKENR):
            return utils.error(400, "'accesstoken' is invalid")
        user = account._gett(token, 1)
        if 'error' in user:
            return user
        if False == utils.validr(id, utils.IDR):
            return utils.error(400, "'id' is invalid")
        achive = _get(id)
        if 'error' in achive:
            return achive

    else:
        return ss


def new(args):
    ss = utils.notempty(args, ['accesstoken', 'name', 'group'])
    if ss == True:
        token = args['accesstoken']
        group = args['group']
        name = args['name']
        description = args.get('description', "")
        image = args.get(
            'image',
            "https://cloud.wan-group.ru/upload/achive.png")
        if False == utils.validr(token, utils.TOKENR):
            return utils.error(400, "'accesstoken' is invalid")
        user = account._gett(token, 1)
        if 'error' in user:
            return user
        if False == utils.validr(id, utils.IDR):
            return utils.error(400, "'id' is invalid")
        group = groups._get(group)
        if 'error' in group:
            return group
        if user[0] in group['admins'] or user[0] == group['owner_id']:
            achive = _new(name, description, image, group['id'])
            return achive
        else:
            return utils.error(403, "You are not admin for this group")

    else:
        return ss


def give(args):
    ss = utils.notempty(args, ['accesstoken', 'id', 'user_id'])
    if ss == True:
        token = args['accesstoken']
        userid = args['user_id']
        ach = _get(args['id'])
        if False == utils.validr(token, utils.TOKENR):
            return utils.error(400, "'accesstoken' is invalid")
        thisuser = account._gett(token, 1)
        if 'error' in thisuser:
            return thisuser
        if 'error' in ach:
            return ach
        group = groups._get(ach['group'])
        if 'error' in group:
            return group
        if userid in group['users']:
            if thisuser[0] in group['admins'] or thisuser[0] == group['owner_id']:
                pool._set(4, userid, group['id'], ach)
                return {'state': 'ok'}
            else:
                return utils.error(403, "You are not admin for this group")
        else:
            return utils.error(404, "This user not exists")

    else:
        return ss
