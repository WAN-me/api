from methods import db

def _set(user_id):
    db.exec('''update users set online = strftime('%s', 'now', '+2 minutes') where user_id == ?;''', (user_id,))