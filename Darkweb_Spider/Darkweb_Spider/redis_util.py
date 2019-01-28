# -*- coding: utf-8 -*-
import re
from scrapy.utils.project import get_project_settings
from scrapy import log

class RedisCollection(object):

    def __init__(self,OneUrl):
        self.collectionname = OneUrl

    def getCollectionName(self):
        # name = None
        if self.IndexAllUrls() is not None:
            name = self.IndexAllUrls()
        else:
            name = 'UnknownUrl'
        # log.msg("the collections name is %s"(name),log.INFO)
        return name

    def IndexAllUrls(self):
        settings = get_project_settings()
        domain_list = settings['DOMAIN']
        result = None
        for str in domain_list:
            if re.findall(str,self.collectionname):
                result = str
                break
        return result