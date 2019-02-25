#coding=utf-8

import requests
from bs4 import BeautifulSoup
from requests import exceptions
from scrapy.utils.project import get_project_settings
import logging
import json


logger = logging.getLogger(__name__)
origin_url = 'http://deepmix2z2ayzi46.onion/'
login_form = 'http://deepmix2z2ayzi46.onion/ucp.php?mode=login&sid='

def get_session():
    session = requests.session()
    session.proxies['http'] = 'xxx.xxx.xxx.xxx:8118'
    session.proxies['https'] = 'xxx.xxx.xxx.xxx:8118'
    return session

def get_CookieSid(username, passwd):
    # print('[*] 登录中......')
    logging.info('[*] 登录中......')
    headers = {
               'Host':'deepmix2z2ayzi46.onion',
               'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Encoding':'gzip, deflate',
               'Referer': 'http://deepmix2z2ayzi46.onion/index.php',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Connection':'keep-alive',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0'}

    session = get_session()
    try:
        #绕过meta头refresh属性定时跳转反爬机制
        front_res = session.get(url='http://deepmix2z2ayzi46.onion',
                                headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0'},
                                timeout=20)
        res = session.get(url='http://deepmix2z2ayzi46.onion/index.php',
                      headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0',
                               'Referer':'http://deepmix2z2ayzi46.onion'},timeout=20)
        soup = BeautifulSoup(res.text,'lxml')
        list = soup.find_all(name='input', type='hidden')
        begin = int(list[0]['value'].index('='))+1
        end = begin + 32
        sid = list[0]['value'][begin:end]
        data = {'username': username, 'password': passwd, 'login': '登录', 'redirect': './index.php?sid='+sid}
        login_redirect_url = login_form + sid
        r = session.post(url = login_redirect_url, headers = headers, data=data,
                         timeout=30, verify=False, allow_redirects=False)

    except exceptions.Timeout as e:
        # print('[*] 连接超时!')
        logging.error('[*] 连接超时!')
        return

    if r.status_code in {301,302}:
        location = r.headers['Location']
        __b__ = location.index('sid') + 4
        _sid = location[__b__:]
        # print('[*] 登录成功!')
        logging.info('[*] 登录成功!')
        return json.dumps(session.cookies.get_dict()) , _sid
    else:
        # print('[*] 登录失败！')
        logging.error('[*] 登录失败!')
        return

def get_value():
    __value__ = []
    settings = get_project_settings()
    Accounts = settings['ACCOUNTS']
    for accounts in Accounts:
        print(accounts)
        cookie,sid = get_CookieSid(accounts , 'xxxxxxxx')
        __i__= {'cookie':cookie,'sid':sid}
        print(__i__)
        __value__.append(__i__)
    return __value__

__l__ = get_value()
logging.info('Finished to get cookies.')
