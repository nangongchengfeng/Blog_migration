# -*- coding: utf-8 -*-
# @Time    : 2023/1/9 18:52
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : Crawl_pictures.py
# @Software: PyCharm
import os

import requests

# 返回 页面的HTML 格式
from bs4 import BeautifulSoup

headers = {
    'Users-Agent': 'Mozilla/6.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}


def get_url_info(page):
    url = f'https://pic.netbian.com/e/search/result/index.php?page={page}&searchid=1164'
    res = requests.get(url, headers=headers).text
    return res


# 获取第一层 图片地址
def get_url_list(res):
    soup = BeautifulSoup(res, "html.parser")
    res.encode('UTF-8').decode('UTF-8')
    div_class = soup.find(name='ul', attrs={"class": "clearfix"})
    a_name = div_class.find_all(name='a')
    image_url = []
    for i in a_name:
        image_url.append('http://pic.netbian.com' + i['href'])
    return image_url


# 爬取 图片真实地址
def get_image_url(image_url):
    all_images_url = []
    for new_url in image_url:
        res = requests.get(new_url, headers=headers).text
        soup = BeautifulSoup(res, "html.parser")
        res.encode('UTF-8').decode('UTF-8')
        div_class = soup.find(name='div', attrs={"class": "photo-pic"})
        a_name = div_class.find_all(name='img')

        for i in a_name:
            # print()
            all_images_url.append("https://pic.netbian.com/" + i['src'])
    return all_images_url


def create_directory():
    # 创建文件夹
    isExists = os.path.exists('./4kdongman')
    if not isExists:
        os.makedirs('./4kdongman')


def start_main(numbers):
    all_list_urls = []
    for i in range(1, numbers):
        print(i)
        res = get_url_info(i)
        image_url = get_url_list(res)
        all_url = get_image_url(image_url)
        all_list_urls = all_list_urls + all_url
    # return all_list_urls
    print(len(all_list_urls),all_list_urls)


def url_download(all_list_urls):
    create_directory()
    count = 1
    for i in all_list_urls:
        img_data = requests.get(url=i, headers=headers).content
        filePath = './4kdongman/' + str(count) + '.jpg'
        with open(filePath, 'wb') as fp:
            fp.write(img_data)
        print('%s,下载成功' % count)
        count = count + 1


if __name__ == '__main__':
    start_main(2)
