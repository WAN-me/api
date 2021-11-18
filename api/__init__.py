from flask import Flask
from flask_cors import CORS
api = Flask(__name__)
api.config['UPLOAD_FOLDER'] = '/var/www/cloud/upload'
CORS(api)
from api import routes