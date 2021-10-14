import requests,time
def anymethods():
    while True:
        print(requests.get(f'http://127.0.0.1:5000/{input("page>>> ")}').content.decode('utf-8')+"\n\n")

def userget():
    now = time.time()
    for t in range(700):
        D =requests.get('http://127.0.0.1:5000/user?accesstoken=testokentipohesdsfdfs')
    print(time.time()-now)
def useradd():
    now = time.time()
    for t in range(700):
        D =requests.get(f'http://127.0.0.1:5000/reg?name={t}')
    print(time.time()-now)
anymethods()














