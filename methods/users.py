from methods.utils import secure
from methods import utils, db, account


def get(args):
    ss = utils.notempty(args, ['accesstoken'])
    if ss == True:
        token = args['accesstoken']
        res = account._gett(token, cursor=args['cursor'])
        id = args.get('id', res[0])
        return res if 'error' in res else _get(id, args['cursor'])
    else:
        return ss


def _get(id, cursor):
    cursor.execute(
            '''select id, name, online_state, image, verifi from users where id = :id ''', {
                'id': id})
    user = cursor.fetchall()
    if len(user) == 0:
        return utils.error(404, "This user not exists")
    else:
        user = user[0]
        return {
            'id': user[0],
            'name': secure(
                user[1]),
            'online_state': user[2],
            'image': user[3],
            'verifi': user[4]}
