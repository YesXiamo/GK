#!/usr/bin/env
# -*-coding:utf8;-*-
#__author__ = 'Mac'

from functools import wraps
from threading import Thread, Lock, RLock
from json import dumps, loads
from sys import argv
import configparser
import datetime
import time
import re
from requests import Session


def async(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        thr = Thread(target=func, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


def u_esc(x: str, code='utf-8') ->str:
    """
    编码字符串
    :param x:
    :param code:
    :return:
    """
    return x.encode(code).decode('unicode_escape')


def infp(file, mode='r', not_startswith='', not_endswith='', out2scr=True, code='utf8') ->list:
    """
    读取文件，返回list
    :param file: 文件名字
    :param mode: 读取mode
    :param not_startswith: 忽略字符串开头的行
    :param not_endswith: 忽略字符串结尾的行
    :param out2scr: 是否print读取文件的信息
    :param code: 文件编码
    :return:
    """
    res = []
    if out2scr:
        print('读取{}'.format(file))

    try:
        with open(file, mode=mode, encoding=code) as fp:
            for line in (x.strip() for x in fp):
                if not line:
                    continue
                if not_startswith or not_startswith:
                    if line.startswith(not_startswith) or line.endswith(not_startswith):
                        continue
                res.append(line)
    except IOError as err:
        print('文件错误：{}'.format(file, str(err)))
    return res


def outfp(source: (list or tuple or set or str or dict), file: str, mode='a', out2scr=True, code='utf8'):
    """
    输出到文件，.jpg/.png输出为二进制文件
    :param source: 根据不同类型有不同输出方式
    :param file: 文件名字
    :param mode: a->追加模式，w->覆盖模式
    :param out2scr: 是否print写入文件的信息
    :param code: 文件编码
    :return:
    """
    if '.jpg' in file or 'png' in file:
        with open(file, 'wb') as fp:
            fp.write(source)

    with open(file, mode=mode, encoding=code) as fp:
        if isinstance(source, (list, tuple, set)):
            for item in source:
                fp.write('{}\n'.format(item))
        elif isinstance(source, str):
            fp.write('{}\n'.format(source))
        elif isinstance(source, dict):
            for k, v in source.items():
                fp.write('{}:{}\n'.format(k, v))

    if out2scr:
        print('{}已输出'.format(file))


def str_time(mode=0) ->(str or list):
    """
    返回字符串格式的时间
    :param mode: mode为4则返回list
    :return:
    """
    rule = {
        0: str(datetime.datetime.now())[:-7],
        1: str(datetime.datetime.now())[11:-7],
        2: str(datetime.datetime.now())[:11],
        3: str(datetime.datetime.now())[:11].replace('-', ''),
        4: str(datetime.datetime.now())[:11].split('-')
    }
    return rule[mode if mode in rule else 0]


def read_ini(app, args, ini='api.ini') ->list:
    """
    从ini文件获取参数变量，缺失参数返回False
    :param app: section
    :param args: 字段
    :param ini: ini文件
    :return: 参数变量数组
    """
    res = []
    conf = configparser.ConfigParser()
    conf.read(ini)
    for i in args:
        try:
            x = conf.get(app, i)
        except:
            x = False
        res.append(x)
    return res


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


if __name__ == "__main__":
    pass