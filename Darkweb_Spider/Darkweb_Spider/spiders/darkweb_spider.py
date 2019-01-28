# -*- coding: utf-8 -*-

import scrapy
import re

from bs4 import BeautifulSoup
from Darkweb_Spider.items import DarkwebSpiderItem
from Darkweb_Spider.redis_operate import RedisOpera
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import *
from scrapy import log

class darkweb_spider(scrapy.Spider):
    name = 'darkweb_spider'

    def __init__(self):
        settings = get_project_settings()  # 获取settings配置数据
        self.afterlogin_headers = settings['AFTERLOGIN_HEADERS']
        self.target_url = settings['TARGET_URL']
        self.plate_map = settings['PLATE_MAP']

        self.InsertRedis = RedisOpera('insert')
        self.QueryRedis = RedisOpera('query')

    def start_requests(self):
        log.msg('登录成功',log.INFO)
        for plate_item in self.plate_map:
            log.msg('进入 %s' %plate_item['plate_name'],log.INFO)
            #spider.logger.info('进入  ' + plate_item['plate_name'])
            plate_url = plate_item['plate_url']
            yield scrapy.Request(url=plate_url, method='GET', headers=self.afterlogin_headers,
                                 meta={'plate': plate_item['plate_name']}, callback=self.into_plate, dont_filter=True)

    # 进入分类论坛
    def into_plate(self, response):
        log.msg('解析分类论坛页面: %s' %response.url,log.INFO)
        soup = BeautifulSoup(response.text, 'lxml')
        page_list = soup.find_all(name='button', attrs={'class': 'page_b1'})
        page_count = int(page_list[-1].get_text())
        if page_count > 5:
            page_count = 5
        for page in range(page_count):
            plate_page_url = response.url + '&page_y1=' + str(page+1)
            yield scrapy.Request(url=plate_page_url, method='GET', headers=self.afterlogin_headers,
                                 meta={'plate': response.meta['plate']},
                                 callback=self.parse_page, dont_filter=True)

    # 按分类论坛页面解析
    def parse_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        table = soup.find_all(name='table', attrs={'class': 'm_area_a'})
        tr_list = table[0].find_all('tr')
        for tr_item in tr_list[3:-2:2]:
            td_list = tr_item.find_all('td')
            a_list = td_list[4].find_all('a')
            # 标题
            title = a_list[0].get_text()
            href = a_list[0]['href']
            # 访问链接
            content_url = self.target_url + href[1:].replace('../', '')
            # 访问量
            visits = td_list[-3].get_text()

            # 进行url去重
            if self.QueryRedis.query(content_url):
                raise IgnoreRequest("IgnoreRequest : %s" % content_url)
            else:
                self.InsertRedis.insert(content_url)

            yield scrapy.Request(url = content_url, method='GET', headers=self.afterlogin_headers,
                                 meta={'plate': response.meta['plate'], 'title': title, 'content_url': content_url,
                                       'visits': visits},
                                 callback=self.parse, dont_filter=True)

    # 解析帖子内容
    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        #交易价格
        table = soup.find_all(name = 'table', attrs = {'class':'v_table_1'})
        tr_list = table[0].find_all('tr')
        td_list_price = tr_list[4].find_all('td')
        price_list = re.findall(r'\d+\.?\d*', td_list_price[3].get_text())
        price = price_list[0]
        #成交数量
        td_list_volume = tr_list[6].find_all('td')
        volume_list = re.findall(r'\d+', td_list_volume[3].get_text())
        volume = volume_list[0]
        #帖子内容
        content_list = soup.find_all(name='div', attrs={'class': 'content'})
        if len(content_list):
            content = content_list[0].get_text()
        else:
            content = ''
        #发布时间
        publish_time_list = soup.find_all(name='span', attrs={'class': 'responsive-hide'})
        if len(publish_time_list):
            origin_publish_time = publish_time_list[0].next_sibling
            ptr_list = [x for x in filter(str.isdigit, origin_publish_time)]
            pt_str = "".join(ptr_list)
            y = pt_str[:4]
            d = pt_str[-6:-4]
            if len(pt_str) == 12:
                m = pt_str[4:6]
            else:
                m = '0' + pt_str[4]
            publish_time = y + '-' + m + '-' + d
        else:
            publish_time = ''
        item = DarkwebSpiderItem()
        item['title'] = response.meta['title']
        item['plate'] = response.meta['plate']
        item['content_url'] = response.meta['content_url']
        item['content'] = content
        item['price'] = price
        item['volume'] = volume
        item['visits'] = response.meta['visits']
        item['publish_time'] = publish_time
        yield item











