+++
author = "南宫乘风"
title = "Vim文本编辑器详细用法"
date = "2019-01-19 19:03:12"
tags=['linux']
categories=[' Linux基础']
image = "post/4kdongman/95.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/86555639](https://blog.csdn.net/heian_99/article/details/86555639)

## <a id="1_ViVim_0"></a>1 Vi、Vim文本编辑器

1．Vi、Vim<br> Vi是Visual interface的简称。<br> Vim是Vi的增强版，即Vi Improved。在后面的实例中将介绍Vim的使用。

## <a id="vi_8"></a>为什么学vi？

1）所有的Unix Like 系统都会内建 vi 文本编辑器，其他的文本编辑器则不一定会存在；<br> 2）很多个别软件的编辑接口都会主动呼叫 vi (例如未来会谈到的 crontab, visudo, edquota 等指令)；<br> 3）vim 具有程序编辑的能力，可以主动的以字体颜色辨别语法癿正确性，方便程序设计；<br> 4）因为程序简单，编辑速度相当快速。

**系统自带教程：vimtutor<br> vim [options] [filelist]<br> 常用选项：<br> +[num]<br> +/{pat}**

## <a id="1_21"></a>1、工作模式、命令模式、输入模式和末行模式

![20190119184917217.png](https://img-blog.csdnimg.cn/20190119184917217.png)<br> Vim拥有5种编辑模式：命令模式、输入模式、末行模式、可视化模式、查询模式。<br> 1）．命令模式（其它模式→ESC）<br> 2）．输入模式（命令模式→a、i、o、A、I、O）<br> 3）．末行模式（命令模式→:）<br> 4）．可视化模式（命令模式→v）<br> 5）．查询模式（命令模式→?、/）

## <a id="2_31"></a>2、模式之间切换

![20190119185126706.png](https://img-blog.csdnimg.cn/20190119185126706.png)<br> **命令模式：**<br> ![2019011918522467.png](https://img-blog.csdnimg.cn/2019011918522467.png)<br> ![20190119185236884.png](https://img-blog.csdnimg.cn/20190119185236884.png)<br> ![20190119185247593.png](https://img-blog.csdnimg.cn/20190119185247593.png)<br> **输入模式：**

新增 (append)

a ：从光标所在位置後面开始新增资料，光标後的资料随新增资料向後移动。<br> A： 从光标所在列最後面的地方开始新增资料。

插入 (insert)

i： 从光标所在位置前面开始插入资料，光标後的资料随新增资料向後移动。<br> I ：从光标所在列的第一个非空白字元前面开始插入资料。

开始 (open)

o ：在光标所在列下新增一列并进入输入模式。<br> O: 在光标所在列上方新增一列并进入输入模式

**末行模式：**<br> ![20190119185605373.png](https://img-blog.csdnimg.cn/20190119185605373.png)<br> ![20190119185619908.png](https://img-blog.csdnimg.cn/20190119185619908.png)<br> ![20190119185636316.png](https://img-blog.csdnimg.cn/20190119185636316.png)

## <a id="3_59"></a>3、打开文件

vim /path/to/somefile<br> vim +# :打开文件，并定位于第#行<br> vim +：打开文件，定位至最后一行<br> vim +/PATTERN : 打开文件，定位至第一次被PATTERN匹配到的行的行首<br> 默认处于编辑模式

## <a id="4_66"></a>4、关闭文件

1、末行模式关闭文件<br> :q 退出<br> :wq 保存并退出<br> :q! 不保存并退出<br> :w 保存<br> :w! 强行保存<br> :wq --&gt; :x<br> 2、编辑模式下退出<br> ZZ: 保存并退出

## <a id="4_77"></a>4、移动光标(编辑模式)

1、逐字符移动：<br> h: 左<br> l: 右<br> j: 下<br> k: 上<br> #h: 移动#个字符；

2、以单词为单位移动<br> w: 移至下一个单词的词首<br> e: 跳至当前或下一个单词的词尾<br> b: 跳至当前或前一个单词的词首

#w:

3、行内跳转：<br> 0: 绝对行首<br> ^: 行首的第一个非空白字符<br> $: 绝对行尾<br> home<br> end

4、行间跳转<br> #G：跳转至第#行；<br> G：最后一行<br> 1G：跳转到第1行首===gg

末行模式下，直接给出行号即可<br> :5 直接定位到第5行首

## <a id="5_107"></a>5、翻屏

Ctrl+f: 向下翻一屏<br> Ctrl+b: 向上翻一屏

Ctrl+d: 向下翻半屏<br> Ctrl+u: 向上翻半屏

## <a id="6_115"></a>6、删除单个字符

x: 删除光标所在处的单个字符<br> #x: 删除光标所在处及向后的共#个字符

## <a id="7_d_120"></a>7、删除命令: d

d命令跟跳转命令组合使用；<br> #dw, #de, #db

dd: 删除当前光标所在行<br> #dd: 删除包括当前光标所在行在内的#行；

末行模式下：<br> StartADD,EndADDd<br> .: 表示当前行<br> $: 最后一行<br> +#: 向下的#行

## <a id="8_p_134"></a>8、粘贴命令 p

p: 如果删除或复制为整行内容，则粘贴至光标所在行的下方，如果复制或删除的内容为非整行，则粘贴至光标所在字符的后面；<br> P: 如果删除或复制为整行内容，则粘贴至光标所在行的上方，如果复制或删除的内容为非整行，则粘贴至光标所在字符的前面；

## <a id="9_y_139"></a>9、复制命令 y

用法同d命令<br> yy 复制1行<br> 5yy 复制5行

## <a id="10_146"></a>10、修改：先删除内容，再转换为输入模式

c: 用法同d命令

## <a id="11r_150"></a>11、替换：r

R: 替换模式

## <a id="12_u_154"></a>12、撤消编辑操作 u

u：撤消前一次的编辑操作<br> 连续u命令可撤消此前的n次编辑操作<br> #u: 直接撤消最近#次编辑操作

撤消最近一次撤消操作：Ctrl+r

## <a id="13_163"></a>13、可视化模式

v: 按字符选取<br> 该模式下通过光标移动选择文本，选取后按 y 可以把文本提取到缓冲区（即复制），c 可以剪切。之后可以使用p在光标后粘贴，P粘贴在光标前<br> V：按矩形选取<br> V是行选取模式，以行为单位进行选取。Ctrl+v是块选取模式，可以选取一块矩形区域中的文本。

## <a id="14_170"></a>14、查找

/PATTERN<br> ?PATTERN<br> n<br> N

## <a id="15_177"></a>15、查找并替换

```
	在末行模式下使用s命令
	ADDR1,ADDR2s@PATTERN@string@gi
	1,$
	%：表示全文	
	:s/root/admin/  替换光标所在行第一个root为admin
	:s/root/admin/g 替换光标所在行所有root为admin
	:1,5 s/root/admin/g 替换第1-5行所有root为admin
	:1,$ s/admin/root/g 替换所有行的admin为root ==== 1,$ 等价于%

```

## <a id="16vim_190"></a>16、使用vim编辑多个文件

vim FILE1 FILE2 FILE3<br> :next 切换至下一个文件<br> :prev 切换至前一个文件<br> :last 切换至最后一个文件<br> :first 切换至第一个文件

退出<br> :qa 全部退出

## <a id="17_201"></a>17、分屏显示一个文件

Ctrl+w, s: 水平拆分窗口<br> Ctrl+w, v: 垂直拆分窗口

在窗口间切换光标：<br> Ctrl+w, ARROW(表示上下左右箭头)

```
:qa 关闭所有窗口

```

## <a id="18_211"></a>18、分窗口编辑多个文件

vim -o : 水平分割显示<br> vim -O : 垂直分割显示

## <a id="19_216"></a>19、将当前文件中部分内容另存为另外一个文件

末行模式下使用w命令 <br> :w <br> :ADDR1,ADDR2w /path/to/somewhere

## <a id="20_222"></a>20、将另外一个文件的内容填充在当前文件中

:r /path/to/somefile

## <a id="21shell_226"></a>21、跟shell交互

:! COMMAND

## <a id="22_231"></a>22、高级话题

1、显示或取消显示行号<br> :set number<br> :set nu

:set nonu

2、显示忽略或区分字符大小写<br> :set ignorecase<br> :set ic

:set noic

3、设定自动缩进<br> :set autoindent<br> :set ai<br> :set noai

4、查找到的文本高亮显示或取消<br> :set hlsearch<br> :set nohlsearch

5、语法高亮<br> :syntax on<br> :syntax off

## <a id="23_258"></a>23、配置文件

```
/etc/vimrc
~/.vimrc
set hlsearch            "高亮度反白
set backspace=2     "可随时用退格键删除
set autoindent        "自动缩排
set tabstop=4			"缩进
set softtabstop=4   softtabstop是“逢4空格进1制表符”,前提是你tabstop=4
set shiftwidth=4      自动缩进空格长度
set mouse=a				"使用鼠标
set selection=exclusive
set selectmode=mouse,key
set ruler               "可显示最后一行的状态
set showmode            "左下角那一行的状态
set nu                  "可以在每一行的最前面显示行号啦！
set bg=dark             "显示不同的底色色调
syntax on               "进行语法检验，颜色显示	

```
