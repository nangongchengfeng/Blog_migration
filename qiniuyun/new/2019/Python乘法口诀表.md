---
author: 南宫乘风
categories:
- Python学习
date: 2019-09-05 13:57:11
description: 乘法口诀表乘法口诀表逆向乘法口诀表逆向乘法口诀表。。。。。。。
image: http://image.ownit.top/4kdongman/34.jpg
tags:
- 技术记录
title: Python乘法口诀表
---

<!--more-->

# 乘法口诀表

```python
print("乘法口诀表")

for i in range(1,10):
    for j in range(1,i+1):
        print(str(i)+str("*")+str(j)+"="+str(i*j),end=" ")
    print() 
```

# ![](http://image.ownit.top/csdn/20190905135657950.png)  
          
逆向乘法口诀表

```python
print("逆向乘法口诀表")

for i in range(9,0,-1):
    for j in range(i,0,-1):
            print(str(i)+str("*")+str(j)+"="+str(i*j),end=" ")
    print()
```

![](http://image.ownit.top/csdn/20190905135644667.png)