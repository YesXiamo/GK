#!/usr/bin/env
# -*-coding:utf8;-*-
#__author__ = 'Mac'

from utility import *
from model.Model import add_record


@async
def supcon():
    while True:
        try:
            get_data()
        except Exception as e:
            print(e)
            time.sleep(30)


def get_data():
    tmp = {'time': str_time()}
    exe_spider(tmp)
    add_record(tmp)
    time.sleep(30)
    return tmp


def exe_spider(tmp):
    spider(url1, tmp)


#以下是爬虫，自行修改
cookies = {
    'access_token': '21_G6TAuDrBwewCSMqA3KWARwUfx3qFKQMyVaFvh81C6p83dPSw1f0v8TdxeAUA--qyU4CjuehrGLbgZaY5_weaPQTBLO2Qgey_rqhA9Ssxxhc',
    'openid': 'oKv-o1IwYUmnWrqpbTqluwCtdgiQ',
}
headers = {'User-Agent': ' Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1) QQBrowser/6.0'}
url1 = 'http://journal.trends.com.cn/'


def spider(url, tmp):
    """
    爬虫业务
    :param url: 目标地址
    :param tmp: 结果按  人名字:数字  存tmp，注意后面要int成数字
    :return:
    """
    sess = Session()
    resp = sess.post(url=url, cookies=cookies, allow_redirects=False, timeout=5)
    r = resp.text

    temp = re.findall('精灵公主的真爱检验标准</p><div\sclass="pm"><span\sclass="salecount">销量: \d+', r)[-1]
    tmp['精灵公主的真爱检验标准'] = re.findall('\d+', temp)[-1]
    temp = re.findall('class="title">如何把一只妖精驯养成你的女友</p><div\sclass="pm"><span\sclass="salecount">销量:\s\d+',r)[-1]
    tmp['略略略'] = re.findall('\d+', temp)[-1]


if __name__ == '__main__':
    data = {'time': str_time()}
    spider(url1, data)
    print(data)
