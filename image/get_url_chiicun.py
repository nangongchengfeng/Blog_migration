# -*- coding: utf-8 -*-
# @Time    : 2023/1/9 22:09
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : get_url_chiicun.py
# @Software: PyCharm
from urllib.request import urlopen
from PIL import Image


def check_image_size(url, width=1920, height=1080):
    # Open the image and read its size
    with urlopen(url) as f:
        image = Image.open(f)
        image_width, image_height = image.size
        print(image_width, image_height)

    # Check if the size matches the required size
    return all((image_width == width, image_height == height))
# Check if an image at a given URL has size 1920x1080
if check_image_size('https://pic.netbian.com/uploads/allimg/221019/001522-166610972208a0.jpg'):
    print('Image has the required size')
else:
    print('Image does not have the required size')
