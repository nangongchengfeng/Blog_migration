# -*- coding: utf-8 -*-
# @Time    : 2023/3/28 23:07
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : updata_file.py
# @Software: PyCharm

import os
import random
import string

import requests
from qiniu import Auth, put_file
from apollo_config import secretKey, accessKey

# 获取Access Key 和 Secret Key 后，进行初始化对接：
q = Auth(access_key=accessKey,
         secret_key=secretKey)
# 上传的七牛云空间
bucket_name = 'heian99'


def generate_random_string(length):
    # 生成指定长度的随机字符串，包含数字和小写字母
    letters_and_digits = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))


def generate_random_filename(extension='.png'):
    # 生成以指定扩展名结尾的随机文件名
    return generate_random_string(32) + extension


def upload_to_qiniu(file):
    # 上传后保存的文件名
    key = f'csdn/{file}'

    # 生成上传token
    token = q.upload_token(bucket_name, key)

    # 要上传文件的路径
    localfile = f'images/{file}'
    ret, info = put_file(token, key, localfile)
    # 拼接路径   qj5s0uqce.hb-bkt.clouddn.com这个是创建空间分配的测试域名
    image_file = 'http://image.ownit.top/' + ret.get('key')
    # print(image_file)  # http://qj5s0uqce.hb-bkt.clouddn.com/1.jpg
    return image_file


def download_image(url, save_dir='./images/'):
    # 从给定的URL下载图片，并保存到指定目录下
    response = requests.get(url)
    if response.status_code == 200:
        filename = generate_random_filename('.png')
        filepath = os.path.join(save_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        upload_to_qiniu(filename)
        print(f'Saved image {filename} to {save_dir}.')
    else:
        print(f'Failed to download image from {url}, status code: {response.status_code}.')


# 使用示例


if __name__ == '__main__':
    url = 'https://img-blog.csdnimg.cn/20200429162352895.bmp?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2hlaWFuXzk5,size_16,color_FFFFFF,t_70'
    download_image(url)
    # upload_to_qiniu("10.jpg")
