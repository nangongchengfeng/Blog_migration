+++
author = "南宫乘风"
title = "Python开发mysql和mongo 连接类"
date = "2022-07-25 17:44:50"
tags=['mysql', 'mongodb', '数据库']
categories=['Python学习']
image = "post/4kdongman/15.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/125979933](https://blog.csdn.net/heian_99/article/details/125979933)

因为业务需求，需要连接数据库查询数据

数据库类型：mysql，mongodb

需求：有中连机制，读取配置文件，可实例化，有日志记录

![e42eaabb593245b2a93aecbc1baac682.png](https://img-blog.csdnimg.cn/e42eaabb593245b2a93aecbc1baac682.png)

 

## 配置文件

dbconfig.conf

```
[Mongodbtest]
host=192.168.99.42
port=27018
user=
password=
database=ace_sms


[mysql]
host=192.168.99.42
port=27018
user=
password=
database=ace_sms
```

## 日志类

```
# -*- coding: utf-8 -*-
# @Time    : 2022/7/12 18:13
# @File    : Loggers.py
# @Software: PyCharm
# 加入日志
# 获取logger实例
import logging
import os
import sys

logger = logging.getLogger("baseSpider")
# 指定输出格式
formatter = logging.Formatter('%(asctime)s\
            %(filename)s-%(lineno)d\
            %(levelname)s\
            %(message)s')
# 文件日志
# 获取当前文件路径
current_path = os.path.abspath(os.path.dirname(__file__))
father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
log_file_path = os.path.join(father_path + "\logs\dingding_message.log")

file_handler = logging.FileHandler(log_file_path)
file_handler.setFormatter(formatter)
# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# 为logge添加具体的日志处理器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.setLevel(logging.INFO)

```

## mysql连接类

```
# -*- coding: utf-8 -*-
# @Time    : 2022-07-08 21:32

# @File    : MyDB.py
# @Software: PyCharm
import time

import pymysql

import configparser
import logging
import sys

from tool.Loggers import logger


class mysql:
    def __init__(self, config_file, db):
        """

        :param config_file:
        :param db:
        """
        # 实例化configparser
        config = configparser.ConfigParser()
        # 从配置文件中读取数据库的相关信息

        config.read(config_file, encoding='utf-8')
        self.host = config[db]['host']
        self.port = int(config[db]['port'])
        self.user = config[db]['user']
        self.password = config[db]['password']
        self.database = config[db]['database']
        self.db = db
        self.conn = None
        self._conn()

    def _conn(self):
        try:
            logger.info(f"读取环境：{self.db}，连接信息：主机ip：{self.host},端口：{self.port},用户：{self.user},连接数据库：{self.database}")
            self.conn = pymysql.Connection(host=self.host, user=self.user, password=self.password,
                                           database=self.database, port=self.port)
            logger.info(f"数据库: {self.database}初始化连接成功")
            return True
        except  Exception as e:
            logger.error(f"数据库: {self.database}初始化连接失败，错误：{e}")
            return False

    def close(self):
        self.conn.close()
        logger.info(f"数据库关闭成功")

    def _reConn(self, num=28800, stime=3):  # 重试连接总次数为1天,这里根据实际情况自己设置,如果服务器宕机1天都没发现就......
        _number = 0
        _status = True
        logger.info(f"检查数据库{self.database}连通性,连接IP：{self.host}")
        while _status and _number &lt;= num:
            try:
                self.conn.ping()  # cping 校验连接是否异常
                _status = False
                logger.info(f"数据库{self.database}连接============正常,连接IP：{self.host} ")
            except:
                if self._conn() == True:  # 重新连接,成功退出
                    _status = False
                    break
                _number += 1
                logger.info(f"数据库{self.database}连接============失败,连接IP：{self.host} ")
                time.sleep(stime)  # 连接不成功,休眠3秒钟,继续循环，知道成功或重试次数结束

    def select(self, sql=''):
        try:
            self._reConn()
            logger.info('查询的语句:%s' % sql)
            # 建立游标
            db_cursor = self.conn.cursor()
            db_cursor.execute(sql)
            result = db_cursor.fetchall()
            # 返回值和数据表字段组成json格式
            lists = []
            t = 0
            for x in result:
                i = 0
                onelist = {}
                for field in db_cursor.description:
                    onelist[field[0]] = x[i]
                    i = i + 1
                lists.append(onelist)
            logger.info('组合数据:%s' % lists)
            return lists
            # return result
        except pymysql.Error as e:
            logger.error('数据库查询数据失败：%s' % e)
            return False

    def select_limit(self, sql='', offset=0, length=20):
        sql = '%s limit %d , %d ;' % (sql, offset, length)
        return self.select(sql)

    # # 插入
    # def execute_insert(self, query):
    #     print('query:%s' % query)
    #     try:
    #         # 建立游标
    #         db_cursor = self.dbconn.cursor()
    #         db_cursor.execute(query)
    #         db_cursor.execute('commit')
    #         return True
    #     except Exception as e:
    #         print('数据库插入数据失败：%s' % e)
    #         # 事务回滚
    #         db_cursor.execute('rollback')
    #         db_cursor.close()
    #         exit()

```

## MongoDB连接类



```
# -*- coding: utf-8 -*-
# @Time    : 2022/7/12 10:44
# @File    : MongoDB.py
# @Software: PyCharm


import configparser
import time

import pymongo

from alarm.tool.Loggers import logger


class mongo(object):
    def __init__(self, config_file, db):
        """

        :param config_file: 配置文件路径
        :param db: 获取配置的环境
        """
        # 实例化configparser
        config = configparser.ConfigParser()
        # 从配置文件中读取数据库的相关信息

        config.read(config_file, encoding='utf-8')
        self.host = config[db]['host']
        self.port = int(config[db]['port'])
        self.user = config[db]['user']
        self.password = config[db]['password']
        self.database = config[db]['database']
        self.db = db
        self.conn = None
        self._conn()

    def _conn(self):
        try:
            logger.info(f"读取环境：{self.db}，连接信息：主机ip：{self.host},端口：{self.port},用户：{self.user},连接数据库：{self.database}")
            # self.conn = pymongo.MongoClient(host=self.host,
            #                                 port=self.port)
            self.conn = pymongo.MongoClient(host=self.host,
                                            port=self.port)  # username=self.user, password=self.password
            # self.db_conn = self.conn[self.database]
            # self.db_conn=self.db_conn.authenticate(self.user,self.password)
            self.conn[self.database].authenticate(self.user, self.password, self.database)
            self.db_conn = self.conn[self.database]
            if self.conn.server_info():
                logger.info(f"数据库: {self.database}初始化连接成功")
                return True
        except  Exception as e:
            logger.error(f"数据库: {self.database}初始化连接失败，错误：{e}")
            return False

    # MongoDB数据库关闭
    def close(self):
        self.conn.close()
        logger.info(f"数据库关闭成功")

    # 查询调用状态
    def get_state(self):
        return self.conn is not None  # and self.db_conn is not None

    def _reConn(self, num=28800, stime=3):  # 重试连接总次数为1天,这里根据实际情况自己设置,如果服务器宕机1天都没发现就......
        _number = 0
        _status = True
        logger.info(f"检查数据库{self.database}连通性,连接IP：{self.host}")
        while _status and _number &lt;= num:
            try:
                self.conn.server_info()  # 检查数据库是否正常连通
                _status = False
                logger.info(f"数据库{self.database}连接============正常,连接IP：{self.host} ")
            except:
                if self._conn() == True:  # 重新连接,成功退出
                    _status = False
                    break
                _number += 1
                logger.info(f"数据库{self.database}连接============失败,连接IP：{self.host} ")
                time.sleep(stime)  # 连接不成功,休眠3秒钟,继续循环，知道成功或重试次数结束

    def insert_one(self, collection, data):
        self._reConn()
        if self.get_state():
            ret = self.db_conn[collection].insert_one(data)
            return ret.inserted_id
        else:
            return ""

    def insert_many(self, collection, data):
        if self.get_state():
            ret = self.db_conn[collection].insert_many(data)
            return ret.inserted_id
        else:
            return ""

    def update(self, collection, data):
        # data format:
        # {key:[old_data,new_data]}
        data_filter = {}
        data_revised = {}
        for key in data.keys():
            data_filter[key] = data[key][0]
            data_revised[key] = data[key][1]
        if self.get_state():
            return self.db_conn[collection].update_many(data_filter, {"$set": data_revised}).modified_count
        return 0

    def find(self, col, condition, column=None):
        """
        查询数据代码
        :param col: 数据库中的集合
        :param condition: 查询条件,查询条件必须是个字典
        :param column: find 的第二个参数是可选的，可以指定需要返回的键。这个特别的 "$slice" 运算符可以返回一个数组键中元素的子集。
        :return: list 返回查询到记录的列表
        """
        # print(col, condition)
        # data= self.db_conn["sms_log"]
        # data=self.db_conn["sms_log"].find({"status":"2","createTime":{"$gte": "2022/07/12 22:18:26"}},{"status":1,"channelCode":1,"_id":0})
        # data = self.db_conn["authCode"].find({"use": False,"createdTime": {"$gte": 1657865035}})
        # print(list(data))
        self._reConn()
        if self.get_state():
            if column is None:
                return list(self.db_conn[col].find(condition))
            else:
                return list(self.db_conn[col].find(condition, column))
        else:
            return None

    def get_last_data(self, col, number=1):
        if self.get_state():
            # last_data = list(self.db_conn["authCode"].find().sort("_id", -1 ).limit(50))

            last_data = list(self.db_conn[col].find().sort("_id", -1).limit(number))
            return last_data

    def delete(self, col, condition):
        if self.get_state():
            return self.db_conn[col].delete_many(filter=condition).deleted_count
        return 0

    def aggregate(self, col, condition):
        if self.get_state():
            return list(self.db_conn[col].aggregate(condition))


# 时间戳转换时间
def timestamp_to_time(timestamp):
    timeArray = time.localtime(timestamp)  # 转换为可用的时间，就是下面的%Y %m %d
    # day_time = time.strftime("%Y-%m-%d", timeArray)  # 取上面的timeArray中的对应值0
    second_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)  # 这个一样的
    return second_time  # 返回相应的值


# 时间转换时间戳
def time_to_timestamp(time_str):
    # 转换成时间数组
    timeArray = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    # 转换成时间戳
    timestamp = time.mktime(timeArray)
    # print(timestamp)
    return timestamp


if __name__ == '__main__':
    logger.info("开始实例化数据库对象 ")
    config_file = '../config/dbconfig.conf'
    db = 'Devfubaodai'
    db = mongo(config_file, db)

    # 获取时间
    data_time = '2022-07-18 00:00:00'
    timestamp = time_to_timestamp(data_time)
    # print(timestamp)
    data = db.get_last_data("authCode", 1)
    last_time_data = data[0]["createdTime"]
    satrt_time_data = data[0]["createdTime"]-600
    print(timestamp_to_time(last_time_data))
    print(timestamp_to_time(satrt_time_data))
    data = db.find("authCode", {"createdTime": {"$gte": satrt_time_data, "$lte": last_time_data}}, {"name": 1, "use": 1, "_id": 0})
    num, fail = 0, 0
    for i in data:
        num += 1
        print(i)
    print(num)
    # logger.info(f"短信---最新50条数据，成功使用数量：{num}，未使用的数量：{fail}")

    db.close()
    logger.info("--------------------------------------------------------------------------------------------------")

```

## mian类

```
def main():
    #mysqld_test()
     schedule.every(1).minutes.do(mysqld_test)
     while True:
         schedule.run_pending()
         time.sleep(1)


if __name__ == '__main__':
    res = os.path.abspath(__file__)  # 获取当前文件的绝对路径
    print(res)
    base_path = os.path.dirname(os.path.dirname(res))  # 获取当前文件的上两级目录
    print(base_path)
    base_path2 = os.path.dirname(res)
    print(base_path2)
    sys.path.append(base_path2)
    sys.path.append(base_path)
    sys.path.insert(0, base_path)  # 加入环境变量
    # 以上5行代码必须要加入到文件的最上方
    print(sys.path)
    main()

```


