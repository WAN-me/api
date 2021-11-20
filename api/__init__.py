from flask import Flask
from flask_cors import CORS
api = Flask(__name__)
api.config['UPLOAD_FOLDER'] = '/var/www/cloud/upload'
api.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
CORS(api)
from api import routes