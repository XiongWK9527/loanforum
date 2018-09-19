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

    #写入数据库中
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

    #错误处理方法
    def _handle_error(self, failue):
        print('--------------database operation exception!!-----------------')
        print(failue)