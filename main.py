# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import random

list_image=[]
for i in range(1,11):
    images=str(i).rjust(2,'0')
    list_image.append(images)

print(list_image)
x = random.choice(list_image)
print(x)
url=f"http://image.ownit.top/blog/background/{x}.jpg"
print(url)