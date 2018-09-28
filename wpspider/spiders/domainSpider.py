# -*- coding: utf-8 -*-
import scrapy
from wpspider.items import Url
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class DomainspiderSpider(scrapy.Spider):
    name = 'domainSpider'
    ignore_urls = ['facebook.com','tumblr.com','youtube.com', 'baidu.com','twitter.com','wordpress.com','wikipedia.com']
    start_urls = ['https://blogforarizona.net/']

    def parse(self, response):
        hxs = scrapy.Selector(response)
        # extract all links from page
        all_links = hxs.xpath('*//a/@href').extract()
        # iterate over links

        spltAr = response.url.split("://")
        i = (0,1)[len(spltAr)>1]
        domain = spltAr[i].split("?")[0].split('/')[0].split(':')[0].lower()

        for link in LinkExtractor(allow=(), deny=(self.ignore_urls + [domain])).extract_links(response):

            spltAr = link.url.split("://")
            i = (0, 1)[len(spltAr) > 1]
            dmn = spltAr[i].split("?")[0].split('/')[0].split(':')[0].lower()

            item = Url()
            item['domain'] = dmn
            yield item
            yield scrapy.http.Request(url=link.url)