# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from scrapy.selector import Selector

from items import GetIpPoolItem


class GetIpPoolSpider(scrapy.Spider):
    name = 'getippool'
    allowed_domains = ['xicidaili.com']
    # start_urls = ['https://www.xicidaili.com/nn/1']
    start_urls = ['https://www.xicidaili.com/nt/1']

    pages = 1

    def parse(self, response):
        item = GetIpPoolItem()
        selector = Selector(text=response.text)
        all_trs = selector.css("#ip_list tr")
        for tr in all_trs[1:]:
            try:
                all_texts = tr.css("td::text").extract()
                survival_time = all_texts[10].strip()
                if survival_time != '1分钟':
                    ip = all_texts[0].strip()
                    port = all_texts[1].strip()
                    proxy_type = all_texts[5].strip().lower()
                    if not proxy_type:
                        proxy_type = 'http'
                    item['head'] = proxy_type
                    item['ip_port'] = ip + ':' + port
                    item['survival_time'] = survival_time
                    item['crawl_time'] = datetime.now()
                    yield item
            except Exception:
                pass
        # format_url = 'https://www.xicidaili.com/nn/{}'
        format_url = 'https://www.xicidaili.com/nt/{}'
        urls = [format_url.format(i) for i in range(self.pages)]
        for url in urls:
            request = scrapy.Request(url, callback=self.parse)
            yield request

