# -*- coding: utf-8 -*-
import re

import scrapy

from loanforum.items import WangDaiJinItem


class WangdaijinSpider(scrapy.Spider):
    name = 'wangdaijin'
    start_urls = ['https://www.wangdaijin.com/list52/']
    base_url = 'https://www.wangdaijin.com/'

    def parse(self, response):
        # 解析具体的产品
        for href in response.xpath("//li[@class='clt wkload item']/a/@href").extract():
            full_url = "{}{}".format(self.base_url, href)
            yield scrapy.Request(full_url, callback=self.parse_product_detail)

        # 产品列表页 下一页
        next_page = response.xpath("//a[@class='nxt']/@href")
        if next_page:
            yield scrapy.Request(next_page.extract()[0])
        pass

    # 通用的解析值
    def parse_xpath(self, response, xpath):
        xpath_value = response.xpath(xpath)
        return xpath_value.extract()[0] if len(xpath_value) else ""

    # 解析具体的产品信息
    def parse_product_detail(self, response):
        print("product_detail:{}".format(response.url))
        url = response.url
        content = response.body.decode(response.encoding, errors='ignore')

        item = WangDaiJinItem()
        item['pid'] = re.search( r'article/(\d+)', url, re.M|re.I).group(1)
        item['name'] = re.search( r'产品：([\s\S]*?)</div>', content, re.M|re.I).group(1)
        item['ptime'] = self.parse_xpath(response, "//em[contains(@id,'authorposton')]/text()").replace("发表于", "")
        item['phone'] = self.parse_xpath(response, "//a[@class='wkphone']/@href").replace("tel:","").replace("/","")
        item['category'] = re.search( r'类别：([\s\S]*?)</div>', content, re.M|re.I).group(1)
        item['edu'] = self.parse_xpath(response, "//span[contains(text(),'额度')]/../text()").replace("：", "")
        item['qixian'] = self.parse_xpath(response, "//span[contains(text(),'期限')]/../text()").replace("：", "")
        item['feiyong'] = self.parse_xpath(response, "//span[contains(text(),'费用')]/../text()").replace("：", "")
        item['shenhefangshi'] = self.parse_xpath(response, "//span[contains(text(),'审核')]/../text()").replace("：", "")
        item['fangkuangsudu'] = self.parse_xpath(response, "//span[contains(text(),'放款速度')]/../text()").replace("：", "")
        item['huankuanfangshi'] = self.parse_xpath(response, "//span[contains(text(),'还款方式')]/../text()").replace("：", "")
        item['daozhangfangshi'] = self.parse_xpath(response, "//span[contains(text(),'到帐方式')]/../text()").replace("：", "")
        item['shijidaokuang'] = self.parse_xpath(response, "//span[contains(text(),'实际到帐金额')]/../text()").replace("：", "")
        item['xuyaoziliao'] = self.parse_xpath(response, "//span[contains(text(),'需要资料')]/../text()").replace("：", "")
        yield item
