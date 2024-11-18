# -*- coding: utf-8 -*-
# @Time    : 2023/3/30 14:06
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : Image_de_duplication.py
# @Software: PyCharm
import os
import shutil

from PIL import Image

# 图片目录路径
image_dir = 'dongman/'
repeat_dir = 'repeat_image/'
# 遍历目录下的所有图片文件名
file_names = []
for file in os.listdir(image_dir):
    if file.startswith('image_') and (file.endswith('.jpg') or file.endswith('.png')):
        file_names.append(file)

# 比较图片并删除重复的图片
for i, name1 in enumerate(file_names):
    # 加载第一张图片
    print(f"开始检测： {name1}")
    try:
        img1 = Image.open(os.path.join(image_dir, name1))
        img1 = img1.convert('RGB')
        for j, name2 in enumerate(file_names[i + 1:]):
            # print(name2)
            try:
                # 加载第二张图片
                img2 = Image.open(os.path.join(image_dir, name2))
                img2 = img2.convert('RGB')
                # 比较两张图片是否相同
                if img1 == img2:
                    # 删除编号更大的那张图片
                    if int(name1.split('_')[1].split('.')[0]) > int(name2.split('_')[1].split('.')[0]):
                        # os.remove(os.path.join(image_dir, name1))
                        # del file_names[i]
                        # # print(f"删除： {file_names[i]}")
                        # print(f"删除： {name1}")

                        shutil.move(os.path.join(image_dir, name1), os.path.join(repeat_dir, name1))
                        print(f"移动： {name1} 到 repeat_image 目录下")
                    else:
                        # os.remove(os.path.join(image_dir, name2))
                        # print(f"删除： {name2}")
                        shutil.move(os.path.join(image_dir, name2), os.path.join(repeat_dir, name2))
                        print(f"移动： {name2} 到 repeat_image 目录下")
            except FileNotFoundError:
                pass
                # print(f'文件未找到：{name2}')
    except FileNotFoundError:
        pass
        # print(f'文件未找到：{name1}')
