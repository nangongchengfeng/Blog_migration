# -*- coding: utf-8 -*-
# @Time    : 2023/3/28 23:07
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : updata_file.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
# @Time    : 2023/3/28 10:43
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : update_file.py
# @Software: PyCharm
from qiniu import Auth, put_file
from apollo_config import secretKey, accessKey

# 获取Access Key 和 Secret Key 后，进行初始化对接：
q = Auth(access_key=accessKey,
         secret_key=secretKey)
# 上传的七牛云空间
bucket_name = 'heian99'


def upload_to_qiniu(file):
    # 上传后保存的文件名
    key = f'csdn/{file}'

    # 生成上传token
    token = q.upload_token(bucket_name, key)

    # 要上传文件的路径
    localfile = f'image/{file}'
    ret, info = put_file(token, key, localfile)
    # 拼接路径   qj5s0uqce.hb-bkt.clouddn.com这个是创建空间分配的测试域名
    image_file = 'http://image.ownit.top/' + ret.get('key')
    print(image_file)  # http://qj5s0uqce.hb-bkt.clouddn.com/1.jpg
    return image_file


if __name__ == '__main__':
    upload_to_qiniu("10.jpg")
