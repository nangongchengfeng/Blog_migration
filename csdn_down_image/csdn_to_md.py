# @Software: PyCharm
# -*- coding: utf-8 -*-
# @Time    : 2023/1/7 14:49
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : blog.py
# @Software: PyCharm
import os
import random
import re
from datetime import datetime, timedelta

import chardet
import parsel
import requests
import tomd

# 正则中的%s分割
from bs4 import BeautifulSoup

splits = [
    {1: [('年', '月', '日', '点', '分', '秒'), ('-', '-', '', ':', ':', ''), ('\/', '\/', '', ':', ':', ''),
         ('\.', '\.', '', ':', ':', '')]},
    {2: [('年', '月', '日', '点', '分'), ('-', '-', '', ':', ''), ('\/', '\/', '', ':', ''),
         ('\.', '\.', '', ':', '')]},
    {3: [('年', '月', '日'), ('-', '-', ''), ('\/', '\/', ''), ('\.', '\.', '')]},
    {4: [('年', '月', '日'), ('-', '-', ''), ('\/', '\/', ''), ('\.', '\.', '')]},

    {5: [('月', '日', '点', '分', '秒'), ('-', '', ':', ':', ''), ('\/', '', ':', ':', ''), ('\.', '', ':', ':', '')]},
    {6: [('月', '日', '点', '分'), ('-', '', ':', ''), ('\/', '', ':', ''), ('\.', '', ':', '')]},
    {7: [('月', '日'), ('-', ''), ('\/', ''), ('\.', '')]},

    {8: [('点', '分', '秒'), (':', ':', '')]},
    {9: [('点', '分'), (':', '')]},
]

# 匹配正则表达式
matchs = {
    1: (r'\d{4}%s\d{1,2}%s\d{1,2}%s \d{1,2}%s\d{1,2}%s\d{1,2}%s', '%%Y%s%%m%s%%d%s %%H%s%%M%s%%S%s'),
    2: (r'\d{4}%s\d{1,2}%s\d{1,2}%s \d{1,2}%s\d{1,2}%s', '%%Y%s%%m%s%%d%s %%H%s%%M%s'),
    3: (r'\d{4}%s\d{1,2}%s\d{1,2}%s', '%%Y%s%%m%s%%d%s'),
    4: (r'\d{2}%s\d{1,2}%s\d{1,2}%s', '%%y%s%%m%s%%d%s'),

    # 没有年份
    5: (r'\d{1,2}%s\d{1,2}%s \d{1,2}%s\d{1,2}%s\d{1,2}%s', '%%m%s%%d%s %%H%s%%M%s%%S%s'),
    6: (r'\d{1,2}%s\d{1,2}%s \d{1,2}%s\d{1,2}%s', '%%m%s%%d%s %%H%s%%M%s'),
    7: (r'\d{1,2}%s\d{1,2}%s', '%%m%s%%d%s'),

    # 没有年月日
    8: (r'\d{1,2}%s\d{1,2}%s\d{1,2}%s', '%%H%s%%M%s%%S%s'),
    9: (r'\d{1,2}%s\d{1,2}%s', '%%H%s%%M%s'),
}

parten_other = '\d+天前|\d+分钟前|\d+小时前|\d+秒前'


class TimeFinder(object):

    def __init__(self, base_date=None):
        self.base_date = base_date
        self.match_item = []

        self.init_args()
        self.init_match_item()

    def init_args(self):
        # 格式化基础时间
        if not self.base_date:
            self.base_date = datetime.now()
        if self.base_date and not isinstance(self.base_date, datetime):
            try:
                self.base_date = datetime.strptime(self.base_date, '%Y-%m-%d %H:%M:%S')
            except Exception as e:
                raise Exception('type of base_date must be str of%Y-%m-%d %H:%M:%S or datetime')

    def init_match_item(self):
        # 构建穷举正则匹配公式 及提取的字符串转datetime格式映射
        for item in splits:
            for num, value in item.items():
                match = matchs[num]
                for sp in value:
                    tmp = []
                    for m in match:
                        tmp.append(m % sp)
                    self.match_item.append(tuple(tmp))

    def get_time_other(self, text):
        m = re.search('\d+', text)
        if not m:
            return None
        num = int(m.group())
        if '天' in text:
            return self.base_date - timedelta(days=num)
        elif '小时' in text:
            return self.base_date - timedelta(hours=num)
        elif '分钟' in text:
            return self.base_date - timedelta(minutes=num)
        elif '秒' in text:
            return self.base_date - timedelta(seconds=num)

        return None

    def find_time(self, text):
        # 格式化text为str类型
        if isinstance(text, bytes):
            encoding = chardet.detect(text)['encoding']
            text = text.decode(encoding)

        res = []
        parten = '|'.join([x[0] for x in self.match_item])

        parten = parten + '|' + parten_other
        match_list = re.findall(parten, text)
        if not match_list:
            return None
        for match in match_list:
            for item in self.match_item:
                try:
                    date = datetime.strptime(match, item[1].replace('\\', ''))
                    if date.year == 1900:
                        date = date.replace(year=self.base_date.year)
                        if date.month == 1:
                            date = date.replace(month=self.base_date.month)
                            if date.day == 1:
                                date = date.replace(day=self.base_date.day)
                    res.append(datetime.strftime(date, '%Y-%m-%d %H:%M:%S'))
                    break
                except Exception as e:
                    date = self.get_time_other(match)
                    if date:
                        res.append(datetime.strftime(date, '%Y-%m-%d %H:%M:%S'))
                        break
        if not res:
            return None
        return res


