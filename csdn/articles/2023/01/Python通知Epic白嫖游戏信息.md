+++
author = "南宫乘风"
title = "Python通知Epic白嫖游戏信息"
date = "2023-01-03 18:13:53"
tags=['游戏']
categories=['Python学习']
image = "post/4kdongman/77.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/128495053](https://blog.csdn.net/heian_99/article/details/128495053)

### [每周都有免费游戏 - Epic Games](https://store.epicgames.com/zh-CN/free-games)<br> 近期看到Epic在送游戏，目前每周都会有活动白嫖。

身为白嫖党，肯定要操作一下。

[游戏列表：Epic Games Store 每周免费游戏（331） | indienova GameDB 游戏库](https://indienova.com/gamedb/list/121/p/1)

大致思路：

1、根据网站，获取可 “  白嫖  ”的游戏

2、处理相关信息，组成文本

3、发送到微信上，让我们知道。

## 1、查询网站

下面网页，会发布最新免费，可白嫖的游戏。我们爬取这些信息，进行判断

[游戏列表：Epic Games Store 每周免费游戏（331） | indienova GameDB 游戏库](https://indienova.com/gamedb/list/121/p/1)

![fd4ce46ee29941649c50596d99153ca2.png](https://img-blog.csdnimg.cn/fd4ce46ee29941649c50596d99153ca2.png)



## 2、代码编写

1.我们爬取网页的数据

2.获取网页中所有游戏的信息

3.判断游戏信息是最新编辑的

4.汇总信息进行发送到微信

相关实例代码

```
# -*- coding: utf-8 -*-
# @Time    : 2022/12/29 16:33
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : epic_all.py
# @Software: PyCharm
import json
import re
import time

import requests
from bs4 import BeautifulSoup


def get_url_info():
    url = 'https://indienova.com/gamedb/list/121/p/1'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.41'}
    res = requests.get(url, headers=headers).text
    return res


def check_epci_info(game_info_list):
    list_content = []
    for i in game_info_list:
        game_time = i['game_time']
        if '小时前' in game_time[0]:
            content = f"中文名称：{i['game_zh']}  &lt;br/&gt;" \
                      f"英文名称：{i['game_en']} &lt;br/&gt;" \
                      f"领取时间：{i['game_start']} &lt;br/&gt;" \
                      f"发布时间：{i['game_time']}&lt;br/&gt;&lt;br/&gt;"
            list_content.append(content)
    return list_content


def parse_web_page(res):
    soup = BeautifulSoup(res, "html.parser")
    res.encode('UTF-8').decode('UTF-8')
    div_class = soup.find(name='div', attrs={"id": "portfolioList"})
    # print(div_class[0])
    game_name = div_class.find_all(name='div', attrs={"class": "col-xs-12 col-sm-6 col-md-4 user-game-list-item"})
    list_game = str(game_name).split('&lt;div class="col-xs-12 col-sm-6 col-md-4 user-game-list-item"&gt;')
    game_info_list = []
    for i in list_game[1:]:
        dict_info = {}
        # print('----------------------------------------------------------------------------------')
        game = BeautifulSoup(i, "html.parser")
        game_all_info = game.find(name='h4')
        game_name_zh = game_all_info.find_all(name='a')
        game_name_en = game_all_info.find_all(name='small')
        game_name_zh = re.findall(r'&gt;(.+?)&lt;', str(game_name_zh))
        game_name_en = re.findall(r'&gt;(.+?)&lt;', str(game_name_en))
        # print(game_name_zh, game_name_en)
        game_start_end = game.find(name='p', attrs={"class": "intro"})
        game_start_end_new = game_start_end.find_all(name='span')
        game_edit_time = game.find(name='p', attrs={"class": "text-date"})
        game_edit_time_new = game_edit_time.find_all(name='small')
        game_edit_time_new = str(game_edit_time_new).replace(" ", "").replace("\n", " ")

        game_start_end_new = re.findall(r'&gt;(.+?)&lt;', str(game_start_end_new))
        game_edit_time_new = re.findall(r'&gt;(.+?)&lt;', str(game_edit_time_new))
        dict_info["game_zh"] = game_name_zh
        dict_info["game_en"] = game_name_en
        dict_info["game_start"] = game_start_end_new
        dict_info["game_time"] = game_edit_time_new
        game_info_list.append(dict_info)

    # print(game_start_end_new,game_edit_time_new)
    return game_info_list


def send_to_epic_message(list_content):
    content = ''.join(list_content) + '\nhttps://indienova.com/gamedb/list/121/p/1'
    token = 'tokenxxxxxxxxxxxxxxxxxxxx'
    day_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    title = f'Epic免费游戏-{day_time}'  # 改成你要的标题内容
    error_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 获取格式化的时间
    url = 'http://www.pushplus.plus/send'
    data = {
        "token": token,  # 密钥
        "title": title,  # 标题
        "content": content,  # 发送的信息内容，这里我们是json数组
        "template": "markdown"  # 数据类型为json
    }
    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    request_result = requests.post(url, data=body, headers=headers)


# print(request_result)  # &lt;Response [200]&gt;

if __name__ == '__main__':
    res = get_url_info()
    game_info_list = parse_web_page(res)
    list_content = check_epci_info(game_info_list)
    send_to_epic_message(list_content)

```

## 3、发送平台（pushplus）

微信公众号关注

[pushplus(推送加)-微信消息推送平台](http://www.pushplus.plus/)

获取token进行配置即可。



## 4、定时任务

我们要把脚本部署到Linux操作环境 上。

首先记得安装依赖。pip install 模块

定时任务，每天10点运行一次。

```
0 10 * * * /usr/bin/python3 /opt/epic_send.py
```



![0de7026a73ce401888516ffa824c7f2e.png](https://img-blog.csdnimg.cn/0de7026a73ce401888516ffa824c7f2e.png)





![da0528e805d34782b54f30a576164b4b.png](https://img-blog.csdnimg.cn/da0528e805d34782b54f30a576164b4b.png)



## 5、增加 喜加一 的资讯通知

网站为[steam free game，steam free promotion - Steam Stats](https://steamstats.cn/xi)

![f47039d1dd304c5bb4a5a95941bbef6b.png](https://img-blog.csdnimg.cn/f47039d1dd304c5bb4a5a95941bbef6b.png)



```
# -*- coding: utf-8 -*-
# @Time    : 2022/12/29 15:51
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : epic.py
# @Software: PyCharm
import json
import time

import requests
from bs4 import BeautifulSoup


def get_free():
    url = 'https://steamstats.cn/xi'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.41'}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, "html.parser")
    text = "今日喜加一 &lt;br&gt;" + 'https://steamstats.cn/xi' + '&lt;br&gt;'

    tbody = soup.find('tbody')
    tr = tbody.find_all('tr')
    i = 1
    for tr in tr:
        td = tr.find_all('td')
        name = td[1].string.strip().replace('\n', '').replace('\r', '')
        gametype = td[2].string.replace(" ", "").replace('\n', '').replace('\r', '')
        start = td[3].string.replace(" ", "").replace('\n', '').replace('\r', '')
        end = td[4].string.replace(" ", "").replace('\n', '').replace('\r', '')
        time = td[5].string.replace(" ", "").replace('\n', '').replace('\r', '')
        oringin = td[6].find('span').string.replace(" ", "").replace('\n', '').replace('\r', '')
        text = text + "序号：" + str(
            i) + '&lt;br&gt;' + "游戏名称：" + name + '&lt;br&gt;' + "DLC/game：" + gametype + '&lt;br&gt;' + "开始时间：" + start + '&lt;br&gt;' + "结束时间：" + end + '&lt;br&gt;' + "是否永久：" + time + '&lt;br&gt;' + "平台：" + oringin + '&lt;br&gt;'
    # print(text)
        i++
    return text


def send_to_epic_message(text_info):
    content = ''.join(text_info)
    token = 'xxxxxxxxxxxxxxxxx'
    day_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    title = f'喜加一 免费游戏-{day_time}'  # 改成你要的标题内容
    error_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 获取格式化的时间
    url = 'http://www.pushplus.plus/send'
    data = {
        "token": token,  # 密钥
        "title": title,  # 标题
        "content": content,  # 发送的信息内容，这里我们是json数组
        "template": "markdown"  # 数据类型为json
    }
    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    request_result = requests.post(url, data=body, headers=headers)


if __name__ == "__main__":
    game_info = get_free()
    if len(game_info) &gt; 40:
        send_to_epic_message(get_free())

```





![687eff663beb4ca485724613b23138b6.png](https://img-blog.csdnimg.cn/687eff663beb4ca485724613b23138b6.png)

 

 

参考文档：[python获取steam/epic喜加一信息并自动发送到微信 - 知乎](https://zhuanlan.zhihu.com/p/421129986)
