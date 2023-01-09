+++
author = "南宫乘风"
title = "Django开发告警接口（webhook）对接Altermanager告警"
date = "2022-11-28 17:56:43"
tags=['python', 'django', '告警']
categories=['Prometheus监控', 'Python学习']
image = "post/4kdongman/88.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/123938428](https://blog.csdn.net/heian_99/article/details/123938428)

**告警日志统计 **

![9a058cb81d1e4927962dd821620de729.png](https://img-blog.csdnimg.cn/9a058cb81d1e4927962dd821620de729.png)



## **告警去重统计**

![2f39bbf2119340eca6893509c0786d08.png](https://img-blog.csdnimg.cn/2f39bbf2119340eca6893509c0786d08.png)

## 告警人分组邮件

![3884b0ac152a4f1faa0ece0429c7595c.png](https://img-blog.csdnimg.cn/3884b0ac152a4f1faa0ece0429c7595c.png)



**原理图**

![c92b80dd349003cbac81d33d021a1c14.png](https://img-blog.csdnimg.cn/img_convert/c92b80dd349003cbac81d33d021a1c14.png)



此项目主要使用Django开发告警接口，对接Altermanager告警，实现告警人分组，邮件等

告警信息日志，告警信息统计等等

![344863fab8814d1288e7c4e6b8814ab6.png](https://img-blog.csdnimg.cn/344863fab8814d1288e7c4e6b8814ab6.png)

开发过程

model

```
from django.db import models


# Create your models here.
class alerts(models.Model):
    startsAt = models.DateTimeField(verbose_name='告警产生时间')
    endsAt = models.DateTimeField(verbose_name='告警恢复时间')
    instance = models.CharField(max_length=50, verbose_name='实例', blank=True)
    alertname = models.CharField(max_length=100, verbose_name='告警名称')
    status = models.CharField(max_length=20, verbose_name='状态', blank=True)
    severity = models.CharField(max_length=20, verbose_name='告警级别', blank=True)
    message = models.CharField(max_length=1000, verbose_name='告警信息', blank=True)
    known = models.BooleanField(default=False, verbose_name='知悉')
    memo = models.CharField(max_length=50, verbose_name='知悉备注', blank=True)

    def __str__(self):
        return self.message

    class Meta:
        db_table = 'alerts'
        verbose_name = '告警日志'
        verbose_name_plural = verbose_name
        # ordering = ['-startsAt']  # 按故障时间倒排


class production(models.Model):
    startsAt = models.DateTimeField(verbose_name='告警产生时间')
    endsAt = models.DateTimeField(verbose_name='告警恢复时间')
    instance = models.CharField(max_length=50, verbose_name='实例', blank=True)
    alertname = models.CharField(max_length=100, verbose_name='告警名称')
    status = models.CharField(max_length=20, verbose_name='状态', blank=True)
    severity = models.CharField(max_length=20, verbose_name='告警级别', blank=True)
    message = models.CharField(max_length=1000, verbose_name='告警信息', blank=True)
    known = models.BooleanField(default=False, verbose_name='知悉')

    # memo = models.CharField(max_length=50, verbose_name='知悉备注', blank=True)

    def __str__(self):
        return self.message

    class Meta:
        db_table = 'production'
        verbose_name = '告警统计'
        verbose_name_plural = verbose_name


class alarmuser(models.Model):
    username = models.CharField(max_length=20, verbose_name='告警人', blank=True)
    useremail = models.EmailField(max_length=20, verbose_name='告警邮件', blank=True)
    group = models.CharField(max_length=20, verbose_name='分组', blank=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'alarmuser'
        verbose_name = '告警人配置'
        verbose_name_plural = verbose_name

```

注册xadmin后台

```
import xadmin

from django.contrib import admin

from xadmin import views
from webhook.models import alerts, production, alarmuser


class GlobalSetting:
    site_title = "长风破浪"
    site_footer = "长风破浪"
    menu_style = "accordion"  # 这个是设置菜单主题
    enable_themes = True
    use_bootswatch = True
    refresh_times = [5, 10, 30, 60]


xadmin.site.register(views.CommAdminView, GlobalSetting)


class AlertsAdmin(object):
    """xadmin的全局配置"""
    site_title = "长风破浪"  # 设置站点标题
    site_footer = "长风破浪"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠
    '''设置列表可显示的字段'''
    list_display = ('startsAt', 'endsAt', 'instance', 'alertname', 'status', 'severity', 'message', 'known', 'memo',)

    list_filter = ['status', 'severity', 'startsAt', 'endsAt']
    search_fields = ['instance', 'alertname']
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50


class ProductionAdmin(object):
    menu_style = "accordion"  # 设置菜单折叠
    list_display = ('startsAt', 'endsAt', 'instance', 'alertname', 'status', 'severity', 'message', 'known',)

    list_filter = ['status', 'severity', 'startsAt', 'endsAt']
    search_fields = ['instance', 'alertname']
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50


class AlarmuserAdmin(object):
    list_display = ('username', 'useremail', 'group')


xadmin.site.register(alerts, AlertsAdmin)
xadmin.site.register(production, ProductionAdmin)
xadmin.site.register(alarmuser, AlarmuserAdmin)

```

view视图

```
import json
import smtplib
from email.mime.text import MIMEText

import yaml
from dateutil import parser
from django.http import HttpResponse
from webhook.models import alerts as alerts_t, alarmuser
from webhook.models import production
import datetime
from jinja2 import Environment, FileSystemLoader


# 获取html目录
class ParseingTemplate:
    def __init__(self, templatefile):
        self.templatefile = templatefile

    def template(self, **kwargs):
        try:
            env = Environment(loader=FileSystemLoader('templates'))
            template = env.get_template(self.templatefile)
            template_content = template.render(kwargs)
            return template_content
        except Exception as error:
            raise error


# 时区转换（增加八个小时）
def time_zone_conversion(utctime):
    format_time = parser.parse(utctime).strftime('%Y-%m-%dT%H:%M:%SZ')
    time_format = datetime.datetime.strptime(format_time, "%Y-%m-%dT%H:%M:%SZ")
    return str(time_format + datetime.timedelta(hours=8))


# 获取告警人的分组和邮件
def get_email(email_name=None, action=0):
    """
    :param email_name: 发送的邮件列表名
    :param action: 操作类型，0: 查询收件人的邮件地址列表, 1: 查询收件人的列表名称, 2: 获取邮件账号信息
    :return: 根据action的值，返回不通的数据结构
    """
    if action == 0:
        email = alarmuser.objects.filter(group=email_name)
        email_lsit = []
        for i in email:
            email_lsit.append(i.useremail)
        print('显示邮件', email_lsit)
        return email_lsit
    elif action == 1:
        group_list = []
        group = alarmuser.objects.values("group").distinct()
        for i in group:
            group_list.append(i['group'])
        print('显示组:', group_list)


# 获取邮件的地址的配置
def get_email_conf(file, email_name=None, action=0):
    """
    :param file: yaml格式的文件类型
    :param email_name: 发送的邮件列表名
    :param action: 操作类型，0: 查询收件人的邮件地址列表, 1: 查询收件人的列表名称, 2: 获取邮件账号信息
    :return: 根据action的值，返回不通的数据结构
    """
    try:
        with open(file, 'r', encoding='utf-8') as fr:
            read_conf = yaml.safe_load(fr)
            if action == 0:
                for email in read_conf['email']:
                    if email['name'] == email_name:
                        return email['receive_addr']
                    else:
                        print("%s does not match for %s" % (email_name, file))
                else:
                    print("No recipient address configured")
            elif action == 1:
                return [items['name'] for items in read_conf['email']]
            elif action == 2:
                return read_conf['send']
    except KeyError:
        print("%s not exist" % email_name)
        exit(-1)
    except FileNotFoundError:
        print("%s file not found" % file)
        exit(-2)
    except Exception as e:
        raise e


# 发送邮件地址
def sendEmail(title, content, receivers=None):
    if receivers is None:
        receivers = ['chenf-o@glodon.com']
    send_dict = get_email_conf('email.yaml', action=2)
    mail_host = send_dict['smtp_host']
    mail_user = send_dict['send_user']
    mail_pass = send_dict['send_pass']
    sender = send_dict['send_addr']
    print(mail_host, mail_user, mail_pass, sender)
    msg = MIMEText(content, 'html', 'utf-8')
    msg['From'] = "{}".format(sender)
    msg['To'] = ",".join(receivers)
    print(receivers)
    print(msg['To'])
    msg['Subject'] = title
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, msg.as_string())
        print('mail send successful.')
    except smtplib.SMTPException as e:
        print(e)


# 先保存，后发邮件
def webhook(request):
    if request.method == "GET":
        # email = get_email(action=1)
        return HttpResponse('禁止get')
    if request.method == 'POST':
        try:
            request_data = request.body
            print(request_data.decode())
            request_dict = json.loads(request_data.decode('utf-8'))
            alerts = request_dict['alerts']

            prometheus_data = json.loads(request.body)

            for i in alerts:
                msg = i['annotations']['message'] if 'message' in i['annotations'] else 'null'
                if msg == 'null' and 'summary' in i['annotations']:
                    msg = i['annotations']['summary']
                print(i['startsAt'][0:19] + i['status'] + " :" + msg)
                if msg == 'null': print(i)
                ints = i['labels']['instance'] if 'instance' in i['labels'] else 'unknown'

                print(ints + " --- " + i['labels']['alertname'] + " ---- " + i['labels']['severity'])
                print(i['endsAt'])
                a = alerts_t()
                a.startsAt = time_zone_conversion(i['startsAt'])
                str = '0001-01-01'
                print(str in i['endsAt'])
                if (str in i['endsAt']):
                    a.endsAt = '0001-01-01 00:00:00'
                else:
                    a.endsAt = time_zone_conversion(i['endsAt'])
                print(a.endsAt)
                a.instance = ints
                a.alertname = i['labels']['alertname']
                if i['status'] == 'firing':
                    a.status = '告警中'
                if i['status'] == 'resolved':
                    a.status = '已恢复'
                    a.known = True
                a.severity = i['labels']['severity']
                a.message = msg
                a.save()

                startime = time_zone_conversion(i['startsAt'])
                endtime = a.endsAt
                instances = ints
                AlarmObject = production.objects.filter(startsAt=startime, endsAt=endtime, instance=instances)
                print(AlarmObject)
                if AlarmObject.exists():
                    pass
                else:
                    b = production()
                    b.startsAt = time_zone_conversion(i['startsAt'])
                    # print(str in i['endsAt'])
                    if (str in i['endsAt']):
                        b.endsAt = '0001-01-01 00:00:00'
                    else:
                        b.endsAt = time_zone_conversion(i['endsAt'])
                    # print(b.endsAt)
                    b.instance = ints
                    b.alertname = i['labels']['alertname']
                    if i['status'] == 'firing':
                        b.status = '告警中'
                    if i['status'] == 'resolved':
                        b.status = '已恢复'
                        b.known = True
                    b.severity = i['labels']['severity']
                    b.message = msg
                    b.save()
                print('显示a:', a)
                # 时间转换，转换成东八区时间
            for k, v in prometheus_data.items():
                if k == 'alerts':
                    for items in v:
                        if items['status'] == 'firing':
                            items['startsAt'] = time_zone_conversion(items['startsAt'])
                        else:
                            items['startsAt'] = time_zone_conversion(items['startsAt'])
                            items['endsAt'] = time_zone_conversion(items['endsAt'])
            print(prometheus_data)
            team_name = prometheus_data["commonLabels"]["team"]
            print(team_name)
            generate_html_template_subj = ParseingTemplate('email_template_firing.html')
            html_template_content = generate_html_template_subj.template(
                prometheus_monitor_info=prometheus_data
            )
            # 获取收件人邮件列表
            email_list = get_email(email_name=team_name, action=0)
            print(email_list)
            print(prometheus_data['commonLabels']['alertname'])
            sendEmail(
                prometheus_data['commonLabels']['alertname'],
                html_template_content,
                receivers=email_list
            )
            # return "prometheus monitor"
            return HttpResponse(1)
        except Exception as e:
            print(e)
            raise e
        # finally:
        #     return HttpResponse(1)

```

需要完整代码，请留言

稍后整理完毕传到github上

[GitHub - nangongchengfeng/Alerts](https://github.com/nangongchengfeng/Alerts.git)

屎一样的代码，请大佬忽略。后期会使用falsk 更新
