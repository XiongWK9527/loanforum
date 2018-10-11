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
            charset='utf8',  #编码要加上，否则可能出现中文乱码问题
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
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


    #错误处理方法
    def _handle_error(self, failue):
        print('--------------database operation exception!!-----------------')
        print(failue)