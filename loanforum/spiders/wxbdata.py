# -*- coding: utf-8 -*-
import ast
import re

import scrapy
from loanforum.items import WxbItem

'''
统计sql
select category, rank, name, wx_alias, describle, pub_total, read_num_max, avg_read_num, avg_like_num, fans_num_estimate, index_scores, qrcode from t_wxb order by cate_id, rank asc

备注：
1: 每次需要更改cookies
2: 选择爬取的日榜，周榜，月榜的类型
3: 选择爬取的时间
   日榜 rank_day = "2019-05-05"
   周榜 rank_day = "2019-04-29" rank_day_end= "2019-05-05"
   月榜 rank_day = "2019-04"
   
'''

class WxbdataSpider(scrapy.Spider):
    name = 'wxbdata'
    allowed_domains = ['data.wxb.com']
    start_urls = ['http://data.wxb.com/']

    page_size = 50
    max_size = 300

    # 爬取数据的类型，1:日 2:周 3:月
    rank_type = 1

    ## 需要爬的日期
    # rank_day = "2019-05-05"
    rank_day = "2019-04"
    rank_day_end = ""

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

    category_dict = {
        "-1": "总榜",
        "1": "时事资讯",
        "2": "数码科技",
        "3": "汽车",
        "4": "房产家居",
        "5": "职场招聘",
        "6": "财经理财",
        "7": "生活",
        "8": "情感励志",
        "9": "女性时尚",
        "10": "旅行",
        "11": "运动健康",
        "12": "餐饮美食",
        "13": "搞笑娱乐",
        "14": "明星影视",
        "15": "母婴",
        "16": "文化教育",
        "17": "创业管理",
        "18": "政务",
        "19": "企业",
        "20": "地方",
        "21": "其他"
    }

    def start_requests(self):
        category_list = []
        # 需要爬去的页面
        for x in self.category_dict.keys():
            category_list.append(str(x))

        for category in category_list:
            url = ''
            # 日榜
            if self.rank_type == 1:
                url = "https://data.wxb.com/rank/day/{rank_day}/{category}?sort=&page=1&page_size={page_size}"\
                    .format(rank_day=self.rank_day, category=category, page_size=self.page_size)
            # 周榜
            elif self.rank_type == 2:
                url = "https://data.wxb.com/rank/week/{rank_day}/{rank_day_end}/{category}?sort=&page=1&page_size={page_size}" \
                    .format(rank_day=self.rank_day, rank_day_end=self.rank_day_end, category=category, page_size=self.page_size)
            # 月榜
            elif self.rank_type == 3:
                url = "https://data.wxb.com/rank/month/{rank_day}/{category}?sort=&page=1&page_size={page_size}"\
                    .format(rank_day=self.rank_day, category=category, page_size=self.page_size)
            yield scrapy.Request(url=url,
                                 headers=self.headers,
                                 cookies=self.cookie,
                                 callback=self.parse)

    def __get_regex_value(self, content, pattern, index=1) -> str:
        result = re.search(pattern, content, re.M | re.I)
        return result.group(index).strip() if result else ""

    ## 移除emoji
    def __remove_emoji(self, text):
        content = str(text).encode('utf-8', 'replace').decode('utf-8')
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', content)


    def parse(self, response):
        url = response.url
        print("crawl: url={0}".format(url))
        page = self.__get_regex_value(url, r'page=(\d+)')
        category = self.__get_regex_value(url, r'/([-\d]+?)\?')

        content = response.body.decode(response.encoding, errors='ignore')
        ## 解析值
        wxb_data = ast.literal_eval(content)
        for data in wxb_data['data']:
            item = WxbItem()
            item['rank_day'] = self.rank_day
            item['category'] = self.category_dict[category]
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
            item['qrcode'] = str(data['qrcode']).replace("\\", "/").replace("//", "/")
            item['cate_id'] = category
            yield item

        pageValue = int(page)
        ## 普通会员只能爬取top300
        if pageValue < (self.max_size / self.page_size):
            pageValue = pageValue + 1

            url = ''
            # 日榜
            if self.rank_type == 1:
                url = "https://data.wxb.com/rank/day/{rank_day}/{category}?sort=&page={page}&page_size={page_size}"\
                    .format(rank_day=self.rank_day, category=category, page=pageValue, page_size=self.page_size)
            # 周榜
            elif self.rank_type == 2:
                url = "https://data.wxb.com/rank/week/{rank_day}/{rank_day_end}/{category}?sort=&page={page}&page_size={page_size}" \
                    .format(rank_day=self.rank_day, rank_day_end=self.rank_day_end, category=category, page=pageValue, page_size=self.page_size)
            # 月榜
            elif self.rank_type == 3:
                url = "https://data.wxb.com/rank/month/{rank_day}/{category}?sort=&page={page}&page_size={page_size}" \
                    .format(rank_day=self.rank_day, category=category, page=pageValue, page_size=self.page_size)
            yield scrapy.Request(url=url,
                                 headers=self.headers,
                                 cookies=self.cookie,
                                 callback=self.parse)
        pass
