# -*- coding: utf-8 -*-
# @Time    : 2023/5/10 14:35
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : csdn_spider.py.py
# @Software: PyCharm
import requests
import re
from bs4 import BeautifulSoup
import time
import random
import pandas as pd
from sqlalchemy import create_engine
import datetime as dt

headers = {
    'User-Agent': 'Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; Trident/5.0)',
    'referer': 'https: // passport.csdn.net / login',
}


def get_info():
    """获取大屏第一列信息数据"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; Trident/5.0)',
        'referer': 'https: // passport.csdn.net / login',
    }
    # 我的博客地址
    url = 'https://blog.csdn.net/heian_99/article/details/105689982'
    try:
        resp = requests.get(url, headers=headers)
        now = dt.datetime.now().strftime("%Y-%m-%d %X")
        # print(resp.text)
        soup = BeautifulSoup(resp.text, 'lxml')
        author_name = soup.find('div', class_='user-info d-flex flex-column profile-intro-name-box').find('a').get_text(
            strip=True)
        head_img = \
            soup.find('div', class_='avatar-box d-flex justify-content-center flex-column').find('a').find('img')['src']
        row1_nums = soup.find_all('div', class_='data-info d-flex item-tiling')[0].find_all('span', class_='count')
        row2_nums = soup.find_all('div', class_='data-info d-flex item-tiling')[1].find_all('span', class_='count')
        level_mes = \
            soup.find_all('div', class_='data-info d-flex item-tiling')[0].find_all('dl')[-1]['title'].split(',')[0]
        rank = soup.find('div', class_='data-info d-flex item-tiling').find_all('dl')[-1]['title']
        # 6级,点击查看等级说明

        info = {
            'date': now,  # 时间
            'head_img': head_img,  # 头像
            'author_name': author_name,  # 用户名
            'article_num': str(row1_nums[0].get_text()),  # 文章数
            'fans_num': str(row2_nums[1].get_text()),  # 粉丝数
            'like_num': str(row2_nums[2].get_text()),  # 喜欢数
            'comment_num': str(row2_nums[3].get_text()),  # 评论数
            'level': level_mes,  # 等级
            'visit_num': str(row1_nums[3].get_text()),  # 访问数
            'score': str(row2_nums[0].get_text()),  # 积分
            'rank': str(row1_nums[2].get_text()),  # 排名
        }
        df_info = pd.DataFrame([info.values()], columns=info.keys())
        # print(info)
        return df_info
    except Exception as e:
        print(e)
        # return get_info()


def get_type(title):
    """设置文章类型(依据文章名称)"""
    the_type = '其他'
    article_types = ['Jenkins', 'Go语言', 'Ansible', 'Kubernetes', 'Prometheus监控', 'MySQL', 'Zabbix监控', 'Nginx',
                     'Python学习', '项目实战', 'Linux Shell', 'Linux系统入门', '错误问题解决', 'Java', '软件']
    for article_type in article_types:
        if article_type in title:
            the_type = article_type
            break
    return the_type


def get_blog():
    """获取大屏第二、三列信息数据"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; Trident/5.0)',
        'referer': 'https: // passport.csdn.net / login',
    }
    base_url = 'https://blog.csdn.net/heian_99/article/list/'
    resp = requests.get(base_url + "1", headers=headers, timeout=3)

    max_page = int(re.findall(r'var listTotal = (\d+);', resp.text)[0]) // 40 + 1

    df = pd.DataFrame(columns=['url', 'title', 'date', 'read_num', 'comment_num', 'type'])
    count = 0

    for i in range(1, max_page + 1):
        url = base_url + str(i)
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.text, 'lxml')
        articles = soup.find("div", class_='article-list').find_all('div',
                                                                    class_='article-item-box csdn-tracking-statistics')

        for article in articles[1:]:
            a_url = article.find('h4').find('a')['href']
            title = article.find('h4').find('a').get_text(strip=True)[2:]
            issuing_time = article.find('span', class_="date").get_text(strip=True)
            num_list = article.find_all('span', class_="read-num")
            read_num = num_list[0].get_text(strip=True)

            if len(num_list) > 1:
                comment_num = num_list[1].get_text(strip=True)
            else:
                comment_num = 0
            # print(a_url, title, issuing_time, read_num,comment_num,num_list)
            # exit(1)
            the_type = get_type(title)
            df.loc[count] = [a_url, title, issuing_time, int(read_num), int(comment_num), the_type]
            count += 1
        time.sleep(random.choice([1, 1.1, 1.3]))
    print(df)
    return df


