# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from loanforum.db.DBHelper import DBHelper
from spiders.a51kanong import A51kanongSpider
from spiders.wangdaijin import WangdaijinSpider
from spiders.zhongxinwanka import ZhongxinwankaSpider


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
        return item
