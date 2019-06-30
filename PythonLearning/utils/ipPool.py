# -*- coding: utf-8 -*-

import pymongo
import requests
from scrapy.conf import settings


class IpPool(object):

    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        db_name = settings["MONGODB_DB_NAME"]
        # 创建MONGODB数据库链接
        client = pymongo.MongoClient(host=host, port=port)
        # 指定数据库
        self.mongo_db = client[db_name]
        self.post = self.mongo_db['ip_pool']

    def delete_proxy(self, ip_port):
        # 删除无效代理
        self.post.delete_one({"ip_port": ip_port})

    # 判断ip是否可用
    def judge_proxy(self, ip_port, head):
        http_url = "http://www.baidu.com"
        try:
            proxy_dict = {
                'http': 'http://' + ip_port,
            }
            response = requests.get(http_url, proxies=proxy_dict)
        except Exception:
            print("不可用代理ip地址：" + head + '://' + ip_port)
            self.delete_proxy(ip_port)
            return False
        else:
            code = response.status_code
            if 200 <= code < 300:
                print("有效的代理ip地址：" + head + '://' + ip_port)
                return True
            else:
                print("不可用代理ip地址：" + head + '://' + ip_port)
                self.delete_proxy(ip_port)
                return False

    def get_random_proxy(self):
        data = None
        # 随机选取一条
        for item in self.post.aggregate([{'$sample': {'size': 1}}]):
            data = item
            break
        ip_port = data['ip_port']
        head = data['head']
        if self.judge_proxy(ip_port, head):
            return 'http://' + ip_port
        else:
            return self.get_random_proxy()


if __name__ == "__main__":
    get_ip = IpPool()
    print(get_ip.get_random_proxy())
