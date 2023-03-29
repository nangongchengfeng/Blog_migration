# -*- coding: utf-8 -*-
# @Time    : 2023/3/29 15:51
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : update_4k动漫.py
# @Software: PyCharm
from qiniu import Auth, put_file

# 获取Access Key 和 Secret Key 后，进行初始化对接：
q = Auth(access_key='jWaf41PJ7JKXdKmnB6TM3CSuorg4XT_Gas6CDGAm',
         secret_key='ScBEdgrmLBrcak2oPuVnHoqwvW4tIJpV2LvucP8y')
# 上传的七牛云空间
bucket_name = 'heian99'


def upload_to_qiniu(file):
    # 上传后保存的文件名
    key = f'4kdongman/{file}'

    # 生成上传token
    token = q.upload_token(bucket_name, key)

    # 要上传文件的路径
    localfile = f'4kdongman/{file}'
    ret, info = put_file(token, key, localfile)
    # 拼接路径   qj5s0uqce.hb-bkt.clouddn.com这个是创建空间分配的测试域名
    image_file = 'http://image.ownit.top/' + ret.get('key')
    print(image_file)  # http://qj5s0uqce.hb-bkt.clouddn.com/1.jpg
    return image_file


if __name__ == '__main__':
    # upload_to_qiniu("10.jpg")
    for i in range(1, 103):
        num = f"{i:02d}" + ".jpg"
        upload_to_qiniu(num)
        print(num)
