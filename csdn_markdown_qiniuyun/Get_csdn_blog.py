# -*- coding: utf-8 -*-
# @Time    : 2023/4/10 15:00
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : mian.py
# @Software: PyCharm
# 使用 csdn的 api 进行获取文章，特使条件，必须使用md语法编辑器（富本编辑器不行）

import json
import os
import uuid
import time
import requests
import datetime
import argparse
import re
from bs4 import BeautifulSoup

from apollo_config import cookie

# 设置请求头
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
}


# 标签管理，获取所有标签 （名称 地址 博客数量）
def request_blog_column(id):
    # 拼接博客首页链接
    urls = 'https://blog.csdn.net/' + id
    # 发送get请求获取响应
    reply = requests.get(url=urls, headers=headers)
    # 使用BeautifulSoup解析响应
    parse = BeautifulSoup(reply.content, "lxml")
    # 查找包含“special-column-name”类名的所有<a>标签
    spans = parse.find_all('a', attrs={'class': 'special-column-name'})

    blog_columns = []
    # 遍历所有<span>标签
    for span in spans:
        # 从<span>标签中提取链接
        href = re.findall(r'href=\"(.*?)\".*?', str(span), re.S)
        href = ''.join(href)

        # 再次发送get请求获取响应
        blog_column_reply = requests.get(url=href, headers=headers)
        # 从响应中提取专栏博客数量
        blogs_num = re.findall(
            r'<a class="clearfix special-column-name" target="_blank" href=\"' + href + '\".*?<span class="special-column-num">(.+?)篇</span>',
            blog_column_reply.text, re.S)
        blogs_column_num = str(blogs_num[0])

        # 获取专栏名
        blog_column = span.text.strip()
        # 根据id和专栏名创建目录
        blog_column_dir = './' + str(id) + '/' + str(blog_column)
        if not os.path.exists(blog_column_dir):
            os.mkdir(blog_column_dir)
        # 从链接中提取博客id
        blog_id = href.split("_")[-1]
        blog_id = blog_id.split(".")[0]
        blog_columns.append([href, blog_column, blog_id, blogs_column_num])

    # 返回包含链接、专栏名、博客id、专栏博客数量的嵌套列表
    return blog_columns


# 获取 博客 所有博客的信息（分栏，url 标题）
def request_blog_list(id):
    # 获取所有专栏博客信息的嵌套列表
    # blog_columns = request_blog_column(id)
    blog_columns = [['https://blog.csdn.net/heian_99/category_11822490.html', 'Jenkins', '11822490', '7']]
    blogs = []
    # 遍历专栏博客信息的嵌套列表
    for blog_column in blog_columns:
        blog_column_url = blog_column[0]
        blog_column_name = blog_column[1]
        blog_column_id = blog_column[2]
        blog_column_num = int(blog_column[3])
        # 如果专栏博客数量大于40，一页的篇数为40，需要翻页
        if blog_column_num > 40:
            # 计算翻页数量
            page_num = round(blog_column_num / 40)
            # 倒序循环翻页链接
            for i in range(page_num, 0, -1):
                # 拼接翻页链接
                blog_column_url = blog_column[0]
                url_str = blog_column_url.split('.html')[0]
                blog_column_url = url_str + '_' + str(i) + '.html'
                # 将文章信息追加到文章列表中
                append_blog_info(blog_column_url, blog_column_name, blogs)
            # 获取第一页的文章列表信息
            blog_column_url = blog_column[0]
            blogs = append_blog_info(blog_column_url, blog_column_name, blogs)
        # 如果专栏博客数量小于等于40
        else:
            # 获取专栏第一页的文章列表信息
            blogs = append_blog_info(blog_column_url, blog_column_name, blogs)
    # 返回所有文章的信息
    print(blogs)
    return blogs


# 往文章列表中追加文章信息
"""
该函数接受三个参数，分别为专栏博客的url，专栏博客的名称和用于存储文章信息的列表。该函数会发送get请求，获取专栏博客的响应，并使用BeautifulSoup解析响应。
随后，该函数会定位到网页中的所有class="column_article_list"的<ul>标签，遍历每个<ul>标签，提取封装着文章信息的<li>标签，再提取出每篇文章的链接和标题，
存储在一个字典中，最后将字典追加到传入的列表中。该函数返回存储着所有文章信息的列表。
"""


