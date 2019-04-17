# -*- coding: utf-8 -*-
import re

import scrapy

from loanforum.items import LawItem


class LawSpider(scrapy.Spider):
    name = 'law'
    start_urls = ['http://www.lvshiminglu.com/tags']

    # 获取返回内容
    def __get_response_content(self, response) -> str:
        return response.body.decode(response.encoding, errors='ignore')

    # 通用的解析值
    def __get_xpath_value(self, response, xpath) -> str:
        xpath_value = response.xpath(xpath)
        return xpath_value.extract()[0] if len(xpath_value) else ""

    def __get_regex_value(self, content, pattern, index=1) -> str:
        result = re.search(pattern, content, re.M | re.I)
        return result.group(index).strip() if result else ""

    def parse(self, response):
        # 解析律师事务所的分类
        for item in response.xpath("//div[@class='widget widget_categories']/ul/li"):
            full_url = self.__get_xpath_value(item, "a/@href")
            # 去除招聘网站
            if full_url == "http://www.lvshiminglu.com/category/lvshizhaopin":
                continue
            yield scrapy.Request(full_url, callback=self.parse_category)
        pass

    # 解析每个地区的
    def parse_category(self, response):
        # 解析列表
        for item in response.xpath("//ul[@id='archive']/li"):
            full_url = self.__get_xpath_value(item, "h3/a/@href")
            yield scrapy.Request(full_url, callback=self.parse_detail)

        # 处理分页
        next_page = response.xpath("//span[@class='older']/a/@href")
        if next_page:
            full_url = next_page.extract()[0]
            yield scrapy.Request(full_url, callback=self.parse_category)
        pass

    # 解析详情
    def parse_detail(self, response):
        print("product_detail:{}".format(response.url))
        url = response.url
        content = response.body.decode(response.encoding, errors='ignore')
        item = LawItem()
        item['pid'] = self.__get_regex_value(url, r'lvshi/(\d+)\.html')
        item['name'] = self.__get_xpath_value(response, "//*[@class='title']/text()").strip().split("，")[0]
        license = self.__get_regex_value(content, r'(许可证号|执业证号)：([^<]*?)</p', index=2)
        if license == "" :
            license = self.__get_regex_value(content, r'(\d+)（普通合伙[^(]*?）')
        item['license'] = license
        item['address'] = self.__get_regex_value(content, r'地址：([^<]*?)</p')
        item['phone'] = self.__get_regex_value(content, r'电话：([^<]*?)</p')
        item['website'] = self.__get_regex_value(content, r'律师所网站：([^<]*?)</p')
        item['principal'] = self.__get_regex_value(content, r'负责人：([^<]*?)</p')
        item['partner'] = self.__get_regex_value(content, r'合伙人：([^<]*?)</p').replace("：", "")
        item['url'] = url
        yield item



