---
author: 南宫乘风
categories:
- Python学习
date: 2019-05-12 21:48:08
description: 一、的优缺点优点：优美、清晰、简单高级语言开发效率高可移植性、可拓展性、可嵌入性缺点：运行速度慢代码不能加密线程不能利用多二、与的区别代码：：代码混乱，重复代码较多，冗余：代码崇尚优美、清晰、简单：：。。。。。。。
image: http://image.ownit.top/4kdongman/07.jpg
tags:
- 技术记录
title: Python基础知识
---

<!--more-->

# 一、python的优缺点

## 　　优点：

1.  优美、清晰、简单
2.  高级语言
3.  开发效率高
4.  可移植性、可拓展性、可嵌入性

## 　　缺点：

1.  运行速度慢
2.  代码不能加密
3.  线程不能利用多CPU

# 二、python2与python3的区别

## 　　代码：

1.  python2：代码混乱，重复代码较多，冗余
2.  python3：代码崇尚优美、清晰、简单

## 　　print：

1.  python2：print是一个语句
2.  python3：print是一个函数

## 　　input：

1.  python2：raw\_input\(\)接收字符串，input\(\)接收数字
2.  python3：input\(\)接收的全部是字符串

## 　　编码方式：

1.  python2：默认编码是ASCII码（若想使用中文：#\_\*\_coding:utf-8\_\*\_）
2.  python3：默认编码是utf-8，支持中文

## 　　不等运算符：

1.  python2：可以使用\!=或者>\<
2.  python3：只能使用\!=

## 　　创建迭代计数器：

1.  python2：xrange
2.  python3：range

## 　　repr：

1.  python2：repr可以是语句
2.  python3：只允许使用repr\(\)函数

## 　　文件：

1.  python2：可以使用\!=或者>\<
2.  python3：只能使用\!=

## 　　整型：

1.  python2：存在long型
2.  python3：全部为int型

## 　　修改语法：

1.  python2：字典的keys，values，items以及map，filter，reduce返回的都是一个列表
2.  python3：字典的keys，values，items以及map，filter，reduce返回一个可迭代对象

## 　　新增语法：

1.  python2：print和exec语句，无nolocal等方法
2.  python3：print和exec改为函数，新增nolocal等方法

## 　　继承：

1.  python2：默认经典类（新式类需要\(object\)）
2.  python3：只有新式类

# 三、开发的种类

## 　　编译型

　　缺点：排错慢，开发效率低，不可移植

　　优点：执行效率高

　　典型：C语言，go语言

## 　　解释型

　　缺点：执行效率低

　　优点：排错快，开发效率高，可移植

　　典型：python，PHP

## 　　混合型

　　典型：java，C#

# 四、python的种类

　　Cpython：基于C语言开发的

　　lpython

　　Jpython

　　PyPy：目前执行最快的

# 五、变量与常量

　　常量：一直不变的量，约定俗称，全部大写为常量

 

　　变量：把程序的运行结果存放在内存中，以便后期代码的调用

　　要求：

1.  必须由数字、字母、下划线组成
2.  不能以数字开头
3.  不能是关键字
4.  不能是中文，不能太长，要有可描述性
5.  官网推荐下划线old\_boy和驼峰体OldBoy