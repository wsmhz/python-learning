# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, TakeFirst
from w3lib.html import remove_tags


class PythonlearningItem(scrapy.Item):
    pass


def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums

class ZhihuQuestionItem(scrapy.Item):
    zhihu_id = scrapy.Field(
        output_processor=TakeFirst()
    )
    topics = scrapy.Field()
    url = scrapy.Field(
        output_processor=TakeFirst()
    )
    title = scrapy.Field(
        output_processor=TakeFirst()
    )
    content = scrapy.Field(
        output_processor=TakeFirst()
    )
    answer_num = scrapy.Field(
        input_processor=MapCompose(get_nums),
        output_processor=TakeFirst()
    )
    comments_num = scrapy.Field(
        input_processor=MapCompose(get_nums),
        output_processor=TakeFirst()
    )
    watch_user_num = scrapy.Field(
        output_processor=TakeFirst()
    )
    follow_user_num = scrapy.Field(
        output_processor=TakeFirst()
    )

    def get_table_name(self):
        unique_params = {
            'zhihu_id': self["zhihu_id"]
        }
        return 'zhihu_question', unique_params


class ZhihuAnswerItem(scrapy.Item):
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    parise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_table_name(self):
        unique_params = {
            'zhihu_id': self["zhihu_id"]
        }
        return 'zhihu_answer', unique_params


def remove_splash(value):
    # 去掉斜线
    return value.replace("/", "")


class LagouJobItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


def handle_jobaddr(value):
    addr_list = value.split("\n")
    addr_list = [item.strip() for item in addr_list if item.strip() != "查看地图"]
    return "".join(addr_list)


class LagouJobItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    job_id = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    work_years = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    degree_need = scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field()
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_jobaddr),
    )
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    tags = scrapy.Field(
        input_processor=Join(",")
    )
    crawl_time = scrapy.Field()

    def get_table_name(self):
        unique_params = {
            'job_id': self["job_id"]
        }
        return 'lagou_job', unique_params


# ip池
class GetIpPoolItem(scrapy.Item):
    head = scrapy.Field()
    ip_port = scrapy.Field()
    survival_time = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_table_name(self):
        unique_params = {
            'ip_port': self["ip_port"]
        }
        return 'ip_pool', unique_params
