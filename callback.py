#!/usr/bin/python3
import cfg
import requests
def send(ip, event, args):
    if 'password' in args:
        args['password'] = "PASSWORD"
    
    if 'accesstoken' in args:
        args['accesstoken'] = "TOKEN"
    print(requests.post(cfg.callback_server, {'ip': ip, 'args':str(args), 'event':event}).text)


if __name__ == "__main__":
    import sbeaver
    server = sbeaver.Server(port=3030)
    @server.bind(r'.*')
    def bing(req: sbeaver.Request):
        print(req)
        args = req.data
        text = f"""
ip {args['ip']}
event {args['event']}
args\n {str(args['args'])}"""
        print(requests.get(f"https://api.telegram.org/bot{cfg.tg_token}/sendMessage?chat_id={cfg.tg_chat}", {"text":text}).text)
        return 200, 'ok'
    server.start()