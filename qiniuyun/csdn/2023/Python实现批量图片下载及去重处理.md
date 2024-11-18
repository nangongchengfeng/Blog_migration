---
author: 南宫乘风
categories:
- Python学习
date: 2023-04-13 19:45:42
description: 背景在爬虫应用开发中，常常需要批量下载图片，并对图片进行去重处理。是一种非常流行的编程语言，也是开发爬虫应用的首选，本文将介绍如何使用下载图片，并对下载的图片进行去重处理。内容首先，我们需要使用中的库。。。。。。。
image: ../../title_pic/35.jpg
slug: '202304131945'
tags:
- python
- 开发语言
title: Python实现批量图片下载及去重处理
---

<!--more-->

## 背景
在爬虫应用开发中，常常需要批量下载图片，并对图片进行去重处理。Python 是一种非常流行的编程语言，也是开发爬虫应用的首选，本文将介绍如何使用 Python 下载图片，并对下载的图片进行去重处理。
## 内容
首先，我们需要使用 Python 中的 Requests 库来下载图片，并使用 OS 库来创建保存图片的文件夹。下载图片后，我们可以使用 hashlib 库对图片的内容做哈希处理，并将处理后的哈希值作为图片的唯一识别标志，以便进行去重处理。在对图片进行去重处理时，我们需要将下载的图片与已有的图片进行比对，可以使用字典或集合等数据结构来存储已有图片的哈希值，以便查找和比对。在所有的图片下载完成后，我们可以将下载的图片的文件名或哈希值保存到本地文本文件中，以备后续查看或处理。
![在这里插入图片描述](../../image/dd6c81b5812642cd84856422c41f2977.png)
![在这里插入图片描述](../../image/50a782ab7909443ca928571c21d47e5f.png)


一些好看的动漫api接口：[https://blog.csdn.net/likepoems/article/details/123924270](https://blog.csdn.net/likepoems/article/details/123924270)

[https://img.r10086.com/](https://img.r10086.com/)
## 代码

### 1、爬取图片代码
```python
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
        response = requests.get('https://api.r10086.com/img-api.php?type=原神横屏系列1', headers=headers)
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
```

### 2、图片去重

原理：MD5 是一种常用的哈希算法，它可以将任意长度的输入（比如一个字符串或者一个文件）转换成一个 128 比特长度的输出，输出值通常表示为一个 32 位的十六进制数字串。而对于任意输入的变化，其产生的输出也会有所不同，因此可以将 MD5 值作为唯一的识别标志来去重。在 Python 中，我们可以使用 hashlib 库中的 md5 函数来生成 MD5 值。

流程：其具体实现流程如下：
1. 导入 hashlib 库。
2. 定义与图片相关的 path、filename 和 filesize 等变量，使用 os.path 库中的函数处理路径和文件名。
3. 对图片的二进制数据使用 hashlib.md5() 生成 MD5 值。
4. 将生成的 MD5 值转换为字符串格式，去除无用字符。
5. 使用集合或字典等数据结构存储已有图片的 MD5 值，在遍历待下载的图片时，判断其对应的 MD5 值是否已经存在于集合或字典中，若存在则说明图片已下载过，不再重复下载；否则可以将该图片下载下来，并将其对应的 MD5 值加入到已有图片集合中。
6. 下载图片后，将其文件名或 MD5 值存储到本地文本文件中，便于后续查看或处理。
上述流程基本描述了使用 MD5 值去重的具体实现过程，其中还需结合具体应用场景进行优化和改进。
```python
import os
import shutil
import hashlib


def get_md5(file):
    """计算文件的MD5值"""
    if not os.path.isfile(file):
        return None
    with open(file, 'rb') as f:
        md5 = hashlib.md5()
        md5.update(f.read())
        return md5.hexdigest()


def find_duplicate_images(dir_path):
    """查找重复图片"""
    all_images = []
    md5_list = []
    delete_list = []
    # 遍历整个目录，将所有图片的路径保存到一个列表中
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.png'):
                all_images.append(os.path.join(root, file))
    # 对于每个图片，计算它的MD5值，并将MD5值和路径保存到两个列表中
    for image in all_images:
        md5 = get_md5(image)
        if md5 is not None:
            md5_list.append(md5)
        else:
            delete_list.append(image)
    # 判断MD5值列表中是否有重复的值，如果有，则说明该图片是重复图片，将其路径保存到一个删除列表中
    for i in range(len(md5_list)):
        for j in range(i + 1, len(md5_list)):
            if md5_list[i] == md5_list[j]:
                delete_list.append(all_images[j])
    # 遍历删除列表，将其中的图片移动到目标目录中
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    for image in delete_list:
        try:
            shutil.move(image, os.path.join(target_dir, os.path.basename(image)))
            print('已移动重复文件：', image)
        except Exception as e:
            print('移动失败：%s，错误：%s' % (image, str(e)))
    print('重复图片搜索完成，共找到%d个重复文件！' % len(delete_list))


# 示例
if __name__ == '__main__':
    # 需要移动重复图片的目标目录
    # target_dir设置全局变量
    global target_dir
    target_dir = 'repeat_image'
    dir_path = 'dongman'
    find_duplicate_images(dir_path)

```
