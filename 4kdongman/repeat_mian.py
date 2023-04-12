# -*- coding: utf-8 -*-
# @Time    : 2023/4/11 10:44
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : repeat_mian.py
# @Software: PyCharm
import os

from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep

from PIL import Image
import threading
import shutil

# 图片目录路径
image_dir = 'dongman/'
repeat_dir = 'repeat_image/'
# 遍历目录下的所有图片文件名
file_names = []
for file in os.listdir(image_dir):
    if file.startswith('image_') and (file.endswith('.jpg') or file.endswith('.png')):
        file_names.append(file)


# 比较两张图片是否相同
def compare_images(name1, name2):
    try:
        # 加载第一张图片
        img1 = Image.open(os.path.join(image_dir, name1))
        img1 = img1.convert('RGB')
        # 加载第二张图片
        img2 = Image.open(os.path.join(image_dir, name2))
        img2 = img2.convert('RGB')
        # 比较两张图片是否相同
        if img1 == img2:
            # 删除编号更大的那张图片
            if int(name1.split('_')[1].split('.')[0]) > int(name2.split('_')[1].split('.')[0]):
                # os.remove(os.path.join(image_dir, name1))
                # file_names.remove(name1)
                # print(f"删除： {name1}")
                sleep(1)
                shutil.move(os.path.join(image_dir, name1), os.path.join(repeat_dir, name1))
                print(f"移动： {name1} 到 repeat_image 目录下")

            else:
                # os.remove(os.path.join(image_dir, name2))
                # print(f"删除： {name2}")
                sleep(1)
                shutil.move(os.path.join(image_dir, name2), os.path.join(repeat_dir, name2))
                print(f"移动： {name2} 到 repeat_image 目录下")

    except FileNotFoundError:
        pass


# 实例化线程池
pool = ThreadPoolExecutor(max_workers=5)

# 多线程比较图片并删除重复的图片
futures = []
print(file_names)
for i, name1 in enumerate(file_names):
    print(f"开始检测： {name1}")
    for name2 in file_names[i + 1:]:
        # print(f"开始检测： {name1}  {name2}")
        future = pool.submit(compare_images, name1, name2)  # 将任务提交到线程池
        futures.append(future)
    sleep(5)

# 等待所有任务执行完毕
for future in as_completed(futures):
    pass
