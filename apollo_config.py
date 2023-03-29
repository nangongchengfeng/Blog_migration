# -*- coding: utf-8 -*-
# @Time    : 2023/3/29 21:30
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : apollo_config.py.py
# @Software: PyCharm
import os


from pyapollos import ApolloClient

print("加载apollo配置")
APOLLO_CONFIG_URL = "config-server-dev.ownit.top"
client = ApolloClient(app_id="qiniuyun", cluster="default",
                      config_server_url='http://' + APOLLO_CONFIG_URL)
# os.environ.get('APOLLO_CONFIG_URL')

# 获取邮箱地址的 账号和密码
accessKey = client.get_value('accessKey')
secretKey = client.get_value('secretKey')
# print(MAIL_USERNAME,MAIL_PASSWORD)
# MySQL 账号和密码

print(accessKey)