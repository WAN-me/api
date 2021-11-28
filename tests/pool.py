import testkenel as tk

def get(token,count=10):
    s = tk.session(token)
    return (s.rget('pool.get',{'count':count}))

def read(token,id=10):
    s = tk.session(token)
    return (s.rget('pool.read',{'id':id}))