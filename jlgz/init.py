#!/usr/bin/env
# -*-coding:utf8;-*-
#__author__ = 'Mac'
from utility import *
from random import randint
import os
import socket

#项目名字
app_name = '时尚ya销量数据监控'
title = '时尚ya销量数据监控'

#db文件，sqlite依赖这个
db_name = 'jlgz'


reg_url = 'http://127.0.0.1:808/api/'


def port_is_used(port, ip='127.0.0.1'):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        s.shutdown(2)
        return True
    except:
        return False


def init_port():
    p = randint(618, 6180)
    while True:
        if not port_is_used(p):
            break
        p = randint(618, 6180)
    return p


def reg(name, p1, p2):
    sess = Session()
    data = {'app': name, 'port': p1, 'path': p2}
    resp = sess.post(url=reg_url+'reg', data=data, timeout=5)
    int(resp.text)

port = init_port()
reg(app_name,  port, os.path.abspath(__file__))


@async
def heart_beat():
    while True:
        sess = Session()
        data = {'app': app_name}
        try:
            resp = sess.post(url=reg_url+'upd', data=data, timeout=5)
            if resp.text != "ok":
                reg()
        except:
            pass
        time.sleep(5)
heart_beat()
