# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import MySQLdb

class LagouPipeline(object):
    def process_item(self, item, spider):
        return item

# class TextWriterPipeline:  # 写入文本
#
#     def open_spider(self, spider):
#         self.file = open('items.txt', 'w')
#
#     def close_spider(self, spider):
#         self.file.close()
#
#     def process_item(self, item, spider):
#         for k in ['job', 'company', 'money','place','required']:
#             value = item[k]
#             self.file.write('%s: %s\n\n' % (k, value)
#            # self.file.write('\n')
#         return item

class MysqlPipeline:  # 写入数据库

    @classmethod  # 实例化类，通过crawler引擎调用setting
    def from_crawler(cls, crawler):
        user = crawler.settings.get('USER')
        password = crawler.settings.get('PASSWORD')
        database = crawler.settings.get('DATABASE')
        charset = crawler.settings.get('CHARSET')
        dbtable = crawler.settings.get('DATABLE')
        host = crawler.settings.get('HOST')
        return cls(user, password, database, charset, dbtable, host)

    def __init__(self, user, password, database, charset, dbtable, host):
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.dbtable = dbtable
        self.host = host
    def open_spider(self, spider):
        self.conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password,database=self.database, charset=self.charset)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        sql = 'insert into 51job values ("%s","%s","%s","%s","%s")'
        data = (item['job'], item['place'], item['company'],item['money'],item['required'])
        self.cursor.execute(sql,args=data)
        return item
