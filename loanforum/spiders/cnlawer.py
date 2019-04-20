# -*- coding: utf-8 -*-
import re

import scrapy
from lxml import etree

from loanforum.items import CnLawerItem


class CnlawerSpider(scrapy.Spider):
    name = 'cnlawer'
    start_urls = ['http://www.cnlaw.net/lawfirm/']
    base_domain_url = "http://www.cnlaw.net/lawfirm/"

    # 通用的解析值
    def __get_xpath_value(self, response, xpath) -> str:
        xpath_value = response.xpath(xpath)
        return xpath_value.extract()[0] if len(xpath_value) else ""

    def __get_regex_value(self, content, pattern, index=1) -> str:
        result = re.search(pattern, content, re.M | re.I)
        return result.group(index).strip() if result else ""

    def parse(self, response):
        # 解析省份
        for item in response.xpath("//img[contains(@src, 'images/1hand.gif')]/../a"):
            href = self.__get_xpath_value(item, "@href")
            area = self.__get_xpath_value(item, "text()")
            full_url = "{}{}".format(self.base_domain_url, href)
            yield scrapy.Request(full_url, meta={'area':area}, callback=self.parse_province)
        pass

    def parse_province(self, response):
        area = response.meta['area']
        url = response.url
        content = response.body.decode(response.encoding, errors='ignore')
        html = etree.HTML(content)
        td = html.xpath("//img[contains(@src, 'images/1.gif')]/..")
        td_str = td[0].xpath("string(.)")
        # print(td_str)
        match_list = re.findall(r'\d{0,3}\s\S*?\s+? 地址：\S*?\s*?律师：\S+?,', str(td_str), re.M | re.I)
        for x in range(len(match_list)):
            value = re.search(r'(\d{0,3})\s(\S*?)\s+? 地址：(\S*?)\s*?律师：(\S+?),', match_list[x], re.M | re.I)
            rank = value.group(1)
            if rank == None or rank == "":
                rank = x + 1
            name = value.group(2)
            if name == str(rank):
                name = ""
            address = value.group(3)
            lawer = value.group(4)
            item = CnLawerItem()
            item['area'] = area
            item['rank'] = rank
            item['address'] = address
            item['name'] = name
            item['law'] = lawer
            print("{0}-{1}-{2}-{3}".format(rank, name, address, lawer))
            yield item


