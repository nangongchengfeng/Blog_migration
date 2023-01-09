+++
author = "南宫乘风"
title = "Python购物车和学生管理系统"
date = "2020-04-14 15:53:27"
tags=['python', '习题']
categories=['Python学习']
image = "post/4kdongman/99.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/105513825](https://blog.csdn.net/heian_99/article/details/105513825)

### 购物车练习程序

**（1）可以显示商品列表**

**（2）根据商品id进行购买**

**（3）根据输入的工作来判断是否有足够的钱购买**

**（4）退出时，显示购买的商品和卡中的余额**

```
# 购物车练习程序

product_list = [
    ('iphone', 5000),
    ('Mac', 9000),
    ('Bike', 800),
    ('watch', 600),
    ('book', 600),
]
shopping_list = []
def shop():
    salay = input("请输入你的工资:")
    if salay.isdigit():
        salay = int(salay)
        while True:
            for index, itme in enumerate(product_list):
                #print(product_list.index(itme),itme)
                print(index,itme)

            user_choice = input("选择要买的商品？请选择购买的编号！")

            if user_choice.isdigit():
                user_choice = int(user_choice)
                if user_choice &lt; len(product_list) and user_choice &gt;-1:
                    p_itme = product_list[user_choice]
                    if p_itme[1] &lt;= salay:#买的起
                        shopping_list.append(p_itme)
                        salay-=p_itme[1]
                        print("Added %s into shopping cart ,you current balance is \033[31;1m%s\033[0m" %(p_itme,salay))
                    else:
                        print("\033[41;1m你的余额不足，只剩[%s]\033[0m" % salay)
                else:
                    print("请输入正确商品编号")

            elif user_choice == 'q':

                print('----------------------shopping list----------------------------')
                for p in shopping_list:
                    print(p)
                print("\033[41;1m你的余额[%s]\033[0m" % salay)
                exit()
            else:
                print("请输入正确的编号")
    else:
        print("你输入的工资格式不对，请输入正确的格式")
        shop()
shop()

```

### 学生管理系统

```
"""
欢迎使用[学生管理系统] V1.0
1.显示所有学生信息
2.新建学生信息
3.查询学生信息
4.修改学生信息
5.删除学生信息
0.退出系统
"""
# 模拟学生数据
from datetime import datetime

student_data = [
    {
        'name': '南宫乘风',
        'sex': '男',
        'address': '西安',
        'birthday': '20000229'
    },
    {
        'name': '乘风',
        'sex': '男',
        'address': '洋县',
        'birthday': '20101229'
    }
]


# 学生类
class Student:
    # 学生初始化
    def __init__(self, name, sex, address, birthday):
        self.name = name
        self.sex = sex
        self.address = address
        self.birthday = birthday

    # 获取学生年龄
    def get_age(self):
        if self.birthday:
            age = datetime.now().year - int(self.birthday[:4])
            return age
        else:
            print("不知道")


# 学生管理系统类


class System:
    # 初始化
    def __init__(self, name):
        self.name = name
        self.data = []

    # 美化输出打印
    def beauty_print(self, data_list):
        for index, student in enumerate(data_list):
            print(f"序号：{index}", end='\t')
            print(f"姓名：{student.name}", end='\t')
            print(f"性别：{student.sex:2}", end='\t')
            print(f"地址：{student.address}", end='\t')
            print(f"年龄：{student.get_age()}")

    # 加载数据
    def load_data(self):
        for item in student_data:
            student = Student(item['name'], item['sex'], item['address'], item['birthday'])
            self.data.append(student)

    # 显示菜单
    def show_menu(self):
        # f-string
        print(f"""
        ******************************
            欢迎使用[{self.name}] V2.0
            1.显示所有学生信息
            2.新建学生信息
            3.查询学生信息
            4.修改学生信息
            5.删除学生信息
            0.退出系统
        ******************************    
        """)

    # 启动学生管理系统
    def start(self):
        # 加载数据
        self.load_data()
        while True:

            self.show_menu()
            op = input("选择操作")
            if op == '1':
                self.show_all_student()
            elif op == '2':
                self.create_student()
            elif op == '3':
                self.find_student()
            elif op == '4':
                self.modify_student()
            elif op == '5':
                self.remove_student()
            elif op == '6':
                print('退出程序')
                break
            else:
                print("请输入正常的操作")

    # 选择性别
    def choose_sex(self):
        sex = input("请选择性别：（1）:男|(2):女").strip()
        if sex == '1':
            return '男'
        elif sex == '2':
            return '女'
        else:
            return '未知'

    # 判断名字
    def input_name(self):
        while True:
            name = input("请输入名字：").strip()
            if name:
                return name
            else:
                continue

    # 根据名字查询
    def find_student_name(self):
        name = self.input_name()
        find_list = []
        for student in self.data:
            if name.lower() in student.name.lower():
                find_list.append(student)
        if find_list:
            return find_list
        else:
            print(f"没有找到学生：{name}")

    # 1.显示所有学生信息
    def show_all_student(self):
        self.beauty_print(self.data)

    # 2.新建学生信息
    def create_student(self):
        name = self.input_name()
        sex = self.choose_sex()
        address = input("请输入地址")
        birthday = input("请输入生日")
        student = Student(name, sex, address, birthday)
        self.data.append(student)

    # 3.查询学生信息
    def find_student(self):
        # name = self.input_name()
        # for student in self.data:
        #     if name.lower() in student.name.lower():
        #         self.beauty_print([student])

        find_list = self.find_student_name()
        self.beauty_print(find_list)

    # 4.修改学生信息
    def modify_student(self):
        find_list = self.find_student_name()
        if find_list:
            self.beauty_print(find_list)
            index = int(input("选择序号:"))
            student = find_list[index]
            print('当前修改的是：')
            self.beauty_print([student])
            student.name = input('输入新的名字：').strip()
            student.sex = self.choose_sex()
            student.address = input("请输入地址：")
            student.birthday = input("请输入生日：")
            print(f'{student.name}已经修改')
            return

    # 5.删除学生信息
    def remove_student(self):
        find_list = self.find_student_name()
        if find_list:
            self.beauty_print(find_list)
            index = int(input("选择序号:"))
            student = find_list[index]
            print('当前删除的是：')
            self.beauty_print([student])
            self.data.remove(student)
            return
        else:
            print(f'没有的人')

    # 0.退出系统


if __name__ == '__main__':
    student_sys = System('乘风系统')
    student_sys.start()

```

 
