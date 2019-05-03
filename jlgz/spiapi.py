#!/usr/bin/env
# -*-coding:utf8;-*-
#__author__ = 'Mac'

from flask import Blueprint, render_template, request, jsonify
from spider import *
from init import app_name, title
from model.Model import get_record
import logging
import os


api = Blueprint('api', __name__, template_folder='./api', static_folder='./api/static', static_url_path='/static')
LOGGER = logging.getLogger('gunicorn.error')


@api.route('/title', methods=['POST'])
def api_get_title():
    return jsonify({'RetCode': 0, 'title': title})


@api.route('/data', methods=['POST'])
def api_get_data():
    r_data = check_cache()
    return r_data


@api.route('/echo', methods=['GET', 'POST'])
def api_echo():
    tmp = data_in(request)
    uid = tmp.get('uid', 0)
    return uid


@api.route('/quit', methods=['POST'])
def api_quit():
    os._exit(0)
    return "quit"


@api.route('/')
def index():
    return render_template('index.html')


def get_names(raw):
    names = []
    for i in raw:
        for x in loads(i).keys():
            if x != "time":
                names.append(x)
    return names


def opt_data(raw, names):
    res = []
    for i in raw:
        x = loads(i[0])
        data = []
        for name in names:
            data.append(x.get(name, 0))
        res.append({
            't': x.get('time'),
            'd': data,
        })
    return res


dic_data = {}
expire_time = 30
def check_cache():
    global dic_data
    if len(dic_data) < 1 or time.time() - dic_data.get("last_time",0) > expire_time:
        dic_data = {"last_time": time.time()}
        raw = get_record()
        raw_extract = extract_data(raw)
        names = get_names(raw_extract[0])
        res = opt_data(raw_extract, names)
        r_data = jsonify({'RetCode': 0, 'data': res, 'names': names})
        dic_data["data"] = r_data
    else:
        r_data = dic_data["data"]
    return r_data


MAX = 1000
def extract_data(raw):
    raw_len = len(raw)
    if raw_len < MAX:
        return raw
    else:
        raw_extract = []
        interval = raw_len / MAX
        for i in range(MAX + 1):
            j = int(interval * i + 0.5)
            j = raw_len-1 if j > raw_len-1 else j
            raw_extract.append(raw[j])
        return raw_extract


if __name__ == "__main__":
    t0 = time.time()
