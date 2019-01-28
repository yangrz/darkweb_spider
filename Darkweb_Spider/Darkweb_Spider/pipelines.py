# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
from Darkweb_Spider.dbhelpler import DBHelper
from Darkweb_Spider.redis_operate import RedisOpera

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

class DarkwebSpiderPipeline(object):
    # 连接数据库
    def __init__(self):
        self.db = DBHelper()

    def process_item(self, item, spider):
        # 插入数据库
        self.db.insert(item)
        return item

# class InsertRedis(object):
#     def __init__(self):
#         self.Redis = RedisOpera('insert')
#
#     def process_item(self, item, spider):
#         self.Redis.write(item['content_url'])
#         return item

    # item_list = []
    #
    # # def __init__(self , conn):
    # #     self.conn = conn
    #
    # @classmethod
    # def open_spider(self, settings):
    #     print("开启数据库")
    #     self.conn = pymysql.connect(host = settings['MYSQL_HOST'], user = settings['MYSQL_USER'],
    #                                 password = settings['MYSQL_PASSWD'], database = settings['MYSQL_NAME'],
    #                                 charset = settings['charset'])
    #     self.cursor = self.conn.cursor()
    #     # return cls(conn)
    #
    # # 批量插入mysql数据库
    # def bulk_insert_to_mysql(self, bulkdata):
    #     try:
    #         print("the length of the data-------", len(self.companylist))
    #         sql = '''REPLACE INTO DeepWeb_phpbbs (title, content_url, content, plate, publish_time, update_time)
    #         VALUES (%s, %s, %s, %s, %s, %s)'''
    #         self.cursor.executemany(sql, bulkdata)
    #         self.conn.commit()
    #     except:
    #         self.conn.rollback()
    #
    # def process_item(self, item):
    #     self.item_list.append([item['title'], item['content'], item['content_url'], item['plate'], item['publish_time'],
    #                            item['update_time']])
    #     if len(self.item_list) == 1000:
    #         self.bulk_insert_to_mysql(self.item_list)
    #         # 清空缓冲区
    #         del self.item_list[:]
    #     return item
    #
    # def close_spider(self):
    #     print("closing spider,last commit", len(self.item_list))
    #     self.bulk_insert_to_mysql(self.item_list)
    #     self.conn.commit()
    #     self.cursor.close()
    #     self.conn.close()
