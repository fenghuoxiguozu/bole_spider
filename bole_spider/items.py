# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BoleSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()                                #文章标题
    url=scrapy.Field()                                    #文章URL
    article_type = scrapy.Field()                              #文章分类
    like_num = scrapy.Field()                                #赞
    collect = scrapy.Field()                        #收藏
    comment = scrapy.Field()                 #评论

