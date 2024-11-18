---
author: 南宫乘风
categories:
- Python学习
date: 2020-11-30 21:07:54
description: 南宫乘风：我在学哦：你不写项目，是不会有进步的，年轻人，耗子尾汁吧南宫乘风：我要进步，要学习，开始项目：来骗，来偷袭。很快啊！年轻人，不讲码德学了一点时间，为了巩固基础，拿一个简单的项目练手。购物车功。。。。。。。
image: http://image.ownit.top/4kdongman/43.jpg
tags:
- python
title: Python构建简单的ATM+购物功能项目
---

<!--more-->

---

**南宫乘风：我在学Python哦**

**Python：你不写Python项目，是不会有进步的，年轻人，耗子尾汁吧**

**南宫乘风：我要进步，要学习，开始项目**

**Python：来骗，来偷袭。很快啊！年轻人，不讲码德**

---

**学了一点时间Python，为了巩固基础，拿一个简单的项目练手。**

# **ATM+购物车功能（ps：很简单，大佬不要嘲笑哈）**

## **项目需求：**

> ```html
> 1.额度15000或自定义     -->  注册功能
> 2.实现购物商城，买东西加入购物车，调用信用卡接口结账  --> 购物功能、支付功能
> 3.可以提现，手续费5%   --> 提现功能
> 4.支持多账户登录  --> 登录功能
> 5.支持账户间转账  --> 转账功能
> 6.记录日常消费 -->  记录流水功能
> 7.提供还款接口 -->  还款功能
> 8.ATM记录操作日志 --> 记录日志功能
> 9.提供管理接口，包括添加账户、用户额度，冻结账户等。。。 ---> 管理员功能
> 10.用户认证用装饰器  --> 登录认证装饰器
> ```

## "用户视图层" 展示给用户选择的功能

> ```html
> user
> 
> 1、注册功能
> 2、登录功能
> 3、查看余额
> 4、提现功能
> 5、还款功能
> 6、转账功能
> 7、查看流水
> 8、购物功能
> 9、查看购物车
> 10、管理员功能
> ```
> 
> admin
> 
> ```html
> 1、添加账号
> 2、修改额度
> 3、冻结账号
> 4、解冻账号
> 5、返回上一层
> ```

## 架构流程图

**采取MVC的架构方式**

**各层分开，编写接口**

**三层架构：**

> ```html
> 1、把每个功能都分层三部分，逻辑清晰
> 2、如果用户更换不同的用户界面或不同的数据库存储机制，不会影响接口层的核心逻辑代码，扩展性强。
> 3）可以在接口层，准确的记录日志与流水。
> ```

