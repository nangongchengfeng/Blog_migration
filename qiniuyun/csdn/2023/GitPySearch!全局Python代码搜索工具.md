---
author: 南宫乘风
categories:
- Python学习
- 项目实战
date: 2023-06-21 18:41:14
description: 一、背景在某些情况下，我们需要快速了解哪些项目包含特定的配置，例如使用了库或数据库的连接配置。然而，在上逐个代码仓库进行搜索是非常耗时的。为了提高效率，我们开发了一个脚本工具，用于实现全局搜索功能。该。。。。。。。
image: ../../title_pic/39.jpg
slug: '202306211841'
tags:
- python
- java
- 前端
title: GitPySearch- 全局Python代码搜索工具
---

<!--more-->

##  一 、背景

在某些情况下，我们需要快速了解哪些项目包含特定的配置，例如使用了fastjson库或数据库的连接配置。然而，在GitLab上逐个代码仓库进行搜索是非常耗时的。为了提高效率，我们开发了一个Python脚本工具，用于实现全局搜索功能。

该脚本能够在GitLab上对所有项目进行全局搜索，帮助我们快速确定哪些项目使用了特定的配置。无论项目数量是几个、几十个还是上百个，这个脚本都能够节省大量的时间和精力。

使用这个工具，我们可以根据关键词（如库名、配置项等）进行搜索，并获取包含该关键词的项目列表。脚本会自动遍历所有项目，并返回符合条件的项目链接，方便我们进一步查看和分析。

无论是对大型团队还是个人开发者，这个工具都能提供便利。它能够高效地帮助我们了解项目中的配置使用情况，加快问题排查和代码审查的速度。

如果你的项目数量较少，只有几个项目，并且能够轻松在GitLab上逐个搜索，那么这个脚本可能并不适用于你。但是，当你面对数十甚至上百个项目时，这个脚本将成为你的得力助手，提供高效的全局搜索能力。

通过这个GitLab全局搜索文本工具，我们能够更快地发现项目中的配置使用情况，优化代码结构，提高开发效率，以及更好地管理和维护项目。


## 二、原理流程

1. 用户输入GitLab的URL和访问令牌。
2. 系统使用输入的URL和访问令牌与GitLab建立连接。
3. 系统调用GitLab模块，获取GitLab中的所有项目ID。
4. 对于每个项目ID，系统构建搜索接口URL，包括关键字和项目ID作为参数。
5. 系统使用请求库向搜索接口发送HTTP请求，获取搜索结果页面内容。
6. 系统使用XPath解析搜索结果页面内容，提取相关信息。
7. 如果搜索结果存在：
   - 系统判断关键字匹配成功，并将匹配到的项目ID和关键字相关信息存储起来。
   - 可选：系统展示匹配到关键字的项目信息给用户。
8. 继续处理下一个项目ID，重复步骤4-7，直到所有项目ID处理完毕。
9. 系统输出所有匹配到关键字的项目信息。
10. 项目流程结束。

## 三、python版本与依赖
python:3.8.0 (如果本地已有python3的环境则不需要通过docker)
python依赖的module如下：

```bash
import json
import os

import requests
from lxml import etree
from multiprocessing import Pool
import gitlab

```
## 四、 操作步骤
### 1、安装上面的模块

```bash
pip install lxml     -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install    gitlab  -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2、获取Gitlab的token
要获取GitLab的访问令牌（Token），请按照以下步骤操作：

1. 登录到GitLab账户。
2. 在右上角的用户菜单中，点击"Settings"选项。
3. 在左侧导航栏中，选择"Access Tokens"选项。
4. 在"Personal Access Tokens"部分，点击"Create a token"按钮。
5. 输入访问令牌的名称和过期日期（可选）。
6. 选择所需的权限范围（API、读取用户信息等）。
7. 点击"Create personal access token"按钮。
8. 访问令牌将被生成，并显示在屏幕上。请务必复制该令牌并妥善保存，因为它将在创建后只显示一次。

注意事项：

- 访问令牌具有与您的账户相同的权限，请谨慎保管，并仅将其用于受信任的应用程序或脚本。
- 如果不再需要访问令牌或想要撤销访问权限，请返回到"Access Tokens"页面，并点击相应的撤销按钮。

请注意，获取访问令牌需要有相应的权限，如果您无法找到或访问"Access Tokens"选项，请联系您的GitLab管理员以获取帮助。
![在这里插入图片描述](../../image/f9e617fe8df649f891b4c3f2d735e7b7.png)

### 3、获取Gitlab接口的cookie
要获取GitLab接口的Cookie，可以按照以下步骤操作：

1. 打开浏览器并登录到GitLab账户。
2. 在登录成功后，打开浏览器的开发者工具（通常是按F12键或右键点击页面并选择"检查"或"开发者工具"选项）。
3. 在开发者工具中，切换到"网络"（Network）选项卡。
4. 在浏览器中执行需要获取Cookie的操作，例如访问某个页面或执行某个API请求。
5. 在开发者工具中，您将看到所有网络请求的记录。
6. 在请求列表中，找到与GitLab相关的请求。
7. 点击该请求，在请求详细信息的右侧面板中，可以找到请求头（Headers）的信息。
8. 在请求头中，查找名为"Cookie"的字段。该字段的值即为GitLab接口的Cookie。

请注意，Cookie包含了用户的身份验证信息，因此请妥善保管Cookie，并仅将其用于合法和授权的用途。同时，获取Cookie需要有相应的权限，如果您无法获取Cookie，请联系您的GitLab管理员以获取帮助。
![在这里插入图片描述](../../image/46d671c2240f41ff9179746ea19c3a82.png)

### 4、Python代码

```python
# -*- coding: utf-8 -*-
# @Time    : 2023/6/21 14:20
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : git_prod_scan.py
# @Software: PyCharm
import json
import os

