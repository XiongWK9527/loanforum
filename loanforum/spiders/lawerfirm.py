# -*- coding: utf-8 -*-
import re

import scrapy
from lxml import etree

from loanforum.items import LawFirmItem


class LawerfirmSpider(scrapy.Spider):
    name = 'lawerfirm'
    start_urls = ['http://www.cnlaw.net/rank/']
    base_url = "http://www.cnlaw.net/"

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
        html_content = response.body.decode(response.encoding, errors='ignore')
        item_list = []

        item_list += self.parse_index(html_content, "//b[contains(text(), '律师排行榜100强')]/../../div/ul", "业务")
        item_list += self.parse_index(html_content, "//b[contains(text(), '公益律师100强')]/../../div/ul", "公益")
        item_list += self.parse_index(html_content, "//b[contains(text(), '民商法律师100强')]/../../div/ul", "民商")
        item_list += self.parse_index(html_content, "//b[contains(text(), '刑事辩护律师50强')]/../../div/ul", "刑事辩护")
        item_list +=self.parse_index(html_content, "//b[contains(text(), '知识产权律师50强')]/../../div/ul", "知识产权")
        for x in item_list:
            item = LawFirmItem()
            item['rank'] = x['rank']
            item['name'] = x['name']
            item['type'] = x['type']
            yield scrapy.Request(url=x['url'], meta={'item': item}, callback=self.parse_law_detail, dont_filter=True)
        pass


    def parse_law_detail(self, response):
        item = response.meta['item']
        url = response.url
        content = response.body.decode(response.encoding, errors='ignore')

        item['url'] = url
        item['pid'] = self.__get_regex_value(url, r'lawyer/(\d+)\.htm')
        item['license'] = self.__get_regex_value(content, r'(许可证号|执业证号)：([^<]*?)<br>', index=2)
        item['company'] = self.__get_regex_value(content, r'(单位)：([^<]*?)<br>', index=2)
        item['address'] = self.__get_regex_value(content, r'(地址)：([^<]*?)<br>', index=2)
        item['phone'] = self.__get_regex_value(content, r'(电话)：([^<&]*?)<br>', index=2)
        item['mobile'] = self.__get_regex_value(content, r'(手机)：([^<&]*?)<br>', index=2)
        item['email'] = self.__get_regex_value(content, r'(信箱)：([^<&]*?)<br>', index=2)
        yield item

    def parse_index(self, html_content, xpath, type) -> list:
        item_list = []
        html = etree.HTML(html_content)
        div_value = html.xpath(xpath)
        div_text = div_value[0].xpath("string(.)")
        # 兼容刑事的情况
        div_text = str(div_text).replace("&nbsp", " ")
        content_list = re.findall(r'\d{0,3}\s\S+\([\d-]+\S+·\S+\)', div_text, re.M | re.I)

        link_list = div_value[0].xpath("a/@href")
        for x in range(len(content_list)):
            value = re.search(r'(\d{0,3})\s(\S+)\([\d-]+(\S+)·\S+\)', content_list[x], re.M | re.I)
            rank = value.group(1)
            if rank == None or rank == "":
                rank = x + 1
            full_url = "{0}{1}".format(self.base_url, str(link_list[x]).replace("../", ""))
            # print("{0}-{1}-{2}".format(rank, full_url, type))
            name = value.group(2).replace("律师", "").replace("&nbsp", "")
            name = re.sub("\d", "", name) ## 正则去除数字
            item_list.append({"rank": rank, "type":type, "name": name, "url":full_url})
        return item_list
            # yield scrapy.Request(url=full_url, meta={'item':item},callback=self.parse_law_detail,dont_filter=True)



