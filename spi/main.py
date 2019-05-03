#!/usr/bin/env
# -*-coding:utf8;-*-
#__author__ = 'Mac'

from flask import Flask
from flask_cors import CORS
from flask_compress import Compress
from spi import api, ck
import logging


app = Flask(__name__, static_folder='./', template_folder='./')
Compress(app)
CORS(app)
LOGGER = logging.getLogger('gunicorn.error')


if __name__ == '__main__':
    # export FLASK_ENV=development
    app.register_blueprint(api, url_prefix='/api')

    host = '0.0.0.0' if ck() else '127.0.0.1'
    app.run(host=host, port=808, debug=False, threaded=True)


if __name__ != '__main__':
    app.register_blueprint(api, url_prefix='/api')
