import requests
import json
class session():
    def __init__(self,token) -> None:
        self.token = token
    
    def rget(self,method,params):
        params['method'] = method
        params['accesstoken'] = self.token
        r = requests.get("https://api.wan-group.ru/method",params)

        return json.loads(r.content.decode('utf-8'))