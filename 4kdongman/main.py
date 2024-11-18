# -*- coding: utf-8 -*-
# @Time    : 2023/3/30 13:56
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : main.py
# @Software: PyCharm
import os
import requests
from time import sleep


# https://img.r10086.com/
# https://blog.csdn.net/likepoems/article/details/123924270

def download_images(dir_path, file_prefix, num_images):
    """
    循环访问接口并保存图片到指定目录
    dir_path：图片保存的目录
    file_prefix：保存的文件名前缀
    num_images：需要下载的图片数量
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.36 '
    }
    for i in range(num_images):
        response = requests.get('https://cdn.seovx.com/d/?mom=302', headers=headers)
        if response.status_code == 200:
            # 构造文件名
            file_name = os.path.join(dir_path, f'{file_prefix}_{i}.jpg')
            # 保存图片到本地文件
            with open(file_name, 'wb') as f:
                f.write(response.content)
                print(file_name + " 下载完成")
        else:
            print(f'获取图片失败，状态码：{response.status_code}')

        sleep(1)


# 示例
if __name__ == '__main__':
    dir_path = 'dongman'
    file_prefix = 'image'
    num_images = 1000
    download_images(dir_path, file_prefix, num_images)
