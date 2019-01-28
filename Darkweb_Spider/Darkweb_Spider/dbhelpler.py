import pymysql
from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings  #导入setings配置
import datetime
import logging


class DBHelper():
    '''这个类也是读取settings中的配置，自行修改代码进行操作'''

    def __init__(self):
        settings = get_project_settings()  #获取settings配置，设置需要的信息

        dbparams = dict(
            host=settings['MYSQL_HOST'],  #读取settings中的配置
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWD'],
            database=settings['MYSQL_NAME'],
            charset=settings['CHARSET'],  #编码要加上，否则可能出现中文乱码问题
        )
        #**表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self.dbpool = dbpool

    def connect(self):
        return self.dbpool

    #创建数据库
    def insert(self, item):
        sql = '''REPLACE INTO DarkWeb_Spider (title, content_url, content, plate, publish_time, update_time, price, 
        volume, visits) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        #调用插入的方法
        query = self.dbpool.runInteraction(self._conditional_insert, sql, item)
        #调用异常处理方法
        query.addErrback(self._handle_error)

        return item

    #写入数据库中
    def _conditional_insert(self, tx, sql, item):
        item['update_time'] = datetime.datetime.now().strftime("%Y-%m-%d")
        params = (item["title"], item['content_url'], item['content'], item['plate'],
                  item['publish_time'], item['update_time'], item['price'], item['volume'], item['visits'])
        tx.execute(sql, params)

    #错误处理方法

    def _handle_error(self, failue):
        logging.WARN('--------------database operation exception!!-----------------')
        logging.WARN(failue)