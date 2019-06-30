# -*- coding: utf-8 -*-
from datetime import datetime

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from items import LagouJobItem, LagouJobItemLoader


class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    # headers = {
    #     'Host': 'www.lagou.com',
    #     'Referer': 'https://www.lagou.com/',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    #                   '(KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    # }

    rules = (
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
        # Rule(LinkExtractor(allow=r'jobs/\d+.html'), process_request='request_process', callback='parse_job',
        #      follow=True),
        # Rule(LinkExtractor(allow=("zhaopin/.*",)), process_request='request_process', follow=True),
        # Rule(LinkExtractor(allow=("gongsi/j\d+.html",)), process_request='request_process', follow=True),
    )

    # def request_process(self, request):
    #     new_request = request.replace(headers=self.headers)
    #     new_request.meta.update(cookiejar=1)
    #     return new_request

    def parse_job(self, response):
        item_loader = LagouJobItemLoader(item=LagouJobItem(), response=response)
        item_loader.add_css("title", ".job-name::attr(title)")
        item_loader.add_value("url", response.url)
        item_loader.add_xpath("job_id", '//*[@id="jobid"]/@value')
        item_loader.add_css("salary", ".job_request .salary::text")
        item_loader.add_xpath("job_city", "//*[@class='job_request']/p/span[2]/text()")
        item_loader.add_xpath("work_years", "//*[@class='job_request']/p/span[3]/text()")
        item_loader.add_xpath("degree_need", "//*[@class='job_request']/p/span[4]/text()")
        item_loader.add_xpath("job_type", "//*[@class='job_request']/p/span[5]/text()")

        item_loader.add_css("tags", '.position-label li::text')
        item_loader.add_css("publish_time", ".publish_time::text")
        item_loader.add_css("job_advantage", ".job-advantage p::text")
        item_loader.add_css("job_desc", ".job_bt div")
        item_loader.add_css("job_addr", ".work_addr")
        item_loader.add_css("company_name", "#job_company dt a img::attr(alt)")
        item_loader.add_css("company_url", "#job_company dt a::attr(href)")
        item_loader.add_value("crawl_time", datetime.now())

        job_item = item_loader.load_item()

        return job_item
