# -*- coding: utf-8 -*-
from scrapy.mail import MailSender
from scrapy.utils.project import get_project_settings
from Darkweb_Spider.items import DarkwebSpiderItem

class sendMail():

    def __init__(self):
        self.settings = get_project_settings()
        self.mailer = MailSender.from_settings(self.settings)
        self.item = DarkwebSpiderItem()

    def send(self):
        item = self.item
        title = item['title']
        plate = item['plate']
        content_url = item['content_url']
        content = item['content']
        publish_time = item['publish_time']
        update_time = item['update_time']
        self.mailer.send(to = self.settings['MAIL_LIST'],
                         subject="【暗网威胁情报监控平台告警】",
                         body="您好！\
                                   暗网交易市场有您所定制的相关威胁告警信息，请确认！\
                                   %s \
                                   %s \
                                   %s \
                                   %s \
                                   %s \
                                   %s"
                              %(title,plate,content_url,content,publish_time,update_time)
                              )
    def __send__(self):

        print(self.mailer.mailfrom)
        self.mailer.send(to = self.settings['MAIL_LIST'],
                         subject="【暗网威胁情报监控平台告警】",
                         body = 'xxxxxxxxx')

