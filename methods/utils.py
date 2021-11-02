import hashlib

def dohash(input):
    return hashlib.sha256(input.encode()).hexdigest()

def notempty(args,need):
    empty=[]
    for key in need:
        name = args.get(key)
        if not name or name=='':
            empty.append(key)
    if len(empty)==0:
        return True
    else: return 400,f"this keys is empty: {empty}"

def thisonly(input,symbols):
    for s in input:
        if not s in symbols:
            return False
    return True

def valid(content,type):
    if type == 'token':
        ...

def error(code,text):
    return {'error':{"code":code,"text":text}}
