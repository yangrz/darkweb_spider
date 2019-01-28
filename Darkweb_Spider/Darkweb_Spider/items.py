# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DarkwebSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field
    title = scrapy.Field()
    content_url = scrapy.Field()
    content = scrapy.Field()
    plate = scrapy.Field()
    publish_time = scrapy.Field()
    update_time = scrapy.Field()
    price = scrapy.Field()
    volume = scrapy.Field()
    visits = scrapy.Field()
    pass

    # def get_insert_sql(self):
    #     insert_sql = '''REPLACE INTO DeepWeb_phpbbs (title, content_url, content, plate, publish_time, update_time)
    #     VALUES ('{}', '{}', '{}', '{}', '{}', '{}')'''.format(self['title'],self['content_url'],self['content'],
    #                                                           self['plate'],self['publish_time'],self['update_time'])
    #
    #     return insert_sql

