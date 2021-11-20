from methods import utils
import cfg
import requests
version="v2.1"

def universal(args,method):
    v = args.get('v',version)
    return requests.get(f"https://kinopoiskapiunofficial.tech/api/{v}/{method}",params=args,
    headers={'X-API-KEY':cfg.apiKeyForKinopoisk}).content