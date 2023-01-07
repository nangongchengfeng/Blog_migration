# -*- coding: utf-8 -*-
# @Time    : 2023/1/7 22:01
# @Author  : weidongliang
# @Email   : 1794748404@qq.com
# @File    : blog_article_list.py
# @Software: PyCharm
import requests
from lxml import etree

# 请求头，也可以随机一个请求头用header = {"User-Agent":UserAgent().random}
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
}
# 博主名字,记得换成你要爬取的博主名字
author_name = "heian_99"
# 博主博文页数
page_num = 9

with open("url.txt", "w") as x:
    for index in range(1, page_num + 1):
        # 拼接URL
        page_url = "https://blog.csdn.net/" + author_name + "/article/list/" + str(index)
        # 发送请求,获取响应
        response = requests.get(page_url, headers=header).content
        # 将HTML源码字符串转换尘土HTML对象
        page_html = etree.HTML(response)
        # 博客文章的链接
        csdn_article_link_list = page_html.xpath(
            "//div[@class='article-item-box csdn-tracking-statistics']//h4//a/@href")
        print(csdn_article_link_list)
        for obj in csdn_article_link_list:
            x.write(obj)
            x.write('\n')
x.close()
