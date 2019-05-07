# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from loanforum.db.DBHelper import DBHelper
from loanforum.spiders.a51kanong import A51kanongSpider
from loanforum.spiders.wangdaijin import WangdaijinSpider
from loanforum.spiders.zhongxinwanka import ZhongxinwankaSpider
from loanforum.spiders.yetu import YetuSpider
from loanforum.spiders.law import LawSpider
from loanforum.spiders.lawerfirm import LawerfirmSpider
from loanforum.spiders.cnlawer import CnlawerSpider
from loanforum.spiders.wxbdata import WxbdataSpider


class LoanforumPipeline(object):

    def __init__(self):
        self.db = DBHelper()

    def process_item(self, item, spider):
        if spider.name == ZhongxinwankaSpider.name:
            self.db.save_zxwk(item)
        elif spider.name == A51kanongSpider.name:
            self.db.save_51kanong(item)
        elif spider.name == WangdaijinSpider.name:
            self.db.save_wangdaijin(item)
        elif spider.name == YetuSpider.name:
            self.db.save_yetu(item)
        elif spider.name == LawSpider.name:
            self.db.save_law(item)
        elif spider.name == LawerfirmSpider.name:
            self.db.save_law_firm_rank(item)
        elif spider.name == CnlawerSpider.name:
            self.db.save_cnlawer_rank(item)
        elif spider.name == WxbdataSpider.name:
            self.db.save_wxb_data(item)
            pass
        return item
