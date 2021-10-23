import testkenel as tk

def get(token,count=10,ofset=0):
    s = tk.session(token)
    return (s.rget('updates.get',{'count':count,'ofset':ofset}))