# -*- coding: utf-8 -*-
# @Time    : 2023/1/9 17:39
# @Author  : weidongliang
# @Email   : 1794748404@qq.com
# @File    : get_image.py
# @Software: PyCharm
import requests
from lxml import etree
import os

# 创建文件夹
isExists = os.path.exists('./4kdongman')
if not isExists:
    os.makedirs('./4kdongman')

url = 'http://pic.netbian.com/4kdongman/index_%d.html'
headers = {
    'Users-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}

all_list_images=[]
for page in range(1, 6):
    if (page == 1):
        new_url = 'http://pic.netbian.com/4kdongman/'
    else:
        new_url = format(url % page)
    response = requests.get(url=new_url, headers=headers)
    # 设置获取响应数据的编码格式
    response.encoding = 'gbk'
    page_text = response.text

    # 数据解析
    tree = etree.HTML(page_text)
    li_list = tree.xpath('//ul[@class="clearfix"]/li')
    img_list = []
    img_name_list = []
    for li in li_list:
        img_list.append(li.xpath('./a/img/@src')[0])
        img_name_list.append(li.xpath('./a/img/@alt')[0])

    # 获取完整图片url
    img_url_list = []
    for img_url in img_list:
        img_url_list.append('http://pic.netbian.com' + img_url)

    # 提取图片数据



    for i in img_url_list:
        all_list_images.append(i)

print(all_list_images,len(all_list_images))
# count = 1
# for i in img_url_list:
#     img_data = requests.get(url=i, headers=headers).content
#     filePath = './4kdongman/' + str(count) + '.jpg'
#     with open(filePath, 'wb')as fp:
#         fp.write(img_data)
#     print('%s,下载成功' % count)
#     count=count + 1
#
