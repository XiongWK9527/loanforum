# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LoanforumItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# 众鑫网卡的存储对象
class ZhonginwankaItem(scrapy.Item):
    pid = scrapy.Field() # 产品id
    name = scrapy.Field() # 产品名称
    edu = scrapy.Field() # 额度
    qixian = scrapy.Field() # 期限
    feiyong = scrapy.Field()  # 费用
    fangkuangsudu = scrapy.Field() # 放款速度
    shenhefangshi = scrapy.Field()  # 审核方式
    daozhangfangshi = scrapy.Field()  # 到账方式
    platform = scrapy.Field()  # 平台名称
    product = scrapy.Field()  # 产品
    phone = scrapy.Field()  # 电话
    zhengxi = scrapy.Field()  # 征信要求
    shijidaokuang = scrapy.Field()  # 实际到账
    category = scrapy.Field()  # 类别
    xuyaoziliao = scrapy.Field()  # 需要资料
    createTime = scrapy.Field() # 数据更新时间


