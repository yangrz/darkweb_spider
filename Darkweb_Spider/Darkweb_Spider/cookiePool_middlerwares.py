# -*- coding: utf-8 -*-

import random

from w3lib.url import safe_url_string
from six.moves.urllib.parse import urljoin

from scrapy.exceptions import IgnoreRequest
from Darkweb_Spider.spiders import darkweb_spider


class MyAutoProxyDownloaderMiddleware(object):

    def __init__(self, settings):
        self.proxy_status = settings.get('PROXY_STATUS', [302, 403])
        # See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html?highlight=proxy#module-scrapy.downloadermiddlewares.httpproxy
        self.proxy_config = settings.get('PROXY_CONFIG', 'http://username:password@some_proxy_server:port')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            settings=crawler.settings
        )

        # See /site-packages/scrapy/downloadermiddlewares/redirect.py

    def process_response(self, request, response, spider):
        ds = darkweb_spider()

        if (request.meta.get('dont_redirect', False) or
                response.status in getattr(spider, 'handle_httpstatus_list', []) or
                response.status in request.meta.get('handle_httpstatus_list', []) or
                request.meta.get('handle_httpstatus_all', False)):
            return response

        if response.status in self.proxy_status:
            if 'Location' in response.headers:
                location = safe_url_string(response.headers['location'])
                redirected_url = urljoin(request.url, location)
            else:
                redirected_url = ''

            # AutoProxy for first time
            if not request.meta.get('auto_proxy'):
                request.meta.update({'auto_proxy': True, 'proxy': self.proxy_config})
                new_request = request.replace(meta=request.meta, dont_filter=True)
                new_request.priority = request.priority + 2

                spider.log('Will AutoProxy for <{} {}> {}'.format(
                    response.status, request.url, redirected_url))
                return new_request

            # IgnoreRequest for second time
            else:
                spider.logger.warn('Ignoring response <{} {}>: HTTP status code still in {} after AutoProxy'.format(
                    response.status, request.url, self.proxy_status))
                raise IgnoreRequest

        return response
