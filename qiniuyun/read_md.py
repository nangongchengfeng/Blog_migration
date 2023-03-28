# -*- coding: utf-8 -*-
# @Time    : 2023/3/28 23:10
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : read_md.py
# @Software: PyCharm
import re
import requests
from updata_file import upload_to_qiniu

def get_url(url):
    response = requests.get(url)

    if response.status_code == 200:
        content = response.content
        filename = url.split('/')[-1]
        filepath = f'image/{filename}'
        with open(filepath, 'wb') as f:
            f.write(content)
        url=upload_to_qiniu(filename)
        print(url)


pattern = r'!\[[^\]]*\]\(([^)]+)\)'
with open('SpringBoot集成Apollo和自动注册Consul.md', 'r', encoding='utf-8') as f:
    content = f.read()
    # print(content)

# 使用 re.findall() 函数查找所有匹配的图片地址，并将其保存到列表中
image_urls = re.findall(pattern, content)

# 打印所有匹配的图片地址
for url in image_urls:
    get_url(url)
