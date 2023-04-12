# -*- coding: utf-8 -*-
# @Time    : 2023/4/10 15:00
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : mian.py
# @Software: PyCharm
# 使用 csdn的 api 进行获取文章，特使条件，必须使用md语法编辑器（富本编辑器不行）

import json
import os

import parsel
import requests
from datetime import datetime
import argparse
import re
from bs4 import BeautifulSoup
import frontmatter
from apollo_config import cookie
import random

from qiniuyun.updata_file import upload_to_qiniu

# 设置请求头


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
}


# 把 字符串 转换为时间格式
def str_to_datetime(datetime_str):
    """
    将字符串格式的日期时间转换为 datetime 对象。
    :param datetime_str: 字符串格式的日期时间，如 '2023-04-10 14:29:25'。
    :return: datetime 对象，表示相同的日期时间。
    """
    try:
        datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        raise ValueError(f'无效的日期时间格式：{datetime_str}') from e
    return datetime_obj


# 根据图片的url 下载到本地，在上传到七牛云

def get_url(url):
    response = requests.get(url)

    if response.status_code == 200:
        content = response.content
        if 'imgconvert.csdnimg.cn/' in url:
            return url.split('/')[-1]
        elif len(url) > 55:

            filename_pattern = r'/([\w-]+\.(?:jpg|png|gif|jpeg))'
            # filename = url.split('/')[-1]
            filename = re.findall(filename_pattern, url)[-1]
        else:
            filename = url.split('/')[-1]
        filepath = f'images/{filename}'
        # print(filename)
        with open(filepath, 'wb') as f:
            f.write(content)
        url = upload_to_qiniu(filename)
        # print(url)
        return url


# 获取标题页的图片
def random_get_url():
    # 生成数字列表，替换原始的图片编号列表，使用zfill()函数将数字转换成两位数，例如1变成'01'，方便拼接url
    nums = [str(i + 1).zfill(2) for i in range(102)]
    x = random.choice(nums)  # 随机选择一个数字作为图片编号
    image_url = f"http://image.ownit.top/4kdongman/{x}.jpg"  # 拼接图片url
    return image_url


# 传入url连接，获取 发布的时间
def get_blog_time(url):
    html = requests.get(url, headers=headers).text
    selector = parsel.Selector(html)

    time_stamp = selector.css('div > span.time::text').get()
    pattern = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
    match = pattern.search(time_stamp)
    if match:
        datetime_str = match.group()
        # print(datetime_str)
        return datetime_str
        # print(datetime_str)
    else:
        print('未找到时间')
    """
    print(url)
    # 发送get请求获取响应
    reply = requests.get(url=url, headers=headers)

    # 使用BeautifulSoup解析响应
    parse = BeautifulSoup(reply.content, "lxml")
    print(parse)

    # 查找包含“special-column-name”类名的所有<div>标签
    spans = parse.find_all('span', attrs={'class': 'time'})
    spans_up = parse.find_all('div', attrs={'class': 'up-time'})

    print(spans_up, spans)
    for div in spans:
        # 获取<div>标签中的文本内容
        publish_time = div.text.strip()
        pattern = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
        match = pattern.search(publish_time)
        if match:
            datetime_str = match.group()
            print(datetime_str)
            return datetime_str
            # print(datetime_str)
        else:
            print('未找到时间')
    """


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
    blogs = [130058875, 130099639]  # , 130099639  130058875

    # 遍历博客列表中所有文章
    for blog_dict in blogs:
        blog_url = "https://blog.csdn.net/heian_99/article/details/" + str(blog_dict)
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
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++
        title = reply_data['data']['title']
        description = reply_data['data']['description']
        tags = reply_data['data']['tags'].split(',')
        categories = reply_data['data']['categories'].split(',')
        markdowncontent = reply_data['data']['markdowncontent'].replace("@[toc]", "")

        # 文本创建的时间
        create_file_time = str_to_datetime(get_blog_time(blog_url))

        # 构建markdown文本的首部
        # 加载markdown文件
        fm = frontmatter.loads(markdowncontent)
        # 获取首部信息
        fm['title'] = title
        fm['author'] = "南宫乘风"
        fm['description'] = description
        fm['tags'] = tags
        fm['categories'] = categories
        fm['image'] = random_get_url()
        fm['date'] = create_file_time

        # 保存修改后的markdown文件
        metadata_str_new = frontmatter.dumps(fm)

        #
        pattern = r'!\[[^\]]*\]\(([^)]+)\)'
        # 使用 re.findall() 函数查找所有匹配的图片地址，并将其保存到列表中
        image_urls = re.findall(pattern, metadata_str_new)
        # 打印所有匹配的图片地址
        print(image_urls)
        for url in image_urls:
            qiu_url = get_url(url)
            # print(url, qiu_url)
            metadata_str_new = metadata_str_new.replace(url, qiu_url)
        filename = title + ".md"
        content_new = metadata_str_new
        try:
            # 提取文章正文
            with open(filename, mode="w", encoding="utf-8") as f:
                f.write(content_new)
            print("download blog markdown blog:" + '【' + filename + '】')
            # print(metadata_str_new)
            # 构造文章标题存储路径，如'./1/Nginx/Nginx模板自动化.md'
            # blog_title_dir = './' + str(id) + '/' + str(blog_column) + '/' + str(blog_title) + '.md'
            # # 将文章正文保存为.md文件
            # with open(blog_title_dir, "w", encoding="utf-8") as f:
            #     f.write(content)
            # # 打印日志
            # print("download blog markdown blog:" + '【' + blog_column + '】' + str(blog_title))


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
    request_md('heian_99')
