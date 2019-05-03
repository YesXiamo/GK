#!/usr/bin/env
# -*-coding:utf8;-*-
#__author__ = 'Mac'

from flask import Flask, redirect
from flask_cors import CORS
from flask_compress import Compress
from spiapi import api, supcon
from init import *
import logging


supcon()

app = Flask(__name__, static_folder='./', template_folder='./')
Compress(app)
CORS(app)
LOGGER = logging.getLogger('gunicorn.error')


@app.route('/')
def index():
    return redirect('/api/')


if __name__ == '__main__':
    app.register_blueprint(api, url_prefix='/api')
    app.run(host='127.0.0.1', port=port, debug=False, threaded=True)


if __name__ != '__main__':
    app.register_blueprint(api, url_prefix='/api')
