# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging

import pymongo


class MongoPipeline(object):

    def __init__(self, mongo_db):
        self.mongo_db = mongo_db

    @classmethod
    def from_settings(cls, settings):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        db_name = settings["MONGODB_DB_NAME"]
        # 创建MONGODB数据库链接
        client = pymongo.MongoClient(host=host, port=port)
        # 指定数据库
        return cls(client[db_name])

    def process_item(self, item, spider):
        # 根据不同的item 构建不同的表
        table_name, unique_params = item.get_table_name()
        # 存放数据的数据库表名
        post = self.mongo_db[table_name]
        data = dict(item)
        if not post.update(unique_params, {'$set': data}, True):
            logging.error('保存到mongo失败, {}'.format(data))
        else:
            logging.info('保存到mongo成功, {}'.format(unique_params))
        return item
