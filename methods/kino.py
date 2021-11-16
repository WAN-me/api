from methods import utils
import requests

def search(args):
    ss = utils.notempty(args,['query',"page"])
    if ss == True: 
        page = args.get('page',1)
        query = args['query']
        return requests.get("https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword",params={'keyword':query,'page':page},headers={'X-API-KEY':"66e57928-f821-4f05-8922-9828fa81aaca"}).content
    else:
        return ss
