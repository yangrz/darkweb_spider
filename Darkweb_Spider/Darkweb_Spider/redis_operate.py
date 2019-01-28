# -*- coding: utf-8 -*-
import redis
import time
from scrapy import log
from Darkweb_Spider.redis_util import RedisCollection
import logging

class RedisOpera:

    def __init__(self, stat):
        logging.info('init redis %s connection!' %stat)
        self.r = redis.Redis(host='127.0.0.1', port=6379, db=0)

    def insert(self, values):
        # print self.r.keys('*')
        collection_name = RedisCollection(values).getCollectionName()
        self.r.sadd(collection_name, values)

    def query(self, values):
        collection_name = RedisCollection(values).getCollectionName()
        return self.r.sismember(collection_name, values)