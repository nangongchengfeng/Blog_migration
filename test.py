# -*- coding: utf-8 -*-
# @Time    : 2023/4/17 17:59
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : test.py
# @Software: PyCharm
import pandas as pd
import requests
import threading

from sqlalchemy import create_engine

url = 'https://www.ownit.top/assets/image-20230223143809-kejqe1e.png'

def request_image():
    while True:
        try:
            requests.get(url)
        except:
            pass

# # 启动多个线程发送请求
# for i in range(100):
#     threading.Thread(target=request_image).start()

# 连接数据库
engine = create_engine('mysql+pymysql://root:123456@192.168.102.20/csdn?charset=utf8')
def get_catego():
    """获取当日最新的文章数据"""
    # 设置pandas参数，使其以完整显示模式打印DataFrame
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', None)
    # pd.set_option('display.max_colwidth', -1)

    df = pd.read_sql("categorize", con=engine)
    df['categorize'] = df['categorize']
    df['read_num'] = df['read_num']

    print(df)

if __name__ == '__main__':
    get_catego()