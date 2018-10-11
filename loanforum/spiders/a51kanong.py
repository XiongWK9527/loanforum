# -*- coding: utf-8 -*-
import scrapy

from loanforum.items import KaNongItem


class A51kanongSpider(scrapy.Spider):
    name = '51kanong'
    start_urls = ['http://daikuan.51kanong.com/Daikuan/lists/']
    base_url = 'http://daikuan.51kanong.com'

    # 通用的解析值
    def parse_xpath(self, response, xpath):
        xpath_value = response.xpath(xpath)
        return xpath_value.extract()[0] if len(xpath_value) else ""


    def parse(self, response):
        # 解析具体的产品
        for product_item in response.xpath("//tbody[@id='daikuan_list']/tr"):
            item = KaNongItem()
            pid = self.parse_xpath(product_item, "td[@class='action']/a/@href")
            if pid is not None and len(pid) > 0:
                item['pid'] = pid[1:]
            else:
                continue
            item['name'] = self.parse_xpath(product_item, "td[@class='logo']/span/text()")
            item['edu'] = self.parse_xpath(product_item, "td[@class='prosition']/text()")
            item['description'] = self.parse_xpath(product_item, "td[@class='info']/text()")
            item['feiyong'] = self.parse_xpath(product_item, "td[@class='cost']/text()")
            item['applyNum'] = self.parse_xpath(product_item, "td[@class='time']/text()")
            full_url = "{}{}".format(self.base_url, pid)
            yield scrapy.Request(url=full_url, meta={'item':item},callback=self.parse_product_detail,dont_filter=True)

        # 产品列表页 下一页
        next_page = response.xpath("//a[@class='next']/@href")
        if next_page:
            full_url = "{}{}".format(self.base_url, next_page.extract()[0])
            yield scrapy.Request(full_url)
        pass


    # 解析具体的产品信息
    def parse_product_detail(self, response):
        item = response.meta['item']
        item['qixian'] = self.parse_xpath(response, "//td[contains(text(),'期限')]/i/text()")
        item['fangkuangsudu'] = self.parse_xpath(response, "//td[contains(text(),'放款速度')]/i/text()")
        item['shenhefangshi'] = self.parse_xpath(response, "//td[contains(text(),'审核方式')]/i/text()")
        item['daozhangfangshi'] = self.parse_xpath(response, "//td[contains(text(),'到帐方式')]/i/text()")
        item['zhengxi'] = self.parse_xpath(response, "//td[contains(text(),'征信要求')]/i/text()")
        item['platform'] = self.parse_xpath(response, "//td[contains(text(),'平台名称')]/i/text()")
        yield item
