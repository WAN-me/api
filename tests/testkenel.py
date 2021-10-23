import requests
import json
class session():
    def __init__(self,token) -> None:
        self.token = token
    
    def rget(self,method,params):
        params['method'] = method
        params['accesstoken'] = self.token
        r = requests.get("http://127.0.0.1:5000/method",params)
        try:
            return json.loads(r.content.decode('utf-8'))
        except:
            print(r.content)