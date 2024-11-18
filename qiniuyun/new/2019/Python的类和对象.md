---
author: 南宫乘风
categories:
- Python学习
date: 2019-09-05 14:06:48
description: 类和对象类名类里面的东西实例化一个类构造函数构造方法：在类中的方法必须加上参数参数构造函数实际意义：初始化南宫乘风给类加上参数：给构造方法加上参数我的名字工作是属性：类里面的变量：属性名方法：类里面的。。。。。。。
image: http://image.ownit.top/4kdongman/26.jpg
tags:
- 技术记录
title: Python的类和对象
---

<!--more-->

## 类和对象  
  
class 类名  
    类里面的东西  
      
 

```python
class c1:
    pass
```

##   
实例化一个类

```python
a=c1()
```

##   
构造函数 （构造方法）  
                \#self：在类中的方法必须加上seif参数  
               \#\_\_init\_\_\(self,参数\)

##   
构造函数实际意义：初始化

```python
class c2:
    def __init__(self):
        print("南宫乘风")
```

## 给类加上参数：给构造方法加上参数

```python
class c3:
    def __init__(self,name,job):
        print("我的名字"+name+"工作是"+job)
```

##   
      
属性：类里面的变量：self.属性名

```python
class c4:
    def __init__(self,name,job):
        self.myname=name
        self.myjob=job
```

## 方法：类里面的函数：def 方法名（self，参数）

```python
class c5:
    def fun1(self,name):
        print ("hello"+name)
```

```python
class c6:
    def __init__(self,name):
        self.myname=name
    def fun2(self):
        print ("hello"+self.myname)
```

##   
继承（单继承，多继承）

#某一个家庭有父亲，母亲，儿子，女儿  
#父亲可以说话，母亲可以写字  
#儿子继承了父亲，女儿同时继承了父母,并且可听东西  
#小儿子继承了父亲，但是优化了父亲的说话能力

```python
#父亲类
class father():
    def speak(self):
        print("I can speak")
#单继承：class子类（父亲）

#儿子类
class son(father):
    pass

#母亲类
class mother():
    def write(self):
        print("I can write")
        
#多继承
#女儿类
class daugther(father,mother):
    def listen(self):
        print("I can listen")

#重载：（重载）
#小儿子类
class son2(father):
    def speak(self):
        print("I can speak2")
```