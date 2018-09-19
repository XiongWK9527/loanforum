# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from loanforum.db.DBHelper import DBHelper


class LoanforumPipeline(object):

    def __init__(self):
        self.db = DBHelper()

    def process_item(self, item, spider):
        self.db.save_zxwk(item)
        return item
