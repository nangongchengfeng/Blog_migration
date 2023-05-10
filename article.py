# -*- coding: utf-8 -*-
# @Time    : 2023/5/10 18:21
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : article.py
# @Software: PyCharm

# 标签管理，获取所有标签 （名称 地址 博客数量）
import os
import re


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
        # 解析 HTML，获取关注数、文章数、文章阅读量和文章收藏量
        soup = BeautifulSoup(blog_column_reply.text, 'html.parser')
        column_operating_div = soup.find('div', {'class': 'column_operating'})
        subscribe_num_span = column_operating_div.find('span', {'class': 'column-subscribe-num'}).text
        article_num_span = column_operating_div.find_all('span', {'class': 'mumber-color'})[1].text
        read_num_span = column_operating_div.find_all('span', {'class': 'mumber-color'})[2].text
        collect_num_span = column_operating_div.find_all('span', {'class': 'mumber-color'})[3].text

        # 打印获取到的数据
        # print('关注数：', subscribe_num_span)
        # print('文章数：', article_num_span)
        # print('文章阅读量：', read_num_span)
        # print('文章收藏量：', collect_num_span)
        # exit(1)
        # 从响应中提取专栏博客数量
        blogs_num = re.findall(
            r'<a class="clearfix special-column-name" target="_blank" href=\"' + href + '\".*?<span class="special-column-num">(.+?)篇</span>',
            blog_column_reply.text, re.S)
        blogs_column_num = str(blogs_num[0])

        # 获取专栏名
        blog_column = span.text.strip()

        # 从链接中提取博客id
        blog_id = href.split("_")[-1]
        blog_id = blog_id.split(".")[0]
        blog_columns.append([href, blog_column, blog_id, blogs_column_num,subscribe_num_span,article_num_span,read_num_span,collect_num_span])
    print(blog_columns)
    # 返回包含链接、专栏名、博客id、专栏博客数量的嵌套列表
    return blog_columns



# 往文章列表中追加文章信息
"""
该函数接受三个参数，分别为专栏博客的url，专栏博客的名称和用于存储文章信息的列表。该函数会发送get请求，获取专栏博客的响应，并使用BeautifulSoup解析响应。
随后，该函数会定位到网页中的所有class="column_article_list"的<ul>标签，遍历每个<ul>标签，提取封装着文章信息的<li>标签，再提取出每篇文章的链接和标题，
存储在一个字典中，最后将字典追加到传入的列表中。该函数返回存储着所有文章信息的列表。
"""
import requests
from bs4 import BeautifulSoup
# 设置请求头
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
}


def append_blog_info(blog_column_url, blog_column_name, blogs):
    # 发送get请求，获取响应
    reply = requests.get(url=blog_column_url, headers=headers)
    # 使用BeautifulSoup解析响应
    blog_span = BeautifulSoup(reply.content, "lxml")
    # print(blog_span)
    # 获取所有的class="column_article_list"的<ul>标签
    blogs_list = blog_span.find_all('ul', attrs={'class': 'column_article_list'})
    print(blog_column_url, blog_column_name, blogs)
    return blogs



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



if __name__ == '__main__':
    # main()
    request_blog_column('heian_99')
