+++
author = "南宫乘风"
title = "Python的类和对象"
date = "2019-09-05 14:06:48"
tags=[]
categories=['Python学习']
image = "post/4kdongman/57.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/100556646](https://blog.csdn.net/heian_99/article/details/100556646)

## 类和对象<br><br> class 类名<br>     类里面的东西<br>     <br>  

```
class c1:
    pass
```

## <br> 实例化一个类

```
a=c1()
```

## <br> 构造函数 （构造方法）<br>                 #self：在类中的方法必须加上seif参数<br>                #__init__(self,参数)

## <br> 构造函数实际意义：初始化

```
class c2:
    def __init__(self):
        print("南宫乘风")
```

## 给类加上参数：给构造方法加上参数

```
class c3:
    def __init__(self,name,job):
        print("我的名字"+name+"工作是"+job)
```

## <br>     <br> 属性：类里面的变量：self.属性名

```
class c4:
    def __init__(self,name,job):
        self.myname=name
        self.myjob=job
```

## 方法：类里面的函数：def 方法名（self，参数）

```
class c5:
    def fun1(self,name):
        print ("hello"+name)
```

```
class c6:
    def __init__(self,name):
        self.myname=name
    def fun2(self):
        print ("hello"+self.myname)
```

## <br> 继承（单继承，多继承）

#某一个家庭有父亲，母亲，儿子，女儿<br> #父亲可以说话，母亲可以写字<br> #儿子继承了父亲，女儿同时继承了父母,并且可听东西<br> #小儿子继承了父亲，但是优化了父亲的说话能力

```
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

<br>  
