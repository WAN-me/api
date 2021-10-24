import testkenel as tk

def get(token,id):
    s = tk.session(token)
    return (s.rget('message.get',{'id':id}))

def send(token,text,to_id):
    s = tk.session(token)
    return (s.rget('message.send',{'text':text,'to_id':to_id}))

def chats(token):
    s = tk.session(token)
    return (s.rget('message.chats',{}))