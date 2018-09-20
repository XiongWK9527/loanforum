# -*- coding: utf-8 -*-
import os
import re
import time

import scrapy
from scrapy.loader import ItemLoader

from loanforum.items import ZhonginwankaItem


class ZhongxinwankaSpider(scrapy.Spider):
    name = 'zhongxinwanka'
    start_urls = ['https://www.zhongxinwanka.com/forum-95-1.html']
    base_save_file_path = "/tmp/file"
    base_website_domain = "https://www.zhongxinwanka.com/"

    def __init__(self):
        self.save_file_path = os.path.join(self.base_save_file_path, \
                                           time.strftime("%Y%m%d"), \
                                           self.name, \
                                           time.strftime("%Y%m%d%H%M%S"))
        self.mkdir(self.save_file_path)

    # 多级目录创建
    def mkdir(self, path):
        if not os.path.isdir(path):
            self.mkdir(os.path.split(path)[0])
        else:
            return
        os.mkdir(path)

    # 保存文件
    def save_origin_file(self, response):
        filename = response.url.split("/")[-1]
        with open(os.path.join(self.save_file_path, filename), 'wb') as f:
            f.write(response.body)
        pass

    def parse(self, response):
        # 解析具体的产品
        for href in response.xpath("//div[@class='deansubpics']/a/@href").extract():
            full_url = "{}{}".format(self.base_website_domain, href)
            yield scrapy.Request(full_url, callback=self.parse_product_detail)

        # 产品列表页 下一页
        # self.save_origin_file(response)
        next_page = response.xpath("//a[@class='nxt']/@href")
        if next_page:
            full_url = "{}{}".format(self.base_website_domain, next_page.extract()[0])
            yield scrapy.Request(full_url)
        pass

    # 通用的解析值
    def parse_xpath(self, response, xpath):
        xpath_value = response.xpath(xpath)
        return xpath_value.extract()[0] if len(xpath_value) else ""


    # 解析具体的产品信息
    def parse_product_detail(self, response):
        # self.save_origin_file(response)
        print("product_detail:{}".format(response.url))

        url = response.url
        pid = re.search( r'thread-(\d+)-', url, re.M|re.I).group(1)
        content = response.body.decode(response.encoding, errors='ignore')
        # 解析数据对象
        product_item = ItemLoader(item = ZhonginwankaItem(), response = response)
        product_item.add_value('pid', pid)
        product_item.add_value('name', self.parse_xpath(response, "//span[@id='thread_subject']/text()"))
        product_item.add_value('edu', self.parse_xpath(response, "//p[contains(text(),'额度')]/following-sibling::span[1]/text()"))
        product_item.add_value('qixian', self.parse_xpath(response, "//p[contains(text(),'期限')]/following-sibling::span[1]/text()"))
        product_item.add_value('feiyong', self.parse_xpath(response, "//p[contains(text(),'费用')]/following-sibling::span[1]/text()"))
        product_item.add_value('fangkuangsudu', re.search( r'放款速度：([\s\S]*?)</', content, re.M|re.I).group(1))
        product_item.add_value('shenhefangshi', re.search( r'审核方式：([\s\S]*?)</', content, re.M|re.I).group(1))
        product_item.add_value('daozhangfangshi', re.search( r'到账方式：([\s\S]*?)</', content, re.M|re.I).group(1))
        product_item.add_value('platform', self.parse_xpath(response, "//span[contains(text(),'平台名称')]/../text()"))
        product_item.add_value('product', self.parse_xpath(response, "//span[contains(text(),'产品')]/../text()"))
        product_item.add_value('phone', self.parse_xpath(response, "//span[contains(text(),'电话')]/../text()"))
        product_item.add_value('zhengxi', self.parse_xpath(response, "//span[contains(text(),'征信要求')]/../text()"))
        product_item.add_value('shijidaokuang', self.parse_xpath(response, "//span[contains(text(),'实际到账')]/../text()"))
        product_item.add_value('category', self.parse_xpath(response, "//span[contains(text(),'类别')]/../text()"))
        product_item.add_value('xuyaoziliao', self.parse_xpath(response, "//span[contains(text(),'需要资料')]/../text()"))
        return product_item.load_item()
