# -*- coding: utf-8 -*-
import time

import pymysql
from scrapy.utils.project import get_project_settings
from twisted.enterprise import adbapi


class DBHelper():
    '''这个类也是读取settings中的配置，自行修改代码进行操作'''

    def __init__(self):
        settings = get_project_settings()  #获取settings配置，设置需要的信息

        dbparams = dict(
            host=settings['MYSQL_HOST'],  #读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            # charset='utf8mb4',  #编码要加上，否则可能出现中文乱码问题
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
            cp_max=20,
            cp_reconnect=True,
        )
        #**表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)

        self.dbpool = dbpool

    def connect(self):
        return self.dbpool

    def save_zxwk(self, item):
        # 插入数据
        insert = self.dbpool.runInteraction(self._conditional_insert_zxwk, item)
        insert.addErrback(self._handle_error)
        return item

    # 保存51卡农的数据
    def save_51kanong(self, item):
        # 插入数据
        insert = self.dbpool.runInteraction(self._conditional_insert_kanong, item)
        insert.addErrback(self._handle_error)
        return item

    # 保存网贷金的数据
    def save_wangdaijin(self, item):
        # 插入数据
        insert = self.dbpool.runInteraction(self._conditional_insert_wangdaijin, item)
        insert.addErrback(self._handle_error)
        return item

    # 保存玉兔的数据
    def save_yetu(self, item):
        # 插入数据
        insert = self.dbpool.runInteraction(self._conditional_insert_yetu, item)
        insert.addErrback(self._handle_error)
        return item

    # 保存律师会所信息
    def save_law(self, item):
        # 插入数据
        insert = self.dbpool.runInteraction(self._conditional_insert_law, item)
        insert.addErrback(self._handle_error)
        return item

    ## 保存律师排名
    def save_law_firm_rank(self, item):
        # 插入数据
        insert = self.dbpool.runInteraction(self._conditional_insert_law_firm_rank, item)
        insert.addErrback(self._handle_error)
        return item

    ## 保存律师事务所排名
    def save_cnlawer_rank(self, item):
        # 插入数据
        insert = self.dbpool.runInteraction(self._conditional_insert_cnlawer_rank, item)
        insert.addErrback(self._handle_error)
        return item

    ## 保存wxb数据
    def save_wxb_data(self, item):
        # 插入数据
        insert = self.dbpool.runInteraction(self._conditional_insert_wxb_data, item)
        insert.addErrback(self._handle_error)
        return item

    # 写入数据库中
    def _conditional_insert_kanong(self, tx, item):
        sql = "delete from t_kanong where pid = '{}';".format(item['pid'])
        tx.execute(sql)

        sql = "insert into t_kanong(pid,name,edu,description,feiyong,applyNum,qixian,fangkuangsudu,shenhefangshi,daozhangfangshi,zhengxi,platform,createTime) " \
              "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        item['createTime'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                           time.localtime(time.time()))
        params = (item["pid"], item['name'], item['edu'], item['description'], \
                  item['feiyong'], item['applyNum'], item['qixian'], item['fangkuangsudu'], \
                  item['shenhefangshi'], item['daozhangfangshi'], item['zhengxi'], item['platform'], \
                  item['createTime'])
        tx.execute(sql, params)

    def _conditional_insert_zxwk(self, tx, item):
        sql = "delete from t_zxwk where pid = '{}';".format(item['pid'][0])
        tx.execute(sql)

        sql = "insert into t_zxwk(pid,name,edu,qixian,feiyong,fangkuangsudu,shenhefangshi,daozhangfangshi,platform,product,phone,zhengxi,shijidaokuang,category,xuyaoziliao,createTime) " \
              "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        item['createTime'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                           time.localtime(time.time()))
        params = (item["pid"][0], item['name'][0], item['edu'][0],item['qixian'][0], \
                  item['feiyong'][0], item['fangkuangsudu'][0], item['shenhefangshi'][0], item['daozhangfangshi'][0], \
                  item['platform'][0], item['product'][0], item['phone'][0], item['zhengxi'][0], \
                  item['shijidaokuang'][0], item['category'][0], item['xuyaoziliao'][0], item['createTime'])
        tx.execute(sql, params)
        # 写入数据库中

    def _conditional_insert_wangdaijin(self, tx, item):
        sql = "delete from t_wangdaijin where pid = '{}';".format(item['pid'])
        tx.execute(sql)

        sql = "insert into t_wangdaijin(pid,name,ptime,phone,category,edu,qixian,feiyong,shenhefangshi,fangkuangsudu,huankuanfangshi,daozhangfangshi,shijidaokuang,xuyaoziliao,createTime) " \
              "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        item['createTime'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                           time.localtime(time.time()))
        params = (item["pid"], item['name'], item['ptime'], item['phone'], \
                  item['category'], item['edu'], item['qixian'], item['feiyong'], \
                  item['shenhefangshi'], item['fangkuangsudu'], item['huankuanfangshi'], item['daozhangfangshi'], \
                  item['shijidaokuang'], item['xuyaoziliao'], item['createTime'])
        tx.execute(sql, params)

    def _conditional_insert_yetu(self, tx, item):
        sql = "delete from t_yetu where pid = '{}';".format(item['pid'])
        tx.execute(sql)

        sql = "insert into t_yetu(pid,name,edu,fangkuangsudu,qixian,lixi,shenqingtiaojian,xuyaoziliao,shenheshuoming,platform,createTime) " \
              "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        item['createTime'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                           time.localtime(time.time()))
        params = (item["pid"], item['name'], item['edu'], item['fangkuangsudu'], \
                  item['qixian'], item['lixi'], item['shenqingtiaojian'], item['xuyaoziliao'], \
                  item['shenheshuoming'], item['platform'], item['createTime'])
        tx.execute(sql, params)

    def _conditional_insert_law(self, tx, item):
        sql = "delete from t_law where pid = '{}';".format(item['pid'])
        tx.execute(sql)

        sql = "insert into t_law(pid,name,license,address,phone,website,principal,partner,url) " \
              "values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = (item["pid"], item['name'], item['license'], item['address'], \
                  item['phone'], item['website'], item['principal'], item['partner'], \
                  item['url'])
        tx.execute(sql, params)

    def _conditional_insert_law_firm_rank(self, tx, item):
        # sql = "delete from t_lawfirm_rank where pid = '{}';".format(item['pid'])
        # tx.execute(sql)

        sql = "insert into t_lawfirm_rank(pid,rank,name,license,company,address,phone,mobile,email,type,url) " \
              "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = (
        item["pid"], item["rank"], item["name"], item["license"], item["company"], item["address"], item["phone"],
        item["mobile"], item["email"], item["type"], item["url"])
        tx.execute(sql, params)

    def _conditional_insert_cnlawer_rank(self, tx, item):
        # sql = "delete from t_lawfirm_rank where pid = '{}';".format(item['pid'])
        # tx.execute(sql)

        sql = "insert into t_cnlawer_rank(rank,name,address,law,area) " \
              "values(%s,%s,%s,%s,%s)"
        params = (
        item["rank"], item["name"], item["address"], item["law"], item["area"])
        tx.execute(sql, params)


    def _conditional_insert_wxb_data(self, tx, item):
        tx.execute("SET NAMES utf8mb4")
        tx.execute("SET CHARACTER SET utf8mb4")
        tx.execute("SET character_set_connection = utf8mb4")
        sql = "insert into t_wxb(rank_day,category,rank,name,wx_alias,wx_origin_id,describle,pub_total,read_num_max,avg_read_num,avg_like_num,fans_num_estimate,index_scores,qrcode) " \
              "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = (
            item["rank_day"], item["category"], item["rank"], item["name"], item["wx_alias"],
            item["wx_origin_id"], item["desc"], item["pub_total"], item["read_num_max"], item["avg_read_num"],
            item["avg_like_num"], item["fans_num_estimate"], item["index_scores"], item["qrcode"])
        tx.execute(sql, params)

    #错误处理方法
    def _handle_error(self, failue):
        print('--------------database operation exception!!-----------------')
        print(failue)