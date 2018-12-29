# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
from twisted.enterprise import adbapi
import pymysql
from pymysql import cursors


class BoleSpiderPipeline(object):
    def process_item(self, item, spider):
        return item

# class MysqlPipeline(object):
#     def __init__(self):
#         self.conn = pymysql.Connect(
#             host='127.0.0.1',
#             port=3306,
#             user='root',
#             passwd='123456',
#             db='jobbole_crawlspider',
#             charset='utf8',
#         )
#         self.cur = self.conn.cursor()
#
#     def process_item(self, item, spider):
#         item_data=(item['title'],item['article_type'],item['url'],item['like_num'],item['collect'],item['comment'],)
#         sql = "insert into jobbole(title,article_type,url,like_num,collect,comment)VALUES ('%s','%s','%s','%s','%s','%s')" % (item_data)
#         self.cur.execute(sql)
#         self.conn.commit()
#         return item

class MysqlTwistedPipeline(object):
    def __init__(self):
        dbparms={
            'host': settings['MYSQL_HOST'],
            'port': settings['MYSQL_PORT'],
            'user' :settings['MYSQL_USER'],
            'password' : settings['MYSQL_PASSWORD'],
            'database' : settings['MYSQL_DBNAME'],
            'charset' : 'utf8',
            'cursorclass':cursors.DictCursor
        }
        self.dbpool=adbapi.ConnectionPool('pymysql',**dbparms)

    def process_item(self,item,spider):
        query=self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error,spider)

    def handle_error(self,failure,spider):
        print(failure)

    def do_insert(self,cursor,item):
        item_data = (item['title'], item['article_type'], item['url'], item['like_num'], item['collect'], item['comment'])
        sql = "insert into jobbole(title,article_type,url,like_num,collect,comment)VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,item_data)


