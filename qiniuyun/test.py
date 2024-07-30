# -*- coding: utf-8 -*-
# @Time    : 2023/3/29 14:55
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : test.py
# @Software: PyCharm
import os
import random
import re
from datetime import datetime

import frontmatter
import requests


def get_url(url):
    """
    从给定的URL下载图片，并保存到指定目录下
    :param url:
    :return:
    """
    response = requests.get(url)

    if response.status_code == 200:
        content = response.content

        # 检查目录是否存在，不存在则创建
        if not os.path.exists('image'):
            os.makedirs('image')

        # 从 URL 中提取文件名的逻辑
        if 'imgconvert.csdnimg.cn/' in url:
            filename = url.split('/')[-1]
        elif len(url) > 55:
            filename_pattern = r'/([\w-]+\.(?:jpg|png|gif|jpeg))'
            matches = re.findall(filename_pattern, url)
            if matches:
                filename = matches[-1]
            else:
                # 如果正则表达式无法匹配，则尝试使用 URL 的最后一部分
                filename = url.split('/')[-1]
                # 如果仍然没有文件扩展名，则附加一个默认扩展名
                if not re.search(r'\.(?:jpg|png|gif|jpeg)$', filename):
                    filename += '.jpg'
        else:
            filename = url.split('/')[-1]
            if not re.search(r'\.(?:jpg|png|gif|jpeg)$', filename):
                filename += '.jpg'

        filepath = f'image/{filename}'
        with open(filepath, 'wb') as f:
            f.write(content)
        url = f"../../image/{filename}"
        return url
    else:
        print(f"Failed to download the image. Status code: {response.status_code}")
        return None

def random_get_url():
    # 生成数字列表，替换原始的图片编号列表，使用zfill()函数将数字转换成两位数，例如1变成'01'，方便拼接url
    nums = [str(i + 1).zfill(2) for i in range(77)]
    x = random.choice(nums)  # 随机选择一个数字作为图片编号
    image_url = f"../../title_pic/{x}.jpg"  # 拼接图片url
    return image_url


def ensure_dir_exists(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
        print(f'Created directory: {dirpath}')


def remove_spaces(s):
    return s.replace(' ', '')


def remove_brackets(s):
    return s.replace('[', '').replace(']', '').replace(':', '-')


def get_filename_url(filename):
    pattern = r'!\[[^\]]*\]\(([^)]+)\)'
    with open('old/' + filename, 'r', encoding='utf-8') as f:
        content = f.read()
        # print(content)
    summary = content.split('<!--more-->')[-1]
    summary_pattern = re.compile('[\u4e00-\u9fa5，；：！？。、]+')
    chinese_text = ''.join(summary_pattern.findall(summary))
    extracted_text = chinese_text[:100] + '。。。。。。。'

    # 使用 re.findall() 函数查找所有匹配的图片地址，并将其保存到列表中
    image_urls = re.findall(pattern, content)

    # 提取 YAML 前置元数据
    metadata_start = content.find('---')
    metadata_end = content.find('---', metadata_start + 3)
    metadata_str = content[metadata_start:metadata_end + 3]
    # 解析 YAML 前置元数据
    print(metadata_str)
    # print(metadata_str.replace('#', ''))
    metadata = frontmatter.loads(metadata_str.replace('#', ''))
    title = remove_brackets(metadata['title'])
    print(metadata['tags'])

    if metadata['tags'] is not None:
        tags_list = [tag.strip() for tag in metadata['tags'].replace('#', '').split(' ')]
    else:
        tags_list = ['技术记录']

    if metadata['categories'] is not None:
        categories_list = [tag.strip() for tag in metadata['categories'].replace('#', '').split(' ')]
    else:
        categories_list = ['技术记录']

    ####
    metadata['author'] = "南宫乘风"
    metadata['title'] = title
    metadata['categories'] = categories_list
    metadata['tags'] = tags_list
    metadata['image'] = random_get_url()
    metadata['description'] =  metadata['description']     #extracted_text
    slug = datetime.strptime(str(metadata['date']), '%Y-%m-%d %H:%M:%S')
    slug = slug.strftime('%Y%m%d%H%M')
    metadata['slug'] = slug
    metadata_str_new = frontmatter.dumps(metadata)
    # print(metadata['title'])  # 输出：SpringBoot集成Apollo和自动注册Consul
    # print(metadata['date'])  # 输出：2023-03-27 10:18:30
    # print(tags_list)  # 输出：2023-03-27 10:18:30
    # print(categories_list)  # 输出：2023-03-27 10:18:30

    dt = datetime.strptime(str(metadata['date']), '%Y-%m-%d %H:%M:%S')
    year = dt.year
    # 打印所有匹配的图片地址
    for url in image_urls:
        print(url)
        qiu_url = get_url(url) or ''
        print(qiu_url)
        content = content.replace(url, qiu_url)
    new_dir = f'csdn/{year}/'
    ensure_dir_exists(new_dir)
    filename = remove_spaces(filename)
    # 将修改后的 Markdown 文件写回磁盘
    content_new = content[:metadata_start] + metadata_str_new + content[metadata_end + 3:]
    with open(new_dir + filename, mode="w", encoding="utf-8") as f:
        f.write(content_new)


def list_filenames(dir_path):
    file_list = []
    for filename in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, filename)):
            # print(filename)
            file_list.append(filename)
    return file_list


if __name__ == "__main__":
    # url='https://img-blog.csdnimg.cn/f0d382ca74a74af2b711e7e8e8a4a5cb.png?x-oss-process=image/watermark,type_ZHJvaWRzYW5zZmFsbGJhY2s,shadow_50,text_Q1NETiBA5Y2X5a6r5LmY6aOO,size_20,color_FFFFFF,t_70,g_se,x_16'
    # get_url(url)
    # get_filename_url("“实时数据同步：构建高效的 MySQL 数据同步方案“.md")
    file_list = list_filenames('old/')
    print(file_list)
    for file in file_list:
        print(file)
        get_filename_url(file)
