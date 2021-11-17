from methods import utils,db

def get(args):
    id = args['id']
    val = db.exec('''select id,text from vul where id = :id ''',{'id':id})
    return {'id':val[0],'text':val[1]}

def set(args):
    text = args['text']
    db.exec('''insert into vul (text)
        values (?)''',(text,))
    valid = db.exec('''select seq from sqlite_sequence where name="vul"''')[0][0]
    return {'id':valid}