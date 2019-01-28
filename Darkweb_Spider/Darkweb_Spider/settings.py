# -*- coding: utf-8 -*-

# Scrapy settings for Darkweb_Spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Darkweb_Spider'

SPIDER_MODULES = ['Darkweb_Spider.spiders']
NEWSPIDER_MODULE = 'Darkweb_Spider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Darkweb_Spider (+http://www.yourdomain.com)'

# Obey robots.txt rules
#ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
#CONCURRENT_REQUESTS = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 4

# Disable cookies (enabled by default)
#COOKIES_ENABLED = True
#COOKIES_DEBUG = True
# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'Darkweb_Spider.middlewares.CookiesMiddleware1': 601,
#
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'Darkweb_Spider.middlewares.DarkwebSpiderDownloaderMiddleware': 543,
    'Darkweb_Spider.middlewares.CookiesMiddleware': 600,
    'Darkweb_Spider.middlewares.RedirectMiddleware': 599,

}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'Darkweb_Spider.pipelines.DarkwebSpiderPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'root'
MYSQL_NAME = 'threat_demo'
CHARSET = 'utf8'

TARGET_URL = 'http://deepmix2z2ayzi46.onion/'
LOGIN_URL = 'http://deepmix2z2ayzi46.onion/ucp.php?mode=login&sid='
DOMAIN = ['deepmix2z2ayzi46.onion']

EXCEPTION_STATUS = [302,403,500]

#DEPTH_PRIORITY = 1
#RETRY_ENABLED = False

ACCOUNTS = ['Threattest','Threattest1','Threattest2','Threattest3',
            'Threattest4','Threattest5','Threattest6','Threattest7']

AFTERLOGIN_HEADERS = {
        'Host': 'deepmix2z2ayzi46.onion',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'http://deepmix2z2ayzi46.onion/index.php',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Update-Insecure-Requests': '1',
        'Pragma':'no-cache',
        'Cache-Control':'no-cache'
    }

PLATE_MAP = [
        {'plate': 'discussion',
         'plate_url': 'http://deepmix2z2ayzi46.onion/pay/user_area.php?q_ea_id=10001',
         'plate_name': '数据情报'},
        {'plate': 'discussion',
         'plate_url': 'http://deepmix2z2ayzi46.onion/pay/user_area.php?q_ea_id=10002',
         'plate_name': '虚拟资源'},
        {'plate': 'discussion',
         'plate_url': 'http://deepmix2z2ayzi46.onion/pay/user_area.php?q_ea_id=10003',
         'plate_name': '技术教学'},
        {'plate': 'discussion',
         'plate_url': 'http://deepmix2z2ayzi46.onion/pay/user_area.php?q_ea_id=10010',
         'plate_name': '其他类别'},
        {'plate': 'discussion',
         'plate_url': 'http://deepmix2z2ayzi46.onion/pay/user_area.php?q_ea_id=10005',
         'plate_name': '基础知识'},
        {'plate': 'discussion',
         'plate_url': 'http://deepmix2z2ayzi46.onion/pay/user_area.php?q_ea_id=10008',
         'plate_name': '卡料CVV'},
        {'plate': 'discussion',
         'plate_url': 'http://deepmix2z2ayzi46.onion/pay/user_area.php?q_ea_id=10009',
         'plate_name': '私人专拍'},
        {'plate': 'discussion',
         'plate_url': 'http://deepmix2z2ayzi46.onion/pay/user_area.php?q_ea_id=10007',
         'plate_name': '实体物品'}
    ]
