from api import api

@api.errorhandler(404)
def pageNotFound(error):
    return api.methods.utils.error(404,'page not found'),404
@api.errorhandler(500)
def ISE(error):
    return api.methods.utils.error(500,'internal server error'),500
@api.route('/', methods=['GET',"POST"])
def m():
    return {'message':'welcome to the WAN-m api!'}

