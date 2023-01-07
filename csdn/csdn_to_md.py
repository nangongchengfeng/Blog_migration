# -*- coding: utf-8 -*-
# @Time    : 2023/1/7 21:54
# @Author  : weidongliang
# @Email   : 1794748404@qq.com
# @File    : csdn_to_md.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
# @Time    : 2023/1/7 14:49
# @Author  : weidongliang
# @Email   : 1794748404@qq.com
# @File    : blog.py
# @Software: PyCharm
import os
import re

import parsel
import requests
import tomd


def get_article_info(url):
    html = requests.get(url, headers=headers).text
    print(html)
    selector = parsel.Selector(html)
    ##articleMeList-blog > div.article-list > div > h4 > a
    urls = selector.css('.mainContent').xpath('.//@href').getall()
    print(urls)
    print('共找到%d篇文章...' % len(urls))
    return urls


def get_html_from_csdn(url):
    html = requests.get(url, headers=headers).text
    selector = parsel.Selector(html)
    title = selector.css('div.article-title-box > h1::text').get()
    article = selector.css('div.article_content').get()
    category = selector.css('div.blog-tags-box > div > a::text').getall()[0]
    tags = selector.css('div.blog-tags-box > div > a[data-report-click*="mod"]::text').getall()
    time_stamp = selector.css('div > span.time::text').get()
    author = selector.css('#uid > span.name::text').get()
    origin = url
    return title, article, category, tags, time_stamp, author, origin


def html_to_md(title, article, category, tags, time_stamp, author, origin):
    md = tomd.convert(article)
    # 图片url标准化
    url_pattern = re.compile(r'<img.*?(https://.*?\.gif|https://.*?\.png).*?">')
    for src_url in url_pattern.finditer(md):
        img_name = src_url.group(1).split('/')[-1]
        md = md.replace(src_url.group(0), '![%s](%s)' % (img_name, src_url.group(1)))
    print('正在下载 %s' % title)
    # text = "> 标题: %s <br> 日期: %s<br> 标签: [%s]<br> 分类: %s<br> \n\n> 作者: %s\n> 原文链接: %s\n%s" % (
    #     title, time_stamp, ', '.join(tags), category, author, origin, md)
    text = "---\ntitle: %s\ndate: %s\ntags: [%s]\ncategories: %s\n---\n\n> 作者: %s\n> 原文链接: %s\n%s" % (
        title, time_stamp, ', '.join(tags), category, author, origin, md)
    # Windows下文件名字不能包含特殊符号
    file_name = re.sub(r'[\\/:*?"<>|]', ' ', title)
    with open('articles/%s.md' % file_name.strip(), 'w', encoding='utf-8') as f:
        f.write(text)


def main(url):
    if not os.path.exists('articles'):
        os.mkdir('articles')
    article_urls = get_article_info(url)
    for article_url in article_urls:
        title, article, category, tags, time_stamp, author, origin = get_html_from_csdn(article_url)
        html_to_md(title, article, category, tags, time_stamp, author, origin)
    print('完成%d篇文章的下载' % len(article_urls))


if __name__ == '__main__':
    headers = {
        'Host': 'blog.csdn.net',
        'Referer': 'https://blog.csdn.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3542.0 Safari/537.36'
    }
    start_url = "https://blog.csdn.net/heian_99"
    main(start_url)
