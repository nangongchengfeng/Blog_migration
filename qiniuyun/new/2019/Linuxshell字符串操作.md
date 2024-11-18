---
author: 南宫乘风
categories:
- Linux
- Shell
date: 2019-04-10 21:47:37
description: 脚本中对字符串的处理变量名作用：返回字符串的长度返回字符串的长度变量名：：作用：截取字符串，指定截取的长度，也可以不写，字符串的第一个字符的索引值为从下标为的字符开始截取，共截取个从下标为的字符开始截。。。。。。。
image: http://image.ownit.top/4kdongman/89.jpg
tags:
- linux
title: Linux shell 字符串操作
---

<!--more-->

# shell脚本中对字符串的处理

### 1 \$\{#变量名\}

作用：返回字符串的长度

```
# foo="this is a test"
# echo ${#foo}    //返回字符串的长度
14
```

### 2  \$\{变量名：offset：length\}

作用：截取字符串，length指定截取的长度，也可以不写，字符串的第一个字符的索引值为0

```
# foo=“abcdefg”
# echo ${foo:3:2}    //从下标为3的字符开始截取，共截取2个
de
# echo  ${foo:3}    //从下标为3的字符开始截取到最后的字符
defg
```

###   
3  \$\{变量名#pattern\}   \$\{变量名##pattern\}

pattern：模式，通配符表达式  
作用：清除字符串中符合pattern的字符，从字符串最前匹配

```
# foo=“file.txt.zip”
# echo ${foo#*.}    //一个#号代表按照最短匹配清除
txt.zip
# echo ${foo##*.}   //2个#号代表按照最长匹配清除
zip
```

### 4 \$\{变量名\%pattern\}   \$\{变量名\%\%pattern\}

pattern：模式，通配符表达式  
作用：清除字符串中符合pattern的字符，从字符串最后匹配

```
# foo=“file.txt.zip”
# echo ${foo%.*}    //一个%号代表按照最短匹配清除
file.txt
# echo ${foo%%.*}   //2个%号代表按照最长匹配清除
file
```

###   
5 字符串替换操作

\$\{变量名/old/new\}

```
[root@wei ~]# foo="mp3.txt.txt.mp3.avi"
[root@wei ~]# echo ${foo/txt/TXT}
mp3.TXT.txt.mp3.avi
[root@wei ~]# echo ${foo//txt/TXT}
mp3.TXT.TXT.mp3.avi
```

```
[root@wei ~]# foo="txt.txt.txt"
[root@wei ~]# echo ${foo/#txt/TXT}
TXT.txt.txt
[root@wei ~]# echo ${foo/%txt/TXT}
txt.txt.TXT
```

###   
6 实现大小写字母的转换

大写转换小写

```
[root@wei ~]# foo="ABcd"
[root@wei ~]# echo ${foo,}
aBcd
[root@wei ~]# echo ${foo,,}
abcd
```

  
小写转换大写  
 

```
[root@wei ~]# echo ${foo^}
AbCD
[root@wei ~]# echo ${foo^^}
ABCD
```