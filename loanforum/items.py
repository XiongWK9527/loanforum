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


# 51卡农的数据对象
class KaNongItem(scrapy.Item):
    pid = scrapy.Field()  # 产品id
    name = scrapy.Field()  # 产品名称
    edu = scrapy.Field()  # 额度
    description = scrapy.Field()  # 产品描述
    feiyong = scrapy.Field()  # 费用
    applyNum = scrapy.Field()  # 申请人数
    qixian = scrapy.Field()  # 期限
    fangkuangsudu = scrapy.Field()  # 放款速度
    shenhefangshi = scrapy.Field()  # 审核方式
    daozhangfangshi = scrapy.Field()  # 到账方式
    zhengxi = scrapy.Field()  # 征信要求
    platform = scrapy.Field()  # 平台名称
    createTime = scrapy.Field()  # 数据更新时间

# 网贷金的数据对象
class WangDaiJinItem(scrapy.Item):
    pid = scrapy.Field()  # 产品id
    name = scrapy.Field()  # 产品名称
    ptime = scrapy.Field()  # 产品时间
    phone = scrapy.Field()  # 电话
    category = scrapy.Field()  # 类别
    edu = scrapy.Field()  # 额度
    qixian = scrapy.Field()  # 期限
    feiyong = scrapy.Field()  # 费用
    shenhefangshi = scrapy.Field()  # 审核方式
    fangkuangsudu = scrapy.Field()  # 放款速度
    huankuanfangshi = scrapy.Field()  # 还款方式
    daozhangfangshi = scrapy.Field()  # 到账方式
    shijidaokuang = scrapy.Field()  # 实际到账
    xuyaoziliao = scrapy.Field()  # 需要资料
    createTime = scrapy.Field()  # 数据更新时间


# 玉兔的数据对象
class YeTuItem(scrapy.Item):
    pid = scrapy.Field()  # 产品id
    name = scrapy.Field()  # 产品名称
    edu = scrapy.Field()  # 额度范围
    fangkuangsudu = scrapy.Field()  # 放款速度
    qixian = scrapy.Field()  # 借款期限
    lixi = scrapy.Field()  # 利息
    shenqingtiaojian = scrapy.Field()  # 申请条件
    xuyaoziliao = scrapy.Field()  # 需要资料
    shenheshuoming = scrapy.Field()  # 审核说明
    platform = scrapy.Field()  # 平台介绍
    createTime = scrapy.Field()  # 数据更新时间


class LawItem(scrapy.Item):
    pid = scrapy.Field()  # 主键
    name = scrapy.Field()  # 律师事务所名称
    license = scrapy.Field()  # 执业许可证号
    address = scrapy.Field()  # 律师事务所地址
    phone = scrapy.Field()  # 电话
    website = scrapy.Field()  # 律师所网站
    principal = scrapy.Field()  # 律所负责人
    partner = scrapy.Field()  # 合伙人
    url = scrapy.Field() # 事务所地址

class LawFirmItem(scrapy.Item):
    pid = scrapy.Field() # 律师id
    rank = scrapy.Field() # 排名
    name = scrapy.Field() # 律师名
    license = scrapy.Field()  # 执业许可证号
    company = scrapy.Field()  # 单位
    address = scrapy.Field() # 地址
    phone = scrapy.Field() # 电话
    mobile = scrapy.Field() # 手机
    email = scrapy.Field() # 邮箱
    type = scrapy.Field() # 类别
    url = scrapy.Field()  # 网页

class CnLawerItem(scrapy.Item):
    rank = scrapy.Field()  # 排名
    name = scrapy.Field()  # 律师事务所名称
    address = scrapy.Field() # 地址
    law = scrapy.Field() # 律师
    area = scrapy.Field() # 地区

class WxbItem(scrapy.Item):
    rank_day = scrapy.Field()  # 日期
    category = scrapy.Field()  # 类别
    rank = scrapy.Field()      # 排名
    name = scrapy.Field()      # 公众号
    wx_alias = scrapy.Field()  # 微信号
    wx_origin_id = scrapy.Field()  # 微信号/原始号
    desc = scrapy.Field()      # 简介
    pub_total = scrapy.Field() # 发布次数/篇数
    read_num_max = scrapy.Field()  # 头条阅读
    avg_read_num = scrapy.Field()  # 平均阅读
    avg_like_num = scrapy.Field()  # 平均点赞
    fans_num_estimate = scrapy.Field()  # 预估粉丝数
    index_scores = scrapy.Field()  # 小宝指数
    qrcode = scrapy.Field()  # 二维码
    cate_id = scrapy.Field()  # 类型id
