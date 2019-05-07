# -*- coding: utf-8 -*-
import ast
import re

import scrapy
from loanforum.items import WxbItem


class WxbdataSpider(scrapy.Spider):
    name = 'wxbdata'
    allowed_domains = ['data.wxb.com']
    start_urls = ['http://data.wxb.com/']
    ## 需要爬的日期
    rank_day = "2019-05-05"
    page_size = 50
    max_size = 300

    headers = {
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://data.wxb.com/rank?category=-1&page=1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
    }

    # 存在的cookies
    cookie = {
        "aliyungf_tc": "AQAAAIbCcl1fagIA4lfgeupftjHzv5sl",
        "visit-wxb-id": "cd95962440b0d376c87453ea955c6762",
        "wxb_fp_id": "2515334045",
        "PHPSESSID": "832b74e72ebc087e18e567ff6386c3c1"
    }

    def start_requests(self):
        # 需要爬去的页面
        category = ["-1"]
        for x in range(21):
            category.append(str(x + 1))

        for index in category:
            yield scrapy.Request(url="https://data.wxb.com/rank/day/{rank_day}/{index}?sort=&page=1&page_size={page_size}"
                                 .format(rank_day=self.rank_day, index=index, page_size=self.page_size),
                                 headers=self.headers,
                                 cookies=self.cookie,
                                 callback=self.parse)

    def __get_regex_value(self, content, pattern, index=1) -> str:
        result = re.search(pattern, content, re.M | re.I)
        return result.group(index).strip() if result else ""

    ## 移除emoji
    def __remove_emoji(self, text):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', str(text))


    def parse(self, response):
        url = response.url
        print("crawl: url={0}".format(url))
        page = self.__get_regex_value(url, r'page=(\d+)')
        category = self.__get_regex_value(url, r'rank/day/\S+?/([-\d]+?)\?')

        content = response.body.decode(response.encoding, errors='ignore')
        ## 解析值
        wxb_data = ast.literal_eval(content)
        for data in wxb_data['data']:
            item = WxbItem()
            item['rank_day'] = self.rank_day
            item['category'] = category
            item['rank'] = data['rank']
            item['name'] = self.__remove_emoji(data['name'])
            item['wx_alias'] = data['wx_alias']
            item['wx_origin_id'] = data['wx_origin_id']
            item['desc'] = self.__remove_emoji(data['desc'])
            item['pub_total'] = "{pub}/{total}".format(pub=data['push_total'], total=data['articles_total'])
            item['read_num_max'] = data['read_num_max']
            item['avg_read_num'] = data['avg_read_num']
            item['avg_like_num'] = data['avg_like_num']
            item['fans_num_estimate'] = data['fans_num_estimate']
            item['index_scores'] = data['index_scores']
            item['qrcode'] = data['qrcode']
            yield item

        pageValue = int(page)
        ## 普通会员只能爬取top300
        if pageValue < (self.max_size / self.page_size):
            pageValue = pageValue + 1
            yield scrapy.Request(url="https://data.wxb.com/rank/day/{rank_day}/{category}?sort=&page={page}&page_size={page_size}"
                                 .format(rank_day=self.rank_day, category=category, page=pageValue, page_size=self.page_size),
                                 headers=self.headers,
                                 cookies=self.cookie,
                                 callback=self.parse)
        pass
