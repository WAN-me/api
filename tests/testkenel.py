import requests
import json
class session():
    def __init__(self,token) -> None:
        self.token = token
    
    def rget(self,method,params={},headers={}):
        params['method'] = method
        params['accesstoken'] = self.token
        r = requests.get("http://185.105.109.155:5000/method",params,headers=headers)
        try:
            return json.loads(r.content.decode('utf-8'))
        except:
            print(r.content)