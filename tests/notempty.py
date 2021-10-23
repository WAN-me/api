def notempty(args,need):
    empty=[]
    for key in need:
        name = args.get(key)
        if not name or name=='':
            empty.append(key)
    if len(empty)==0:
        return True
    else: return empty

theare = {'name':"testname",'password':"testpassword",'email':"testemail"}
need = ['name','password','email']

print(notempty(theare,need))

