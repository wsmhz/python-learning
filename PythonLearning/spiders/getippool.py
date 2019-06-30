# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector

from items import GetIpPoolItem


class GetIpPoolSpider(scrapy.Spider):
    name = 'getippool'
    allowed_domains = ['xicidaili.com']
    start_urls = ['https://www.xicidaili.com/nn/1']

    pages = 1

    def parse(self, response):
        selector = Selector(response)
        item = GetIpPoolItem()
        tr_list = selector.xpath('//tr')
        for tr in tr_list:
            try:
                head = tr.xpath('td[6]/text()').extract_first().lower()
                ip = tr.xpath('td[2]/text()').extract_first()
                port = tr.xpath('td[3]/text()').extract_first()
                item['head'] = head
                item['ip_port'] = ip + ':' + port
                yield item
            except Exception:
                pass
        urls = ['https://www.xicidaili.com/nn/{}'.format(i) for i in range(self.pages)]
        for url in urls:
            request = scrapy.Request(url, callback=self.parse)
            yield request

