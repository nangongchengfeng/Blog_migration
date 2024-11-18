---
author: 南宫乘风
categories:
- Python学习
date: 2021-07-21 15:00:49
description: 在中实现文件的读写操作其实非常简单，通过内置的函数，我们可以指定文件名、操作模式、编码信息等来获得操作文件的对象，接下来就可以对文件进行读写操作了。这里所说的操作模式是指要打开什么样的文件字符文件还是。。。。。。。
image: http://image.ownit.top/4kdongman/69.jpg
tags:
- python
- list
- json
title: Python文件处理
---

<!--more-->

在Python中实现文件的读写操作其实非常简单，通过Python内置的`open`函数，我们可以指定文件名、操作模式、编码信息等来获得操作文件的对象，接下来就可以对文件进行读写操作了。这里所说的操作模式是指要打开什么样的文件（字符文件还是二进制文件）以及做什么样的操作（读、写还是追加），具体的如下表所示。

| 操作模式 | 具体含义 |
| --- | --- |
| `'r'` | 读取 （默认） |
| `'w'` | 写入（会先截断之前的内容） |
| `'x'` | 写入，如果文件已经存在会产生异常 |
| `'a'` | 追加，将内容写入到已有文件的末尾 |
| `'b'` | 二进制模式 |
| `'t'` | 文本模式（默认） |
| `'+'` | 更新（既可以读又可以写） |

Python文件处理，正确格式，防止有异常，我们需要加上try except

标准格式

```python
def main():
    f = None
    try:
        f = open('文件.txt', 'r', encoding='utf-8')
        print(f.read())
    except FileNotFoundError:
        print('无法打开指定的文件!')
    except LookupError:
        print('指定了未知的编码!')
    except UnicodeDecodeError:
        print('读取文件时解码错误!')
    finally:
        if f:
            f.close()
if __name__ == '__main__':
    main()
```

在Python中，我们可以将那些在运行时可能会出现状况的代码放在`try`代码块中，在`try`代码块的后面可以跟上一个或多个`except`来捕获可能出现的异常状况。例如在上面读取文件的过程中，文件找不到会引发`FileNotFoundError`，指定了未知的编码会引发`LookupError`，而如果读取文件时无法按指定方式解码会引发`UnicodeDecodeError`，我们在`try`后面跟上了三个`except`分别处理这三种不同的异常状况。最后我们使用`finally`代码块来关闭打开的文件，释放掉程序中获取的外部资源，由于`finally`块的代码不论程序正常还是异常都会执行到（甚至是调用了`sys`模块的`exit`函数退出Python环境，`finally`块都会被执行，因为`exit`函数实质上是引发了`SystemExit`异常），因此我们通常把`finally`块称为“总是执行代码块”，它最适合用来做释放外部资源的操作。如果不愿意在`finally`代码块中关闭文件对象释放资源，也可以使用上下文语法，通过`with`关键字指定文件对象的上下文环境并在离开上下文环境时自动释放文件资源，代码如下所示。

除了使用文件对象的`read`方法读取文件之外，还可以使用`for-in`循环逐行读取或者用`readlines`方法将文件按行读取到一个列表容器中，代码如下所示。

```python
import time
def main():
    # 一次性读取整个文件内容
    with open('文件.txt', 'r', encoding='utf-8') as f:
        print(f.read())
    # 通过for-in循环逐行读取
    with open('文件.txt', mode='r') as f:
        for line in f:
            print(line, end='')
            time.sleep(0.5)
    print()
    # 读取文件按行读取到列表中
    with open('文件.txt') as f:
        lines = f.readlines()
    print(lines)
if __name__ == '__main__':
    main()
```

通过上面的讲解，我们已经知道如何将文本数据和二进制数据保存到文件中，那么这里还有一个问题，如果希望把一个列表或者一个字典中的数据保存到文件中又该怎么做呢？答案是将数据以JSON格式进行保存。JSON是“JavaScript Object Notation”的缩写，它本来是JavaScript语言中创建对象的一种字面量语法，现在已经被广泛的应用于跨平台跨语言的数据交换，原因很简单，因为JSON也是纯文本，任何系统任何编程语言处理纯文本都是没有问题的。目前JSON基本上已经取代了XML作为异构系统间交换数据的事实标准。关于JSON的知识，更多的可以参考[JSON的官方网站](http://json.org)，从这个网站也可以了解到每种语言处理JSON数据格式可以使用的工具或三方库，下面是一个JSON的简单例子。

上面的JSON跟Python中的字典其实是一样一样的，事实上JSON的数据类型和Python的数据类型是很容易找到对应关系的，如下面两张表所示。

| JSON | Python |
| --- | --- |
| object | dict |
| array | list |
| string | str |
| number \(int / real\) | int / float |
| true / false | True / False |
| null | None |

```python
import json
def main():
    mydict = {
        'name': '小风',
        'age': 20,
        'qq': 95849158,
        'friends': ['张三', '李四'],
        'cars': [
            {'brand': 'BYD', 'max_speed': 180},
            {'brand': 'Audi', 'max_speed': 280},
            {'brand': 'Benz', 'max_speed': 320}
        ]
    }
    try:
        with open('data.json', 'w', encoding='utf-8') as fs:
            json.dump(mydict, fs)
    except IOError as e:
        print(e)
    print('保存数据完成!')
if __name__ == '__main__':
    main()
```

 

json模块主要有四个比较重要的函数，分别是：

- `dump` - 将Python对象按照JSON格式序列化到文件中
- `dumps` - 将Python对象处理成JSON格式的字符串
- `load` - 将文件中的JSON数据反序列化成对象
- `loads` - 将字符串的内容反序列化成Python对象