# -*- coding: utf-8 -*-
# @Time    : 2023/3/28 23:10
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : read_md.py
# @Software: PyCharm
import os
import random
import re
from datetime import datetime

import requests
import frontmatter

from updata_file import upload_to_qiniu


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
        filepath = f'image/{filename}'
        print(filename)
        with open(filepath, 'wb') as f:
            f.write(content)
        url = upload_to_qiniu(filename)
        # print(url)
        return url


def random_get_url():
    list_image = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16',
                  '17',
                  '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33',
                  '34',
                  '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50',
                  '51',
                  '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67',
                  '68',
                  '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84',
                  '85',
                  '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '100', '101',
                  '102']
    x = random.choice(list_image)
    image_url = f"http://image.ownit.top/4kdongman/{x}.jpg"
    # print(image_url)
    return image_url


def ensure_dir_exists(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
        print(f'Created directory: {dirpath}')


def remove_spaces(s):
    return s.replace(' ', '')


def remove_brackets(s):
    return s.replace('[', '').replace(']', '')


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
    metadata['description'] = extracted_text
    metadata_str_new = frontmatter.dumps(metadata)
    # print(metadata['title'])  # 输出：SpringBoot集成Apollo和自动注册Consul
    # print(metadata['date'])  # 输出：2023-03-27 10:18:30
    # print(tags_list)  # 输出：2023-03-27 10:18:30
    # print(categories_list)  # 输出：2023-03-27 10:18:30
    print(metadata_str_new)
    dt = datetime.strptime(str(metadata['date']), '%Y-%m-%d %H:%M:%S')
    year = dt.year
    # 打印所有匹配的图片地址
    for url in image_urls:
        print(url)
        qiu_url = get_url(url) or ''
        print(qiu_url)
        content = content.replace(url, qiu_url)
    new_dir = f'new/{year}/'
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
    # get_filename_url("在Kubernetes（k8s）中部署Java应用.md")
    file_list = list_filenames('old/')
    print(file_list)
    for file in file_list:
        print(file)
        get_filename_url(file)
