# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import re

import scrapy
from scrapy.loader.processors import MapCompose, Join, TakeFirst


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
        return 'zhihu_question',unique_params


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
        return 'zhihu_answer',unique_params
