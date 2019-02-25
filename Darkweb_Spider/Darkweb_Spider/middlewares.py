# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from Darkweb_Spider.get_cookie_sid import __l__
from w3lib.url import safe_url_string
from six.moves.urllib.parse import urljoin
from scrapy import log
from scrapy.exceptions import IgnoreRequest
from Darkweb_Spider.redis_operate import RedisOpera
from scrapy.exceptions import *
import json
import random

class DarkwebSpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class DarkwebSpiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        #spider.logger.info("DarkWebSpiderMiddleware process_request:requests=%s,spider=%s", request, spider)
        request.meta['proxy'] = 'http://xxx.xxx.xxx.xxx:8118'
        #spider.logger.info('request.meta%s', request.meta)
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        #return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

# class DuplicateRequest(object):
#     def __init__(self):
#         self.Redis = RedisOpera('query')
#
#     def process_request(self, request, spider):
#         if self.Redis.query(request.url):
#             raise IgnoreRequest("IgnoreRequest : %s" % request.url)
#         else:
#             return None


class CookiesMiddleware(object):

    def process_request(self, request, spider):
        __json__ = random.choice(__l__)
        request.cookies = json.loads(__json__['cookie'])
        if ('sid' in request.url) is True:
            begin = request.url.index('sid') + 4
            _old = request.url[begin:]
            request = request.replace(url = request.url.replace(_old , __json__['sid']),dont_filter=True)
            #spider.logger.info("requests=%s,spider=%s", request.url, spider)
            #print(request.cookies)
        print(request.cookies)
        spider.logger.info("requests=%s,spider=%s", request.url, spider)
        # else:
        #     request = request.replace(url=request.url + '&sid=' + __json__['sid'])
        #     spider.logger.info("requests=%s,spider=%s", request.url, spider)

class RedirectMiddleware(object):

    def __init__(self, settings):
        self.exception_status = settings['EXCEPTION_STATUS']

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            settings=crawler.settings
        )

    def process_response(self, request, response, spider):

        if (request.meta.get('dont_redirect', False) or
                response.status in getattr(spider, 'handle_httpstatus_list', []) or
                response.status in request.meta.get('handle_httpstatus_list', []) or
                request.meta.get('handle_httpstatus_all', False)):
            return response

        if response.status in self.exception_status:
            if 'Location' in response.headers:
                location = safe_url_string(response.headers['location'])
                redirected_url = urljoin(request.url, location)
            else:
                redirected_url = ''

            if not request.meta.get('retry'):
                request.meta.update({'retry': True})
                new_request = request.replace(meta=request.meta, dont_filter=True)
                new_request.priority = request.priority + 2

                spider.logger.info('Will Retry 302 Redirect for <{} {}> {}'.format(response.status, request.url, redirected_url))
                return new_request

        # IgnoreRequest for second time
            else:
                spider.logger.info('Ignoring response <{} {}>: HTTP status code still in {} after retry'.format(
                response.status, request.url, self.exception_status))
                raise IgnoreRequest

        return response
