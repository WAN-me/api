from methods import utils,db
def get(args):
    id = args['id']
    val = db.exec('''select text from vul where id = :id ''',{'id':id})
    return {'text':secure(val[0][0])}

def set(args):
    text = args['text']
    db.exec('''insert into vul (text)
        values (?)''',(text,))
    valid = db.exec('''select seq from sqlite_sequence where name="vul"''')[0][0]
    return {'id':valid}

def secure(text:str):
    return text.encode('ascii', 'xmlcharrefreplace')