![](http://image.ownit.top/csdn/20201130203919950.png)

![](http://image.ownit.top/csdn/20201130204117864.png)

 

## 三层架构构建  [ 项目代码](https://wwx.lanzoux.com/i1vhGixijzi)：<https://wwx.lanzoux.com/i1vhGixijzi>

![](http://image.ownit.top/csdn/20201130204442412.png)

![](http://image.ownit.top/csdn/2020113020454357.png)

## 启动界面

### ![](http://image.ownit.top/csdn/20201130205843243.png)

![](http://image.ownit.top/csdn/20201130205906346.png)

### start.py（程序的入口）

```python
'''
程序入口
'''
import os
import sys
from core import src

# 添加解释器的环境变量
sys.path.append(
    os.path.dirname(__file__)
)
# 开始执行项目main
if __name__ == "__main__":
    src.run()
```

## conf

### setting.py（log日志的配置文件，项目的环境配置）

```python
'''
配置文件设置

'''
import os
BASE=os.path.dirname(os.path.dirname(__file__))
# print(BASE)
#获取user_date文件夹路径
USER_DATE=os.path.join(BASE,'db','user_date')
# print(USER_DATE)

"""
日志配置字典LOGGING_DIC
"""
# 1、定义三种日志输出格式，日志中可能用到的格式化串如下
# %(name)s Logger的名字
# %(levelno)s 数字形式的日志级别
# %(levelname)s 文本形式的日志级别
# %(pathname)s 调用日志输出函数的模块的完整路径名，可能没有
# %(filename)s 调用日志输出函数的模块的文件名
# %(module)s 调用日志输出函数的模块名
# %(funcName)s 调用日志输出函数的函数名
# %(lineno)d 调用日志输出函数的语句所在的代码行
# %(created)f 当前时间，用UNIX标准的表示时间的浮 点数表示
# %(relativeCreated)d 输出日志信息时的，自Logger创建以 来的毫秒数
# %(asctime)s 字符串形式的当前时间。默认格式是 “2003-07-08 16:49:45,896”。逗号后面的是毫秒
# %(thread)d 线程ID。可能没有
# %(threadName)s 线程名。可能没有
# %(process)d 进程ID。可能没有
# %(message)s用户输出的消息
import os
BASE_PATH=os.path.dirname(os.path.dirname(__file__))
a1_path=os.path.join(BASE_PATH,'log','a1.log')
a2_path=os.path.join(BASE_PATH,'log','a2.log')
# print(a1_path+'\n'+a2_path)

# 2、强调：其中的%(name)s为getlogger时指定的名字
standard_format = '%(asctime)s - %(threadName)s:%(thread)d - 日志名字:%(name)s - %(filename)s:%(lineno)d -' \
                  '%(levelname)s - %(message)s'

simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'

test_format = '%(asctime)s] %(message)s'

# 3、日志配置字典
LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': standard_format
        },
        'simple': {
            'format': simple_format
        },
        'test': {
            'format': test_format
        },
    },

    'filters': {},
    # handlers是日志的接收者，不同的handler会将日志输出到不同的位置
    'handlers': {
        #打印到终端的日志
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'simple'
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            # 'maxBytes': 1024*1024*5,  # 日志大小 5M
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'filename': a1_path,  # os.path.join(os.path.dirname(os.path.dirname(__file__)),'log','a2.log')
            'encoding': 'utf-8',
            'formatter': 'standard',

        },
        #打印到文件的日志,收集info及以上的日志
        'other': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',  # 保存到文件
            'filename': a1_path, # os.path.join(os.path.dirname(os.path.dirname(__file__)),'log','a2.log')
            'encoding': 'utf-8',
            'formatter': 'standard',


        },
    },
    # loggers是日志的产生者，产生的日志会传递给handler然后控制输出
    'loggers': {
        #logging.getLogger(__name__)拿到的logger配置
        'kkk': {
            'handlers': ['console','other'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'DEBUG', # loggers(第一层日志级别关限制)--->handlers(第二层日志级别关卡限制)
            'propagate': False,  # 默认为True，向上（更高level的logger）传递，通常设置为False即可，否则会一份日志向上层层传递
        },
        '终端提示': {
            'handlers': ['console',],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'DEBUG',  # loggers(第一层日志级别关限制)--->handlers(第二层日志级别关卡限制)
            'propagate': False,  # 默认为True，向上（更高level的logger）传递，通常设置为False即可，否则会一份日志向上层层传递
        },
        '': {
            'handlers': ['default', ],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'DEBUG',  # loggers(第一层日志级别关限制)--->handlers(第二层日志级别关卡限制)
            'propagate': False,  # 默认为True，向上（更高level的logger）传递，通常设置为False即可，否则会一份日志向上层层传递
        },
    },
}

```

## core

### admin.py（admin用户视图）

```python
from core import src
from interface import admin_interface


def add_user():
    src.register()


def change_balance():
    while True:
        # 输入修改修改用户名
        change_user = input('请输入需要修改额度的用户：').strip()
        change_money = input('请输入需要修改的用户额度：').strip()
        if not change_money.isdigit():
            continue
        if int(change_money) >= 0:
            flag, msg = admin_interface.change_balance_interafce(change_user, change_money)
            if flag:
                print(msg)
            else:
                print(msg)
        else:
            print('输入的额度不正确')


def disable_user():
    # 输入要冻结的用户
    while True:
        dis_user = input('请输入要冻结的用户：').strip()
        flag, msg = admin_interface.disable_user_interface(dis_user)
        if flag:
            print(msg)
            break
        else:
            print(msg)


def enable_user():
    # 输入要解冻冻结的用户
    while True:
        dis_user = input('请输入要解冻冻结的用户：').strip()
        flag, msg = admin_interface.enable_user_interface(dis_user)
        if flag:
            print(msg)
            break
        else:
            print(msg)


def lsat_men():
    from core import src
    src.run()


func_dic = {
    '1': add_user,
    '2': change_balance,
    '3': disable_user,
    '4': enable_user,
    '5': lsat_men,

}


def admin_run():
    while True:
        print('''
            1、添加账号
            2、修改额度
            3、冻结账号
            4、解冻账号
            5、返回上一层
        ''')
        choice = input('请输入管理员功能编号：').strip()
        if choice not in func_dic:
            print("请输入正确的功能编号")
            continue
        func_dic.get(choice)()

# if __name__ == '__main__':
#     admin()
```

### src.py（用户的视图）

```python
'''
用户视图层
'''

from interface import user_interface, bank_interface, shop_interface
from lib import common
from core import admin

# 1、注册功能
'''def register():
    while True:
        # 1 让用户输入用户名称和密码进行校验
        username = input('请输入用户：').strip()
        if username.strip()=='':
            print("请输入正确的用户名")
            continue

        user_path = os.path.join(setting.USER_DATE, f"{username}.json")
        if os.path.exists(user_path):
            print(f"您输入的用户名：{username}已经存在")
            continue
        password = input("请输入密码：").strip()
        re_password = input("请确认密码：").strip()
        # 判断密码是否一致
        if password == re_password:

            # 2 查看用户是否存在
            # 3 如用户存在，则让用户重新输入
            # 4 如用户不存在，则保存用户数据
            # 4.1 组织用户的数据的字典信息
            user_dic = {
                'username': username,
                'password': password,
                'balance': 15000,
                # 用于记录用户的流水类表

                'flow': [],
                # 用于记录用户购物车
                'shop_car': [],
                # locaked :用于记录用户是否冻结
                # false：未冻结  True：已经被冻结
                'locaked': False
            }
            # 用户数据tank.json
            user_path = os.path.join(setting.USER_DATE, f"{username}.json")
            with open(user_path, 'w', encoding='utf-8') as f:
                json.dump(user_dic, f)
        else:
            print('您的两次密码不一致,请重新输入')'''

login_user = None


# 分层版
def register():
    while True:
        # 1 让用户输入用户名称和密码进行校验
        username = input('请输入用户：').strip()
        if username.strip() == '':
            print("请输入正确的用户名")
            continue
        password = input("请输入密码：").strip()
        re_password = input("请确认密码：").strip()
        # 判断密码是否一致
        if password == re_password:
            # 2 调用接口层的注册结果。将用户名和密码传到接口层
            # (True, 用户注册成功)，  (False, 注册失败)
            flag, msg = user_interface.register_interface(
                username, password
            )

            # 3) 根据flag判断用户注册是否成功，flag控制break的结束
            if flag:
                print(msg)
                break
            else:
                print(msg)
        else:
            print('您的两次密码不一致,请重新输入')


# 2、登录功能
def login():
    # 登录视图层
    while True:
        username = input('请输入用户名：').strip()
        password = input('请输入用户名密码：').strip()

        flag, msg = user_interface.longin_interface(username, password)
        if flag:
            global login_user
            login_user = username
            print(msg)
            break
        else:
            print(msg)


# 3、查看余额
@common.login_auth
def check_balance():
    # 直接调用查看用户接口，获取用余额
    balance = user_interface.check_balance_interface(login_user)
    print(f'用户：{login_user}账号余额为：{balance}')


# 4、提现功能
@common.login_auth
def withdraw():
    while True:
        # 让用户输入体现金额
        input_money = input('请输入提现金额：').strip()
        # 判断用户输入的金额是否是数字
        if not input_money.isdigit():
            print('请重新输入：')
            continue
        # 用户提现，将金额提交接口处理
        flag, msg = bank_interface.withdraw_interface(login_user, int(input_money))
        if flag:
            print(msg)
            break
        else:
            print(msg)


# 5、还款功能
@common.login_auth
def repay():
    while True:
        # 让用户输入体现金额
        repay_money = input('请输入还款金额：').strip()
        # 判断用户输入的金额是否是数字
        if not repay_money.isdigit():
            print('请重新输入')
            continue
        # 用户提现，将金额提交接口处理
        if int(repay_money) > 0:
            flag, msg = bank_interface.repay_interface(login_user, int(repay_money))
            if flag:
                print(msg)
                break
        else:
            print('不能输入小于0的数字')


# 6、转账功能
@common.login_auth
def transfer():
    '''
    接收用户的转账金额
    接收用户输入的转账目标
    :return:
    '''
    while True:
        user_money = input('请输入转账目标用户：').strip()
        money = input('请输入转账金额：').strip()
        if not money.isdigit():
            print('请输入正确的金额！')
            continue
        money = int(money)
        if money > 0:
            # 转账接口
            flag, msg = bank_interface.transfer_interface(login_user, user_money, money)
            if flag:
                print(msg)
                break
            else:
                print(msg)
        else:
            print('请输入正确的金额！')


# 7、查看流水
@common.login_auth
def check_flow():
    # 直接调用查看流水的列表
    flow_list = bank_interface.check_flow_interface(login_user)
    if flow_list:
        for flow in flow_list:
            print(flow)
    else:
        print('当前用户没有流水记录')


# 8、购物功能
@common.login_auth
def shopping():
    '''
    {
        '0':{'name':'包子','price':30},
        '0': {'name': '包子', 'price': 30},
        '0': {'name': '包子', 'price': 30},
    }
    :return:
    '''
    shop_list = [
        ['包子', 30],
        ['衣服', 150],
        ['安全套', 25],
        ['情趣内衣', 520],
        ['cosplay', 250],
    ]
    shopping_car = {}
    while True:
        # 先打印商品的信息，让用户选择
        print('===================欢迎来到情趣商城================')
        for index, shop in enumerate(shop_list):
            shop_name, shop_price = shop
            print(f'商品编号：{index}, 商品名称：{shop_name},商品单价：{shop_price}')
        print('========================end======================')

        shop_choice = input("请输入你要选购的商品编号(是否结账y or n)：").strip()
        if shop_choice.upper() == 'Y':
            if not shopping_car:
                print('购物车是空的，不能支付，请重新输入')
                continue
            # 调用支付接口进行支付
            flag,msg=shop_interface.shopping_interface(login_user,shopping_car)
            if flag:
                print(msg)
                break
            else:
                print(msg)
        elif shop_choice.upper() == 'N':
            # 判断当前用户是否添加过购物车
            if not shopping_car:
                print('购物车是空的，不能添加，请重新输入')
                continue

            flag,msg=shop_interface.add_shop_car_interface(login_user,shopping_car)
            if flag:
                print(msg)
                break

        if not shop_choice.isdigit():
            print('请输入正确的编号！')
            continue
        shop_choice = int(shop_choice)
        if shop_choice not in range(len(shop_list)):
            print('请输入正确的编号！')
            continue
        shop_name, shop_price = shop_list[shop_choice]

        if shop_name in shopping_car:
            shopping_car[shop_name][1] += 1
        else:
            shopping_car[shop_name] = [shop_price, 1]

        print("当前购物车：",shopping_car)

# 9、查看购物车
@common.login_auth
def check_shop_car():
    shop_list = shop_interface.check_shop_car_interface(login_user)
    if shop_list:
        for shop_name,print_number in shop_list.items():
            print(f'商品：[{shop_name}],数量：[{print_number[1]}]')
    else:
        print('当前用户没有流水记录')


@common.login_auth
def admin_spuer():
    admin.admin_run()


# 创建函数功能字典

func_dic = {
    '1': register,
    '2': login,
    '3': check_balance,
    '4': withdraw,
    '5': repay,
    '6': transfer,
    '7': check_flow,
    '8': shopping,
    '9': check_shop_car,
    '10': admin_spuer,
}


def run():
    while True:
        print('''
        ==========ATM+购物车==========
                1、注册功能
                2、登录功能
                3、查看余额
                4、提现功能
                5、还款功能
                6、转账功能
                7、查看流水
                8、购物功能
                9、查看购物车
                10、管理员功能
        ==========  end  ==========
        ''')
        choice = input("请输入功能编号：").strip()
        if choice not in func_dic:
            print("请输入正确的功能编号")
            continue
        func_dic.get(choice)()
```

## db

## user\_date \(用户存放json的目录\)

### q.json （用户数据的存放文件，字典形式）  
 

```python
{"username": "q", "password": "099b3b060154898840f0ebdfb46ec78f", "balance": 14375.0, "flow": ["用户[q] 提现金额 [500],手续费为：[25.0]", "用户：[q]给用户[w] 转账：[100] 元 成功"], "shop_car": {}, "locked": false}
```

json格式

```python
{
	"username": "q",
	"password": "099b3b060154898840f0ebdfb46ec78f",
	"balance": 14375.0,
	"flow": ["用户[q] 提现金额 [500],手续费为：[25.0]", "用户：[q]给用户[w] 转账：[100] 元 成功"],
	"shop_car": {},
	"locked": false
}
```

### db\_hander.py（对数据处理，相当于mysql接口处理）

```python
'''
数据处理层
    专门用户处理数据的
'''
import json
import os
from conf import setting


# 判断用户是否已经注册
def user_select(username):
    # 1) 接收接口层传过来的username用户名，拼接用户json文件路径
    user_path = os.path.join(
        setting.USER_DATE, f'{username}.json'
    )

    # 2）校验用户json文件是否存在
    if os.path.exists(user_path):
        # 3) 打开数据，并返回给接口层
        with open(user_path, 'r', encoding='utf-8') as f:
            user_dic = json.load(f)
            return user_dic

    # 3) 不return，默认return None

# 保存数据处理
def user_save(user_dic):
    user_path = os.path.join(setting.USER_DATE, f"{user_dic['username']}.json")
    with open(user_path, 'w', encoding='utf-8') as f:
        json.dump(user_dic, f, ensure_ascii=False)
```

## interface

### admin\_interface.py（admin的业务接口处理）

```python
from db import db_hander
from lib import common
user_logger=common.get_log('admin')

# 修改额度接口
def change_balance_interafce(change_user, change_money):
    user_dic = db_hander.user_select(change_user)

    if user_dic:
        user_dic['balance'] = int(change_money)
        db_hander.user_save(user_dic)
        msg=f'[{change_user}]的额度修改{change_money}成功'
        user_logger.info(msg)
        return True, msg
    return False, '修改额度用户不存在'


def disable_user_interface(dis_user):
    user_dic = db_hander.user_select(dis_user)
    if user_dic:
        user_dic['locked'] = True
        db_hander.user_save(user_dic)
        msg = f'[{dis_user}]的冻结成功'
        user_logger.info(msg)
        return True, msg
    else:
        return False, '冻结用户不存在'

# 解冻用户的接口
def enable_user_interface(dis_user):
    user_dic = db_hander.user_select(dis_user)
    if user_dic:
        if user_dic['locked']:
            user_dic['locked'] = False
            db_hander.user_save(user_dic)
            msg = f'[{dis_user}]的冻结成功'
            user_logger.info(msg)
            return True, msg
        return False,f'用户：{dis_user}处于正常状态'
    else:
        return False, '冻结用户不存在'
```

### bank\_interface.py（银行业务处理接口）

```python
'''
银行相关的业务
'''
from db import db_hander
from lib import common
user_logger=common.get_log('bank')

# 用户的提现金额接口
def withdraw_interface(login_user, input_money):
    # 先获取用户字典
    user_dic = db_hander.user_select(login_user)
    # 获取银行的金额
    balance = int(user_dic.get('balance'))
    # 本金+ 手续费
    money = int(input_money) * 1.05
    repair = round(money - input_money, 2)
    # 判断用户金额是否足够
    if balance >= money:
        # 修改用户字典的金额
        balance -= money
        user_dic['balance'] = balance
        flow = f'用户[{login_user}] 提现金额 [{input_money}],手续费为：[{repair}]'
        user_dic['flow'].append(flow)
        # 在保存数据
        db_hander.user_save(user_dic)
        msg=f'用户[{login_user}] 提现金额 [{input_money}],手续费为：[{repair}]'
        user_logger.info(msg)
        return True, msg
    return False, '提现金额不足，请重新输入'


# 还款接口
def repay_interface(login_user, repay_money):
    # 先获取用户字典
    user_dic = db_hander.user_select(login_user)
    # 获取银行的金额
    balance = int(user_dic.get('balance'))
    # 本金+ 手续费
    money = int(repay_money)
    # repair = round(money - repay_money, 2)
    # 修改用户字典的金额
    balance += money
    user_dic['balance'] = balance
    # 在保存数据
    flow = f'用户：[{login_user}] 还款金额 ：[{repay_money}]成功]'
    user_dic['flow'].append(flow)
    db_hander.user_save(user_dic)
    msg = f'用户：[{login_user}] 还款金额 ：[{repay_money}]成功]'
    user_logger.info(msg)
    return True, msg


# 转账接口
def transfer_interface(login_user, user_money, money):
    # 先获取用户字典
    login_user_dic = db_hander.user_select(login_user)
    user_money_dic = db_hander.user_select(user_money)
    # 判断目标用户是否存在
    if not user_money_dic:
        return False, '目标用户不存在'
    if login_user == user_money:
        return False, '不能给自己转账'
    if login_user_dic['balance'] >= money:
        login_user_dic['balance'] -= money
        user_money_dic['balance'] += money
        flow1 = f'用户：[{login_user}]给用户[{user_money}] 转账：[{money}] 元 成功'
        login_user_dic['flow'].append(flow1)
        flow2 = f'用户：[{user_money}]接受用户[{login_user}] 转账：[{money}] 元 成功'
        user_money_dic['flow'].append(flow2)
        db_hander.user_save(login_user_dic)
        db_hander.user_save(user_money_dic)
        msg = f'用户：[{login_user}]给用户[{user_money}] 转账：[{money}] 元 成功'
        user_logger.info(msg)
        return True, msg
    msg = f'用户：[{login_user}]银行余额不足'
    user_logger.info(msg)
    return False, msg


# 流水接口列表查询
def check_flow_interface(login_user):
    # 先获取用户字典
    login_user_dic = db_hander.user_select(login_user)
    flow_list = login_user_dic['flow']
    return flow_list


# 支付接口
def pay_interface(login_user, cost):
    user_dic = db_hander.user_select(login_user)
    if user_dic.get('balance') >= cost:
        user_dic['balance'] -= cost

        flow = f'用户：{login_user}消费金额：{cost}'
        user_dic['flow'].append(flow)
        db_hander.user_save(user_dic)
        user_logger.info(flow)
        return True
    return False


```

### shop\_interface.py（购物业务接口处理）

```python
'''
购物商城接口
'''
from interface import bank_interface
from db import db_hander
from lib import common
shop_logger = common.get_log(log_type='shop')

# 商品准备结算接口
def shopping_interface(login_user, shopping_car):
    # 计算商品总价
    cost = 0
    for shop_price in shopping_car.values():
        price, number = shop_price
        cost += (price * number)

    # 逻辑校验成功，调用银行的支付接口
    flag = bank_interface.pay_interface(login_user, cost)
    if flag:
        msg = f'用户:[{login_user}]支付 [{cost}$] 成功, 准备发货!'
        shop_logger.info(msg)
        return True, msg

    return False, '支付失败，金额不足'


# 商品添加购物车功能
def add_shop_car_interface(login_user, shopping_car):
    # 获取当前用户的购物车
    user_dic = db_hander.user_select(login_user)
    #原来用户的字典的商城列表
    shop_car = user_dic.get('shop_car')

    for shop_name, price_number in shopping_car.items():
        number = price_number[1]
        if shop_name in shop_car:
            user_dic['shop_car'][shop_name][1] += number
        else:
            user_dic['shop_car'].update(
                {shop_name: price_number}
            )
        db_hander.user_save(user_dic)
    return True, '添加购物车成功'

# 查看购物车接口
def check_shop_car_interface(login_user):
    # 获取当前用户的购物车
    user_dic = db_hander.user_select(login_user)
    shop_list = user_dic['shop_car']
    return shop_list
```

### user\_interface.py（用户业务接口处理）

```python
'''
用户相关的接口

'''
import os
import json

from db import db_hander
from lib import common
user_logger=common.get_log('user')

# 用户注册
def register_interface(username, password, balance=15000):
    # 2）查看用户是否存在
    # 2.1) 调用 数据处理层 中的 select函数，会返回 用户字典 或 None
    user_dic = db_hander.user_select(username)

    # {user: user, pwd: pwd...}   or  None
    # 若用户存在，则return，告诉用户重新输入
    if user_dic:
        # return (False, '用户名已存在!')
        return False, '用户名已存在!'

    # 3）若用户不存在，则保存用户数据
    # 做密码加密
    password = common.salt(username, password)

    # 3.1) 组织用户的数据的字典信息
    user_dic = {
        'username': username,
        'password': password,
        'balance': balance,
        # 用于记录用户流水的列表
        'flow': [],
        # 用于记录用户购物车
        'shop_car': {},
        # locked：用于记录用户是否被冻结
        # False: 未冻结   True: 已被冻结
        'locked': False
    }

    # 3.2）保存数据
    db_hander.user_save(user_dic)
    msg=f'{username} 注册成功!'
    user_logger.info(msg)
    return True, msg


# 登录接口
def longin_interface(username, password):
    # 先查看用户是否存在
    user_dic = db_hander.user_select(username)
    password_md5 = common.salt(username, password)

    if user_dic:
        print(user_dic.get('locked'))
        if user_dic.get('locked'):
            return False, f'用户：[{username}]已经被冻结'
        if password_md5 == user_dic['password']:
            msg=f'用户：[{username}] 登录成功  '
            user_logger.info(msg)
            return True,msg

        else:
            msg = f'用户：[{username}]密码错误'
            user_logger.warning(msg)
            return False, msg
    msg = f'用户[{username}]不存在，请重新输入'
    user_logger.info(msg)
    return False, msg


# 查看用户余额接口
def check_balance_interface(login_user):
    user_dic = db_hander.user_select(login_user)
    return user_dic.get('balance')
```

## lib

### common.py（公用类，盐MD5加密，登录装饰器）

```python
import hashlib
from core import src
from conf import setting
import logging.config


# 盐加密，通名字加密 密码

def salt(username, password):
    password_ms5= hashlib.md5()
    password_ms5.update((username+password).encode('utf-8'))
    res = password_ms5.hexdigest()
    return res


# 登录认证装饰器
def login_auth(func):
    def inner(*args, **kwargs):
        if src.login_user:
            res = func(*args, **kwargs)
            return res
        else:
            print('未出示证明，无法享受服务')
            src.login()

    return inner


# 添加日志功能(日志功能在接口层使用)
def get_log(log_type):
    '''
    :param log_type:  user日志   bank日志   购物商城日志
    :return:
    '''
    # 1、加载日志配置信息
    logging.config.dictConfig(
        setting.LOGGING_DIC
    )
    # 获取日志对象
    logger = logging.getLogger(log_type)
    return logger
```

## log（日志文件记录）

### a1.log

```bash
2020-11-29 23:03:52,782 - MainThread:13396 - 日志名字:user - user_interface.py:58 -INFO - 用户：[q]登录成功！
2020-11-29 23:04:11,089 - MainThread:13396 - 日志名字:user - user_interface.py:58 -INFO - 用户：[w]登录成功！
2020-11-29 23:04:15,584 - MainThread:13396 - 日志名字:user - user_interface.py:69 -INFO - 用户不存在，请重新输入
```

整体项目架构不错，可以很清楚了解到三层架构的构建

用户点击：用户视图层————————》业务接口处理————————》数据库数据处理

数据返回用户：数据处理完数据————————》业务接口处理————————》用户视图层