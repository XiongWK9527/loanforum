# -*- coding: utf-8 -*-
import re

import scrapy

from loanforum.items import YeTuItem

class YetuSpider(scrapy.Spider):
    name = 'yetu'
    start_urls = ['https://www.yetu.net/product/']
    __base_domain_url = "https://www.yetu.net"

    # 获取返回内容
    def __get_response_content(self, response) -> str:
        return response.body.decode(response.encoding, errors='ignore')

    # 通用的解析值
    def __get_xpath_value(self, response, xpath) -> str:
        xpath_value = response.xpath(xpath)
        return xpath_value.extract()[0] if len(xpath_value) else ""


    def parse(self, response):
        # 解析具体的产品
        for product_item in response.xpath("//div[@id='content']/div[1]/div[1]/div[1]/ul[1]/li"):
            full_url = "{}{}".format(self.__base_domain_url, self.__get_xpath_value(product_item, "a/@href"))
            yield scrapy.Request(full_url, callback=self.parse_product_detail)

        # 产品列表页 下一页
        next_page = response.xpath("//a[contains(text(),'下一页')]/@href")
        if next_page:
            full_url = "{}{}".format(self.__base_domain_url, next_page.extract()[0])
            yield scrapy.Request(full_url)
        pass

    def parse_product_detail(self, response):
        url = response.url
        item = YeTuItem()

        pid = re.search(r'product/(\d+)', url, re.M | re.I).group(1)
        item['pid'] = pid
        item['name'] = self.__get_xpath_value(response, "//div[@class='tit']/h1[1]/text()").strip()
        item['edu'] = self.__get_xpath_value(response, "//div[@class='rate']/span[1]/text()").strip()
        item['fangkuangsudu'] = self.__get_xpath_value(response, "//div[@class='rate']/label[1]/text()").strip()
        item['qixian'] = self.__get_xpath_value(response, "//div[@class='sr-tag']/label[1]/text()").strip()
        item['lixi'] = self.__get_xpath_value(response, "//span[@id='lixi']/text()").strip()
        item['shenqingtiaojian'] = self.__get_xpath_value(response, "//div[contains(text(), '申请条件')]/following-sibling::p[1]/text()").strip()
        item['xuyaoziliao'] = self.__get_xpath_value(response, "//div[contains(text(), '所需材料')]/following-sibling::p[1]/text()").strip()
        item['shenheshuoming'] = self.__get_xpath_value(response, "//div[contains(text(), '审核说明')]/following-sibling::p[1]/text()").strip()
        item['platform'] = self.__get_xpath_value(response, "//div[contains(text(), '平台介绍')]/following-sibling::p[1]/text()").strip()
        yield item
