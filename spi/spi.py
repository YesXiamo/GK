#!/usr/bin/env
# -*-coding:utf8;-*-
#__author__ = 'Mac'

from flask import Blueprint, request, jsonify, abort, render_template
from threading import Lock, Thread
from sys import argv
from json import loads
from functools import wraps
from requests import Session
import socket
import logging
import time


api = Blueprint('api', __name__, template_folder='./dist', static_folder='./dist', static_url_path='/static')
LOGGER = logging.getLogger('gunicorn.error')


def async(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        thr = Thread(target=func, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


@api.route('/', methods=['GET'])
def index():
    return render_template('index.html')

    tmp = data_in(request)
    res = call_service_get(data=tmp)
    if not res:
        abort(404)
        return
    return res


@api.route('/call', methods=['POST'])
def api_call():
    tmp = data_in(request)
    return jsonify(call_service_post(tmp))


services = {}
service_url = "http://127.0.0.1:"
slock = Lock()


@api.route('/get', methods=['POST'])
def get_service():
    return jsonify({'RetCode': 0, 'app': list(services.keys())})


@api.route('/reg', methods=['POST'])
def reg_service():
    tmp = data_in(request)
    app = tmp.get('app')
    if app not in services:
        with slock:
            services[app] = {
                'port': tmp.get('port'),
                'active': time.time(),
                'path': tmp.get('path')
            }
        return "0"

    return "duped app"


@api.route('/upd', methods=['POST'])
def upd_service():
    tmp = data_in(request)
    app = tmp.get('app')
    if app not in services:
        return "invalid"

    with slock:
        services[app]['active'] = time.time()

    return "ok"


@api.route('/status', methods=['POST'])
def status_service():
    return jsonify({'RetCode': 0, 'app': services})


@api.route('/quit', methods=['POST'])
def quit_service():
    tmp = data_in(request)
    uid = int(tmp.get('uid', 0))
    tmp['api'] = 'quit'
    if uid == 19940618:
        return jsonify(call_service_post(tmp))

    return {'RetCode': -300}


def call_service_url(data):
    app = data.get('app')
    if not app:
        return app

    s = services.get(app)
    if not s:
        return s

    port = s.get('port')
    if not port:
        return port

    return "{}{}/api/".format(service_url, port)


def call_service_get(data):
    url = call_service_url(data)
    if not url:
        return url

    r = data.get('api')
    if r:
        url += r

    sess = Session()
    try:
        resp = sess.get(url, data=data, timeout=5)
        return resp.text
    except Exception as e:
        print(e, url, data)
        return None


def call_service_post(data):
    url = call_service_url(data)
    if not url:
        return {'RetCode': -100}

    r = data.get('api')
    if r:
        url += r

    sess = Session()
    try:
        resp = sess.post(url, data=data, timeout=5)
        return resp.json()
    except Exception as e:
        print(e, url, data)
        return {'RetCode': -200}


@async
def check_service():
    while True:
        t = time.time()
        with slock:
            inactive = []
            for k, v in services.items():
                if abs(v.get('active') - t) > 10:
                    inactive.append(k)

            for i in inactive:
                services.pop(i)
        time.sleep(5)
check_service()


def data_in(req) -> dict:
    data = {}
    po = req.values
    if len(po) > 0:
        data = po.to_dict()
    else:
        try:
            data = loads(req.data.decode())
        except Exception as e:
            print(e)
    # print_data(data)
    return data


def print_data(data):
    if not data:
        print('no data')
        return

    for k, v in data.items():
        if k == 'token':
            continue
        print('{}: {}'.format(k, v))


def ck():
    try:
        return argv[1] == '1'
    except:
        return False


if __name__ == "__main__":
    pass
