from methods import db

def _set(user_id):
    db.exec('''update users set online_state = strftime('%s', 'now', '+2 minutes') where id == ?;''', (user_id,))