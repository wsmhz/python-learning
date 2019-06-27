import datetime
import json
import re
from urllib import parse

import scrapy
from scrapy.loader import ItemLoader

from utils import zhihuLogin
from items import ZhihuQuestionItem
from items import ZhihuAnswerItem

try:
    import cookielib
except:
    import http.cookiejar as cookielib


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    cookies = {}

    start_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B*%5D.topics&limit={1}&offset={2}"

    def parse(self, response):
        # 爬取格式为 /question/xxx 的url
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = filter(lambda x: True if x.startswith("https") else False, all_urls)
        for url in all_urls:
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:
                request_url = match_obj.group(1)
                yield scrapy.Request(request_url, headers=zhihuLogin.headers, callback=self.parse_question)
            else:
                # 如果不是question页面则递归
                # pass
                yield scrapy.Request(url, headers=zhihuLogin.headers, callback=self.parse)

    def parse_question(self, response):
        match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)
        question_id = ''
        if match_obj:
            question_id = int(match_obj.group(2))

        item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
        item_loader.add_css("title", "h1.QuestionHeader-title::text")
        item_loader.add_css("content", ".QuestionHeader-detail")
        item_loader.add_value("url", response.url)
        item_loader.add_value("zhihu_id", question_id)
        item_loader.add_css("answer_num", ".List-headerText span::text")
        item_loader.add_css("comments_num", ".QuestionHeader-Comment button::text")
        item_loader.add_css("watch_user_num", ".QuestionFollowStatus-counts button div strong::text")
        item_loader.add_css("follow_user_num", ".QuestionFollowStatus-counts div div strong::text")
        item_loader.add_css("topics", ".QuestionHeader-topics .Popover div::text")

        question_item = item_loader.load_item()

        yield scrapy.Request(self.start_answer_url.format(question_id, 20, 0),cookies=self.cookies, headers=zhihuLogin.headers, callback=self.parse_answer)
        yield question_item

    def parse_answer(self, response):
        ans_json = json.loads(response.text)
        is_end = ans_json["paging"]["is_end"]
        next_url = ans_json["paging"]["next"]

        for answer in ans_json["data"]:
            answer_item = ZhihuAnswerItem()
            answer_item["zhihu_id"] = answer["id"]
            answer_item["url"] = answer["url"]
            answer_item["question_id"] = answer["question"]["id"]
            answer_item["author_id"] = answer["author"]["id"] if "id" in answer["author"] else None
            answer_item["content"] = answer["content"] if "content" in answer else None
            answer_item["parise_num"] = answer["voteup_count"]
            answer_item["comments_num"] = answer["comment_count"]
            answer_item["create_time"] = answer["created_time"]
            answer_item["update_time"] = answer["updated_time"]
            answer_item["crawl_time"] = datetime.datetime.now()

            yield answer_item

        if not is_end:
            yield scrapy.Request(next_url, headers=zhihuLogin.headers, callback=self.parse_answer)

    def start_requests(self):
        return [scrapy.Request('https://www.zhihu.com', headers=zhihuLogin.headers, callback=self.check_login)]

    def check_login(self, response):
        account = zhihuLogin.ZhihuAccount('', '')
        load_cookie = account.login(captcha_lang='en', load_cookies=True)
        for item in load_cookie:
            self.cookies.update({
                item.name: item.value
            })
        if self.cookies:
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, cookies=self.cookies, headers=zhihuLogin.headers)
