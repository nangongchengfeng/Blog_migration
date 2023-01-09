+++
author = "南宫乘风"
title = "再也不用担心Shell脚本出错-ShellCheck"
date = "2021-06-12 21:33:26"
tags=['shell', 'linux']
categories=['Linux Shell']
image = "post/4kdongman/47.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/117855814](https://blog.csdn.net/heian_99/article/details/117855814)

## 简介

写过shell脚本的人都知道，即便出现一些简单的语法错误，运行的时候也可能没有办法发现。有些看似运行正确的脚本，实际上**可能在某些分支，某些场景下仍然出现错误**，而有的写法可能运行正常，但是却不符合POSIX标准，**不具备可移植性**。

诚然，shell脚本是解释运行，没有办法向C/C++那样严格检查，但是我们仍然可以借助一些工具帮助我们**提前发现一些错误**。

## [shellcheck](https://github.com/koalaman/shellcheck)

github地址：[https://github.com/koalaman/shellcheck](https://github.com/koalaman/shellcheck)

shellcheck 是一款实用的 shell脚本静态检查工具。

首先，可以帮助你提前发现并修复简单的语法错误，节约时间。每次都需要运行才发现写错了一个小地方，确实非常浪费时间。<br> 其次，可以针对你当前不够完善不够健壮的写法，提供建议，帮助你提前绕开一些坑，避免等问题真的发生了才去调试处理。

在其介绍中，目标是针对所有用户的，从初学者到高手，都用得上
- 指出并澄清典型的初学者的语法问题，那通常会shell提供神秘的错误消息。- 指出并澄清典型的中级的语义问题，这些问题会导致shell出现奇怪且反直觉的行为。- 指出可能导致高级用户的脚本中，可能在未来某种情况下失败的陷阱。
### 在线使用

非常简单，在网页 [https://www.shellcheck.net](https://www.shellcheck.net/) 上，贴入你的脚本，运行检查即可

```
#!/bin/sh
for n in {1..$RANDOM}
do
  str=""
  if (( n % 3 == 0 ))
  then
    str="fizz"
  fi
  if [ $[n%5] == 0 ]
  then
    str="$strbuzz"
  fi
  if [[ ! $str ]]
  then
    str="$n"
  fi
  echo "$str"
done
```

shell<br> 它会给出错误提示或者建议：

```
$ shellcheck myscript
 
Line 2:
for n in {1..$RANDOM}
         ^-- SC3009: In POSIX sh, brace expansion is undefined.
             ^-- SC3028: In POSIX sh, RANDOM is undefined.
 
Line 5:
  if (( n % 3 == 0 ))
     ^-- SC3006: In POSIX sh, standalone ((..)) is undefined.
 
Line 9:
  if [ $[n%5] == 0 ]
       ^-- SC3007: In POSIX sh, $[..] in place of $((..)) is undefined.
       ^-- SC2007: Use $((..)) instead of deprecated $[..]
              ^-- SC3014: In POSIX sh, == in place of = is undefined.
 
Line 11:
    str="$strbuzz"
         ^-- SC2154: strbuzz is referenced but not assigned.
 
Line 13:
  if [[ ! $str ]]
     ^-- SC3010: In POSIX sh, [[ ]] is undefined.

$
```

![20210612212405188.png](https://img-blog.csdnimg.cn/20210612212405188.png)

每个可能的错误都提示了。新手写shell出现莫名的报错时，可以尝试使用奥。当然例子中很多并不是真的错误，而是某种写法不符合POSIX标准，这种情况也应该避免。

### 安装方式

在大多数发行版的包管理中，已经有shellcheck了，如在基于debian的机器上

```
apt-get install shellcheck

```

其他系统的具体安装方式，可以查阅 shellcheck 的github首页介绍

当然，也可以选择自行从源码安装。

我选择的就是二进制安装，直接放在/usr/bin/目录下，给权限就可以了

下载：[https://download.csdn.net/download/heian_99/19597695](https://download.csdn.net/download/heian_99/19597695)

github：[https://github.com/koalaman/shellcheck/releases/download/stable/shellcheck-stable.linux.x86_64.tar.xz](https://github.com/koalaman/shellcheck/releases/download/stable/shellcheck-stable.linux.x86_64.tar.xz)

测试

```
#!/bin/bash
if[ $# -eq 0 ]
then
    echo "no para"
else
    echo "$# para"
fi
exit 0
```

结果：

```
[root@redhat heian]# sh test.sh 
test.sh:行2: if[ 0 -eq 0 ]: 未找到命令
test.sh:行3: 未预期的符号 `then' 附近有语法错误
test.sh:行3: `then'
[root@redhat heian]# shellcheck test.sh 

In test.sh line 2:
if[ $# -eq 0 ]
  ^-- SC1069: You need a space before the [.

For more information:
  https://www.shellcheck.net/wiki/SC1069 -- You need a space before the [.

```

相关的报错已经给了解决的办法，也可以根据连接去查询更详细的原因。

### 问题列表

那么shellcheck具体会检查一些什么问题呢，以下给出一个不完整的问题检查列表。<br> 可以看下，你是否都能意识到这样的写法时有错误或隐患的。<br> 如果发现有自己不知道的或自己容易错漏的，那么也许你也应该花点时间，装上shellcheck。

<a name="_caption3"></a>

### <a name="t6"></a>引号问题

```
echo $1                           # Unquoted variables  #变量未加引号
find . -name *.ogg                # Unquoted find/grep patterns #find/grep 的匹配模式未加引号
rm "~/my file.txt"                # Quoted tilde expansion #引号中的波浪符扩展
v='--verbose="true"'; cmd $v      # Literal quotes in variables # 变量中的字面引号
for f in "*.ogg"                  # Incorrectly quoted 'for' loops # 错误的for循环
touch $@                          # Unquoted $@  # $@未加引号
echo 'Don't forget to restart!'   # Singlequote closed by apostrophe  # 单引号被撇号意外关闭了
echo 'Don\'t try this at home'    # Attempting to escape ' in ''  #试图在单引号括起来的部分中加上一个单引号
echo 'Path is $PATH'              # Variables in single quotes # 将变量用单引号括起来
trap "echo Took ${SECONDS}s" 0    # Prematurely expanded trap #过早扩展陷阱
```

### 条件判断

ShellCheck 可以识别大多数不正确的条件判断语句

```
[[ n != 0 ]]                      # Constant test expressions  # 常量测试表达式
[[ -e *.mpg ]]                    # Existence checks of globs # 对文件是否存在进行检查时，使用通配符
[[ $foo==0 ]]                     # Always true due to missing spaces #由于缺乏空格，结果总是为真
[[ -n "$foo " ]]                  # Always true due to literals #由于字面值存在，结果总是为真
[[ $foo =~ "fo+" ]]               # Quoted regex in =~   # 在 =~ 中使用正则表达式
[ foo =~ re ]                     # Unsupported [ ] operators # 不支持的[]运算符
[ $1 -eq "shellcheck" ]           # Numerical comparison of strings # 比较数字和字符串
[ $n &amp;&amp; $m ]                      # &amp;&amp; in [ .. ]  # 在[]中使用&amp;&amp;运算符
[ grep -q foo file ]              # Command without $(..)  #命令缺少了$(..)
[[ "$$file" == *.jpg ]]           # Comparisons that can't succeed #无法成功的比较
(( 1 -lt 2 ))                     # Using test operators in ((..)) #在((..))中使用比较
```

### 常见的对命令的错误使用

ShellCheck 可以识别对一些命令的错误使用

```
grep '*foo*' file                 # Globs in regex contexts  #在grep的正则表达式中前后使用通配符
find . -exec foo {} &amp;&amp; bar {} \;  # Prematurely terminated find -exec  # 使find -exec 过早结束
sudo echo 'Var=42' &gt; /etc/profile # Redirecting sudo # 重定向sudo
time --format=%s sleep 10         # Passing time(1) flags to time builtin # 将time(1)的标志传递给内建的time
while read h; do ssh "$h" uptime  # Commands eating while loop input  # 一个获取输入的while循环中，使用同样会获取输入的命令
alias archive='mv $1 /backup'     # Defining aliases with arguments # 定义使用参数的alias
tr -cd '[a-zA-Z0-9]'              # [] around ranges in tr # 在tr的参数范围外使用[]
exec foo; echo "Done!"            # Misused 'exec'  # 错误地使用exec
find -name \*.bak -o -name \*~ -delete  # Implicit precedence in find  # 在find中的隐式优先级
# find . -exec foo &gt; bar \;       # Redirections in find  #find中的重定向
f() { whoami; }; sudo f           # External use of internal functions #在外部使用内部函数
```

### 初学者的常见错误

ShellCheck 识别很多初学者的语法错误

```
var = 42                          # Spaces around = in assignments #等号两边的空格
$foo=42                           # $ in assignments # 对变量赋值时使用了$
for $var in *; do ...             # $ in for loop variables  # 在循环变量处使用$
var$n="Hello"                     # Wrong indirect assignment #错误的变量
echo ${var$n}                     # Wrong indirect reference #错误的引用
var=(1, 2, 3)                     # Comma separated arrays #逗号分割数组
array=( [index] = value )         # Incorrect index initialization #错误的索引初始化
echo $var[14]                     # Missing {} in array references #引用数组缺少{}
echo "Argument 10 is $10"         # Positional parameter misreference #错误的位置参数引用
if $(myfunction); then ..; fi     # Wrapping commands in $() #在命令外加上$()
else if othercondition; then ..   # Using 'else if'  #使用else if
f; f() { echo "hello world; }     # Using function before definition 在函数定义之前使用函数
[ false ]                         # 'false' being true # 此处false为true
if ( -f file )                    # Using (..) instead of test #使用()取代测试条件
```

### 数据和拼写错误

ShellCheck 可以识别一些数据和拼写错误

```
args="$@"                         # Assigning arrays to strings # 将数组赋值给字符串
files=(foo bar); echo "$files"    # Referencing arrays as strings # 把数字当成字符串引用
declare -A arr=(foo bar)          # Associative arrays without index # 不带索引组合数组
printf "%s\n" "Arguments: $@."    # Concatenating strings and arrays # 连接字符串和数组
[[ $# &gt; 2 ]]                      # Comparing numbers as strings # 把数字当成字符串比较
var=World; echo "Hello " var      # Unused lowercase variables # 未使用的小写变量
echo "Hello $name"                # Unassigned lowercase variables # 未赋值的小写变量
cmd | read bar; echo $bar         # Assignments in subshells # 在subshells中进行赋值
cat foo | cp bar                  # Piping to commands that don't read # 通过管道传递数据给一个不会做读取的程序
printf '%s: %s\n' foo             # Mismatches in printf argument count # pirintf参数数量不匹配
```

 

### 其他杂七杂八的问题

ShellCheck 可以识别到一些其他问题

```
PS1='\e[0;32m\$\e[0m '            # PS1 colors not in \[..\]  # PS1 的颜色不在\[..\] 中
PATH="$PATH:~/bin"                # Literal tilde in $PATH # $PATH中的波浪号
rm “file”                         # Unicode quotes #Unicode 引号
echo "Hello world"                # Carriage return / DOS line endings # 传输返回DOS行结束符/
echo hello \                      # Trailing spaces after \   # \后面的行尾空格
var=42 echo $var                  # Expansion of inlined environment # 展开内联环境变量
#!/bin/bash -x -e                 # Common shebang errors # shebang  命令错误
echo $((n/180*100))               # Unnecessary loss of precision # 不必要的精度丢失
ls *[:digit:].txt                 # Bad character class globs # 不好的通配符
sed 's/foo/bar/' file &gt; file      # Redirecting to input # 重定向到输入
while getopts "a" f; do case $f in "b") # Unhandled getopts flags # 未处理的getopts标志
```

### 总结

以上就是shellcheck的介绍了，主要来自其github 的readme ，源码在 [github](https://www.cnblogs.com/zqb-all/p/!https://github.comf/koalaman/shellcheck) [https://github.com/koalaman/shellcheck](https://github.comf/koalaman/shellcheck)

简单实用，只要配置好了，就可以持续为你提供帮助。而且这个是建议性的，可以自己根据实际情况决定是否采纳。即用即弃的临时脚本，那兼容性等就不用太care。长期使用的，就还是完善一下比较稳妥。

 

参考博客：[https://blog.csdn.net/whatday/article/details/105070638](https://blog.csdn.net/whatday/article/details/105070638)

微信：[https://mp.weixin.qq.com/s/jPZocFgl5OiDochx7rvI6w](https://mp.weixin.qq.com/s/jPZocFgl5OiDochx7rvI6w)

 
