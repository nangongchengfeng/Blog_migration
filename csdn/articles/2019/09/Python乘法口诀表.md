+++
author = "南宫乘风"
title = "Python乘法口诀表"
date = "2019-09-05 13:57:11"
tags=[]
categories=['Python学习']
image = "post/4kdongman/57.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/100556560](https://blog.csdn.net/heian_99/article/details/100556560)

# 乘法口诀表

```
print("乘法口诀表")

for i in range(1,10):
    for j in range(1,i+1):
        print(str(i)+str("*")+str(j)+"="+str(i*j),end=" ")
    print() 
```

# ![20190905135657950.png](https://img-blog.csdnimg.cn/20190905135657950.png)<br>         <br> 逆向乘法口诀表

```
print("逆向乘法口诀表")

for i in range(9,0,-1):
    for j in range(i,0,-1):
            print(str(i)+str("*")+str(j)+"="+str(i*j),end=" ")
    print()

```

![20190905135644667.png](https://img-blog.csdnimg.cn/20190905135644667.png)