def get_categorize():
    id = "heian_99"
    # 拼接博客首页链接
    urls = 'https://blog.csdn.net/' + id
    # 发送get请求获取响应
    reply = requests.get(url=urls, headers=headers)
    # 使用BeautifulSoup解析响应
    parse = BeautifulSoup(reply.content, "lxml")
    # 查找包含“special-column-name”类名的所有<a>标签
    spans = parse.find_all('a', attrs={'class': 'special-column-name'})
    #           [href, blog_column, blog_id, blogs_column_num, subscribe_num_span, article_num_span, read_num_span,
    #              collect_num_span]
    df = pd.DataFrame(columns=['href', 'categorize', 'categorize_id', 'column_num', 'num_span', 'article_num','read_num', 'collect_num'])
    count = 0

    blog_columns = []
    # 遍历所有<span>标签
    for span in spans:
        # 从<span>标签中提取链接
        href = re.findall(r'href=\"(.*?)\".*?', str(span), re.S)
        href = ''.join(href)
        # 再次发送get请求获取响应
        blog_column_reply = requests.get(url=href, headers=headers)
        # 解析 HTML，获取关注数、文章数、文章阅读量和文章收藏量
        soup = BeautifulSoup(blog_column_reply.text, 'html.parser')
        column_operating_div = soup.find('div', {'class': 'column_operating'})
        subscribe_num_span = column_operating_div.find('span', {'class': 'column-subscribe-num'}).text
        article_num_span = column_operating_div.find_all('span', {'class': 'mumber-color'})[1].text
        read_num_span = column_operating_div.find_all('span', {'class': 'mumber-color'})[2].text
        collect_num_span = column_operating_div.find_all('span', {'class': 'mumber-color'})[3].text

        # 从响应中提取专栏博客数量
        blogs_num = re.findall(
            r'<a class="clearfix special-column-name" target="_blank" href=\"' + href + '\".*?<span class="special-column-num">(.+?)篇</span>',
            blog_column_reply.text, re.S)
        blogs_column_num = str(blogs_num[0])

        # 获取专栏名
        blog_column = span.text.strip()

        # 从链接中提取博客id
        blog_id = href.split("_")[-1]
        blog_id = blog_id.split(".")[0]
        blog_columns.append(
            [href, blog_column, blog_id, blogs_column_num, subscribe_num_span, article_num_span, read_num_span,
             collect_num_span])
        df.loc[count] = [href, blog_column, int(blog_id), int(blogs_column_num), int(subscribe_num_span), int(article_num_span),int(read_num_span),
             int(collect_num_span)]
        count += 1
    time.sleep(random.choice([1, 1.1, 1.3]))
    print(df)
    return df

def run():
    # 今天的时间
    today = dt.datetime.today().strftime("%Y-%m-%d")
    # 连接mysql数据库
    engine = create_engine('mysql+pymysql://root:123456@192.168.102.20/csdn?charset=utf8')

    # 获取大屏第一列信息数据, 并写入my_database数据库的info表中, 如若表已存在, 删除覆盖
    df_info = get_info()
    df_info.to_sql("info", con=engine, if_exists='replace', index=False)

    # 获取大屏第二、三列信息数据, 并写入my_database数据库的日期表中, 如若表已存在, 删除覆盖
    df_article = get_blog()
    df_article.to_sql(today, con=engine, if_exists='replace', index=True)
    #获取分类
    df_categorize = get_categorize()
    df_categorize.to_sql("categorize", con=engine, if_exists='replace', index=True)


if __name__ == '__main__':
    # run()
    # print(get_info())
    # 今天的时间
    today = dt.datetime.today().strftime("%Y-%m-%d")
    # 连接mysql数据库
    engine = create_engine('mysql+pymysql://root:123456@192.168.102.20/csdn?charset=utf8')

    # # 获取大屏第一列信息数据, 并写入my_database数据库的info表中, 如若表已存在, 删除覆盖
    # df_info = get_info()
    # print("获取数据：", df_info)
    # print("-----------------")
    # df_info.to_sql("info", con=engine, if_exists='replace', index=False)
    # 获取大屏第二、三列信息数据, 并写入my_database数据库的日期表中, 如若表已存在, 删除覆盖