# 判断目录是否存在，不存在则创建
def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def handleDate(time_str):
    result = None
    # 定义日期格式
    timefinder = TimeFinder(base_date='2020-01-01 00:00:00')
    parsed_time = timefinder.find_time(time_str.replace("\t", "").replace("\n", ""))
    if parsed_time is None:
        if time_str.find("年") >= 0:
            parsed_time = timefinder.find_time(time_str.replace(" ", "").replace("\t", ""))
            if parsed_time is not None:
                result = parsed_time[0]
    else:
        result = parsed_time[0]
    return result


# 返回图片地址
def get_images_url():
    list_image = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
                  '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34',
                  '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51',
                  '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68',
                  '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85',
                  '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99']
    x = random.choice(list_image)
    image_url = f"post/4kdongman/{x}.jpg"
    return image_url


def get_article_info(url):
    html = requests.get(url, headers=headers).text
    # print(html)
    selector = parsel.Selector(html)
    ##articleMeList-blog > div.article-list > div > h4 > a
    urls = selector.css('.mainContent').xpath('.//@href').getall()
    # print(urls)
    urls = ['https://blog.csdn.net/heian_99/article/details/129614899?spm=1001.2014.3001.5502']
    # urls = []
    # urls.append('https://blog.csdn.net/heian_99/article/details/127610131')
    print('共找到%d篇文章...' % len(urls))
    return urls


def get_html_from_csdn(url):
    html = requests.get(url, headers=headers).text
    # print(html)
    selector = parsel.Selector(html)
    title = selector.css('div.article-title-box > h1::text').get()
    article = selector.css('div.article_content').get()
    category = selector.css('div.blog-tags-box > div > a::text').getall()

    category_list = []
    for i in category:
        list_ca = i.replace('#', '')
        category_list.append(list_ca)

    tags = selector.css('div.blog-tags-box > div > a[data-report-click*="mod"]::text').getall()

    result = filter(lambda x: x not in tags, category_list)

    category_list = list(result)
    time_stamp = selector.css('div > span.time::text').get()
    author = selector.css('#uid > span.name::text').get()
    origin = url
    return title, article, category_list, tags, time_stamp, author, origin


def html_to_md(title, article, category_list, tags, time_stamp, author, origin):
    article_a = re.sub(r'<a[^>]*>(.*?)</a>', r'\1', article)
    article_strong= re.sub(r'<strong[^>]*>(.*?)</strong>', r'\1', article_a)
    article_strong = re.sub(r'<strong[^>]*>(.*?)</strong>', r'\1', article_strong)
    md = tomd.convert(article_strong)
    # 传入的html界面
    print("============================================================")
    # 1、获取文章内容中所有 图片的地址
    url_pattern = re.compile(r'<img.*?(https://.*?\.gif|https://.*?\.png).*?">')

    print(url_pattern)
    print(md)

    # 图片url标准化
    print("============================================================")
    for src_url in url_pattern.finditer(md):
        img_name = src_url.group(1).split('/')[-1]
        md_img = f'![{img_name}](images/{img_name})'
        md = md.replace(src_url.group(0), md_img)

    print("============================================================")

    time_stamp = handleDate(time_stamp)
    # file_dir = time_stamp.split(" ")[0]
    year = time_stamp.split("-")[0]
    month = time_stamp.split("-")[1]
    dir_file = "articles/" + year + "/" + month
    images_dir = "articles/" + year + "/" + month + '/images/'
    create_directory_if_not_exists(images_dir)
    create_directory_if_not_exists(dir_file)
    # 2、 下载图片
    for url in url_pattern.findall(article):
        response = requests.get(url)
        # 保存图片到本地文件夹
        with open(images_dir + url.split('/')[-1], 'wb') as f:
            f.write(response.content)
    print('正在下载 %s' % title)
    # text = "> 标题: %s <br> 日期: %s<br> 标签: [%s]<br> 分类: %s<br> \n\n> 作者: %s\n> 原文链接: %s\n%s" % (
    #     title, time_stamp, ', '.join(tags), category, author, origin, md)

    ########################
    # text = "+++ \ntitle: %s\ndate: %s\ntags: [%s]\ncategories: %s\n---\n\n> author: %s\n> 原文链接: %s +++\n%s" % (
    #     title, time_stamp, ', '.join(tags), category, author, origin, md)
    url_image = get_images_url()
    text = f"""+++\nauthor = "{author}"\ntitle = "{title}"\ndate = "{time_stamp}"\ntags={tags}\ncategories={category_list}\nimage = "{url_image}"\n+++\n[作者：{author}   原文链接:{origin}]({origin})\n{md}"""
    ########################
    # Windows下文件名字不能包含特殊符号

    file_name = re.sub(r'[\\/:*?"<>|]', ' ', title)
    with open('%s/%s.md' % (dir_file, file_name.strip()), 'w', encoding='utf-8') as f:
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
