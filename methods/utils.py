import hashlib
import re

TOKENR=r"^([a-f]|[0-9]){1,}$"
IDR=r"^\d{0,}$"
NAMER=r"^[\w'\-,.][^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,30}$"

def allowedPhoto(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ["png","jpg","jped","gif","bmp",]

def secure(text:str):
    return text.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

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
    else: return error(400,f"this keys is empty: {empty}")

def thisonly(input,symbols):
    for s in input:
        if not s in symbols:
            return False
    return True

def valid(content,allow):
    for c in content:
        if not c in allow:
            return False
    return True

def validr(content,reg):
    if len(re.findall(reg, str(content))) > 0:
        return True
    else:
        return False

def error(code,text):
    return {'error':{"code":code,"text":text}}
