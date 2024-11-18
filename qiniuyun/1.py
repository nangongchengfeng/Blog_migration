# -*- coding: utf-8 -*-
# @Time    : 2024-07-18 21:00
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : 1.py
# @Software: PyCharm
import requests
import re
import os


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


# 示例图片链接
image_url = "https://img-blog.csdn.net/20180803092244598?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM1NDI4MjAx/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70"

# 调用函数
result_url = get_url(image_url)
if result_url:
    print(f"Image saved at: {result_url}")
else:
    print("Failed to save the image.")
