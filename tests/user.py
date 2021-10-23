import testkenel as tk

def auth(login,passw):
    s = tk.session("")
    return (s.rget('user.auth',{'login':login,'password':passw}))

def get(token):
    s = tk.session(token)
    return (s.rget('user.get',{}))

def delete(token):
    s = tk.session(token)
    return (s.rget('user.del',{}))

def reg(name,email,passw):
    s = tk.session("")
    return (s.rget('user.reg',{'name':name,'email':email,'password':passw}))