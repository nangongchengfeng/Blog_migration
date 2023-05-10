# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import random

#
import requests

list_image = []
for i in range(1, 100):
    images = str(i).rjust(2, '0')
    list_image.append(images)

print(list_image)
x = random.choice(list_image)
print(x)
url = f"http://image.ownit.top/blog/background/{x}.jpg"
print(url)


# 把上面的代码放到一个函数里面,添加中文注释
def random_get_url():
    """
    随机获取一个图片的url
    :return:
    """
    # 生成数字列表，替换原始的图片编号列表，使用zfill()函数将数字转换成两位数，例如1变成'01'，方便拼接url
    nums = [str(i + 1).zfill(2) for i in range(102)]
    x = random.choice(nums)  # 随机选择一个数字作为图片编号
    image_url = f"http://image.ownit.top/4kdongman/{x}.jpg"  # 拼接图片url
    return image_url


# 调用random_get_url()函数，返回一个图片url，进行下载保存
image_url = random_get_url()
print(image_url)
response = requests.get(image_url)
with open('image.jpg', 'wb') as f:
    f.write(response.content)


print(random_get_url())
