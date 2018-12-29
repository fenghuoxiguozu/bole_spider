# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class JobboleSpider(CrawlSpider):
    name = 'jobbole'
    allowed_domains = ['jobbole.com']
    start_urls = ['http://python.jobbole.com/category/basic/page/1/']

    rules = (
        Rule(LinkExtractor(allow=r'python.jobbole.com/category/basic/page/\d+/'), follow=True),
        Rule(LinkExtractor(allow=r'python.jobbole.com/\d+/'), callback='parse_detail',follow=False),
    )

    def parse_detail(self, response):
        item = {}
        item['title']= response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()
        time= response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract_first()
        item['time'] = time.split()[0]
        item['url'] = response.url
        item['article_type']="-".join(response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract())
        like_num = response.xpath(
            '//span[@class=" btn-bluet-bigger href-style vote-post-up   register-user-only "]/h10/text()').extract_first()
        if like_num=='':
            item['like_num']=0
        else:
            item['like_num'] = like_num

        collect = response.xpath(
            '//span[@class=" btn-bluet-bigger href-style bookmark-btn  register-user-only "]/text()').extract_first()[:-2].replace(' ','')
        if collect=='':
            item['collect']=0
        else:
            item['collect'] = collect

        comment = response.xpath(
            '//span[@class="btn-bluet-bigger href-style hide-on-480"]/text()').extract_first()[:-2].replace(' ','')
        if comment=='':
            item['comment']=0
        else:
            item['comment'] = comment
        return item
