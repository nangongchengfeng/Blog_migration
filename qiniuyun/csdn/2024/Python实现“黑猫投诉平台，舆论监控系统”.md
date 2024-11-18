---
author: 南宫乘风
categories:
- 项目实战
date: 2024-04-24 22:31:16
description: 黑猫投诉平台，舆论监控系统简介黑猫投诉舆论监控系统是一款专为快速识别和响应网络投诉而设计的应用，旨在帮助企业或机构第一时间掌握公众意见和反馈。通过实时监控网站及其他在线平台，系统能够迅速侦测到关于品牌。。。。。。。
image: ../../title_pic/49.jpg
slug: '202404242231'
tags:
- python
- 开发语言
title: Python实现“黑猫投诉平台，舆论监控系统”
---

<!--more-->

## 黑猫投诉平台，舆论监控系统
BuzzMonitor
[https://github.com/nangongchengfeng/BuzzMonitor.git](https://github.com/nangongchengfeng/BuzzMonitor.git)
## 简介
"黑猫投诉"舆论监控系统是一款专为快速识别和响应网络投诉而设计的应用，旨在帮助企业或机构第一时间掌握公众意见和反馈。通过实时监控网站及其他在线平台，系统能够迅速侦测到关于品牌或服务的负面评论、投诉或提议。
![在这里插入图片描述](../../image/976a2217f52847d4a7916bfcd40dc5a3.png)
## 流程
![在这里插入图片描述](../../image/9439a7e12db24299be58b7f2b352619e.png)
参考文档：https://blog.csdn.net/qq_45270849/article/details/135416529

## 针对企业公司关键字
比如：美团外卖

1、打开页面 https://tousu.sina.com.cn/company/view/?couid=1003626&sid=26857

2、找到商家列表，获取到couid的值，这就是关键字

3、根据关键字组合，解密获取到api接口的数据

![在这里插入图片描述](../../image/a2995a6769c8477f86506a892bfb187a.png)
## 定时任务
爬虫是定时任务驱动，使用apscheduler

```bash
    # 创建一个后台调度器
    scheduler = BackgroundScheduler(timezone="Asia/Shanghai")
    # 添加一个每隔20秒执行一次的定时任务 测试
    scheduler.add_job(func=send_alert, trigger="interval", seconds=20)
    # 添加一个每隔10分钟 执行的定时任务
    scheduler.add_job(func=get_heimao, trigger=CronTrigger(minute='*/10'))
    # 启动调度器
    scheduler.start()
    return app
```
## 发送钉钉告警
![在这里插入图片描述](../../image/1fa012982c5c44269c94502dcdfba9ee.png)
## 使用方式
1、数据库创建数据库名称和执行命令
![在这里插入图片描述](../../image/0972b1dd4e2247d2bd86292b6ebc8e7d.png)
![在这里插入图片描述](../../image/f0eaae5c28014cd1a2b4d74d7954dd77.png)

```bash
pip3 install Flask-Migrate

初始化(只需要执行一次)
flask db init
生成文件
flask db migrate
迁移数据库
flask db upgrade

记得 （我已经导入）
只需要在 app.py 中导入 models.py 中的类即可。
而且导入全部和导入一个，结果都是可以对所有的表进行创建。
```
2、设置爬虫的信息
![在这里插入图片描述](../../image/7e4baaa65bcc4354a554be9a487e8fc7.png)
## 接口分页获取数据库内容

```bash
http://127.0.0.1:5000/info/


        # 默认值
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
```
![在这里插入图片描述](../../image/66d90a81714b481595e9a4eb657413af.png)
![在这里插入图片描述](../../image/a8a55d284ce24860ab7beed226bde9c1.png)