import requests
from lxml import etree
from multiprocessing import Pool
import gitlab

# 需要检索的内容关键字
search_content = 'yunkedai'
token = 'xxxxx-Y9FLN'
gitlab_url = 'https://gitlab.xxxx.com/'
gl = gitlab.Gitlab(gitlab_url, token)
private_Cookie = 'xxxxxxx'

headers = {
    'Cookie': private_Cookie
}


def get_all_projects():
    data = []
    for g in gl.groups.list(all=True):
        for p in g.projects.list(all=True):
            project = gl.projects.get(p.id)
            item = {
                "id": p.id,
                "group": g.name,
                "project": p.name
            }
            data.append(item)

    # 将数据保存为 JSON 文件
    with open('all_output.json', 'w') as file:
        json.dump(data, file, indent=4)


def getProject(s):
    """
    根据项目 ID 获取项目信息并打印项目链接
    """
    url = "%s/search?utf8=&snippets=&scope=&search=%s&project_id=%s" % (gitlab_url, search_content, s)
    response = requests.get(url, headers=headers)
    pagehtml = etree.HTML(response.text)
    try:
        li_element = pagehtml.xpath('//li[@data-qa-selector="code_tab"]')[0]
        projecttitle = li_element.xpath('.//span/text()')[0]

        if int(projecttitle) > 0:
            # 查询项目信息
            project = gl.projects.get(s)

            # 获取项目链接
            project_url = project.web_url

            print("项目存在关键词：" + project_url)
        else:
            return
    except IndexError:
        pass


def start_project():
    pool = Pool(processes=5)
    # 读取项目数据
    with open('all_output.json', 'r') as file:
        data = file.read()
    data = json.loads(data)

    # 并发调用 getProject 函数
    for i in data:
        id = i.get('id')
        pool.apply_async(func=getProject, args=(id,))

    print('end')
    pool.close()
    pool.join()
    print("================================================================")
    print("所有项目已扫描完毕")


if __name__ == '__main__':
    file_path = 'all_output.json'
    if os.path.isfile(file_path):
        start_project()
    else:
        get_all_projects()
        start_project()

```

## 五、测试效果
我要 获取 所有项目  包含 **hire_core**  的关键字

请修改代码层面
```bash
search_content = 'hire_core'
```

**执行脚本**
![在这里插入图片描述](../../image/211e700d56264206b57d6daf6c39aac7.png)

##  六、总结
上面的GitLab全局Python代码搜索工具具有以下优势：

1. 搜索效率高：该工具通过使用GitLab的API接口进行搜索，避免了手动在每个项目中进行搜索的繁琐过程。它能够快速扫描多个项目，从而节省了大量的时间和精力。
2. 全面性：该工具可以在GitLab上进行全局搜索，即同时搜索所有项目，而不仅仅局限于单个项目。这样可以确保没有遗漏任何一个项目，提高了搜索的全面性和准确性。
3. 多线程支持：工具采用了多线程的并发处理方式，可以同时处理多个项目的搜索请求，提高了搜索效率。这意味着可以快速地并发搜索大量的项目，更快地找到符合条件的代码片段。
4. 输出结果清晰：工具会输出符合搜索条件的项目链接，让用户能够直观地查看项目和相关代码。这方便了用户对搜索结果的检查和进一步的处理。
5. 灵活可扩展：工具的代码结构清晰，易于理解和修改。用户可以根据自己的需求进行定制和扩展，例如修改搜索关键字、调整并发线程数等，以适应不同的搜索场景和项目规模。