def append_blog_info(blog_column_url, blog_column_name, blogs):
    # 发送get请求，获取响应
    reply = requests.get(url=blog_column_url, headers=headers)
    # 使用BeautifulSoup解析响应
    blog_span = BeautifulSoup(reply.content, "lxml")
    # 获取所有的class="column_article_list"的<ul>标签
    blogs_list = blog_span.find_all('ul', attrs={'class': 'column_article_list'})
    # 遍历所有的<ul>标签
    for arch_blog_info in blogs_list:
        # 获取<ul>标签内所有的<li>标签
        blogs_list = arch_blog_info.find_all('li')
        # 遍历所有的<li>标签
        for blog_info in blogs_list:
            # 获取<li>标签内的文章链接和标题
            blog_url = blog_info.find('a', attrs={'target': '_blank'})['href']
            blog_title = blog_info.find('h2', attrs={'class': "title"}).get_text().strip().replace(" ", "_").replace(
                '/', '_')
            # 将文章信息存储在字典中
            blog_dict = {'column': blog_column_name, 'url': blog_url, 'title': blog_title}
            # 将字典追加到文章列表中
            blogs.append(blog_dict)
    # 返回所有文章的信息
    return blogs


"""
从博客链接中提取文章id
构造请求链接和请求头部
执行get请求，获取博客内容的json响应数据
根据响应数据提取文章正文，并替换掉@[toc]
根据博客标题和博客所属专栏，在指定的目录下创建一个以文章标题命名的.md文件，并将文章正文写入该文件中。
"""


# 通过文章id获取文章内容，并将其保存为.md文件
def request_md(id):
    # 获取指定id的博客列表
    # blogs = request_blog_list(id)
    blogs = [{'column': 'Nginx', 'url': 'https://blog.csdn.net/heian_99/article/details/130058875',
              'title': 'Nginx模板自动化'}]

    # 遍历博客列表中所有文章
    for blog_dict in blogs:
        blog_url = blog_dict['url']
        blog_title = blog_dict['title']
        blog_column = blog_dict['column']
        # 从博客链接中提取文章id
        blog_id = blog_url.split("/")[-1]
        # 构造请求链接
        url = f"https://blog-console-api.csdn.net/v1/editor/getArticle?id={blog_id}"
        # 构造请求头部
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Cookie': cookie,
        }
        # 构造请求数据
        data = {"id": blog_id}
        reply = requests.get(url, headers=headers, data=data)
        # 将请求的json响应数据转为字典类型
        reply_data = reply.json()
        print(reply_data)
        try:
            key = "key" + str(uuid.uuid4())
            # 提取文章正文
            content = reply_data["data"]["markdowncontent"].replace("@[toc]", "")
            # 构造文章标题存储路径，如'./1/Nginx/Nginx模板自动化.md'
            blog_title_dir = './' + str(id) + '/' + str(blog_column) + '/' + str(blog_title) + '.md'
            # 将文章正文保存为.md文件
            with open(blog_title_dir, "w", encoding="utf-8") as f:
                f.write(content)
            # 打印日志
            print("download blog markdown blog:" + '【' + blog_column + '】' + str(blog_title))
        except Exception as e:
            print("***********************************")
            print(e)
            print(url)


def read_from_json(filename):
    jsonfile = open(filename, "r", encoding='utf-8')
    jsondata = jsonfile.read()
    return json.loads(jsondata)


def write_to_json(filename, data):
    jsonfile = open(filename, "w")
    jsonfile.write(data)


def main():
    # parser = argparse.ArgumentParser()
    #
    # parser.add_argument('-i', '--id', dest='id', type=str, required=True, help='csdn name')
    #
    # args = parser.parse_args()
    #
    # csdn_id = args.id
    csdn_id = 'heian_99'
    name_dir = './' + str(csdn_id)
    if not os.path.exists(name_dir):
        os.mkdir(name_dir)

    request_md(csdn_id)


if __name__ == '__main__':
    # main()
    request_blog_list('heian_99')

