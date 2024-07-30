# -*- coding: utf-8 -*-
# @Time    : 2023/3/30 17:23
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : test.py
# @Software: PyCharm
import re

from bs4 import BeautifulSoup

from apollo_config import cookie
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',

}

url = 'https://blog.csdn.net/heian_99/article/details/140774948'
response = requests.get(url, headers=headers)
# 检查响应状态码
print(f"Status Code: {response.status_code}")
# 打印响应内容
# 确保请求成功

# 确保请求成功
if response.status_code == 200:
    # 解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找<div class="bar-content">
    bar_content = soup.find('div', class_='bar-content')

    # 确保找到了<div class="bar-content">
    if bar_content:
        # 查找<div class="bar-content">下面的<span class="time">
        time_span = bar_content.find('span', class_='time')

        # 确保找到了<span class="time">
        if time_span:
            # 获取<span class="time">的值
            time_value = time_span.text

            # 使用正则表达式提取时间部分
            match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', time_value)
            if match:
                filtered_time = match.group(0)
                print(f'Filtered Time: {filtered_time}')
            else:
                print('未找到符合的时间格式')
        else:
            print('未找到<span class="time">')
    else:
        print('未找到<div class="bar-content">')
else:
    print(f'请求失败，状态码: {response.status_code}')
