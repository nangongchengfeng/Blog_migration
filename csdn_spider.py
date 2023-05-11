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


def append_blog_info(blog_column_url, blog_column_name, blogs):
    # 发送get请求，获取响应
    reply = requests.get(url=blog_column_url, headers=headers)
    # 使用BeautifulSoup解析响应
    blog_span = BeautifulSoup(reply.content, "lxml")
    # 获取所有的class="column_article_list"的<ul>标签
    blogs_list = blog_span.find_all('ul', attrs={'class': 'column_article_list'})
    # 遍历所有的<ul>标签
    for arch_blog_info in blogs_list:
        # 获取<ul>标签内所有的<li>标签
        blogs_list = arch_blog_info.find_all('li')
        # 遍历所有的<li>标签
        for blog_info in blogs_list:
            # 获取<li>标签内的文章链接和标题
            blog_url = blog_info.find('a', attrs={'target': '_blank'})['href']
            blog_title = blog_info.find('h2', attrs={'class': "title"}).get_text().strip().replace(" ", "_").replace(
                '/', '_')
            statuses = blog_info.find_all("span", class_="status")
            three_status = []
            for index, status in enumerate(statuses):
                if index == 0:
                    time_str = status.text.split('·')[0]
                    time_str = time_str.strip()
                    three_status.append(time_str)
                else:
                    time_str = status.text.split('·')[0]
                    num = int(re.findall(r'\d+', time_str)[0])
                    three_status.append(num)

            # 将文章信息存储在字典中
            blog_dict = {'url': blog_url, 'title': blog_title, 'date': three_status[0], 'read_num': three_status[1],
                         'comment_num': three_status[2], 'type': blog_column_name}
            # 将字典追加到文章列表中
            blogs.append(blog_dict)
    # 返回所有文章的信息
    return blogs


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
    # 获取所有专栏博客信息的嵌套列表
    # blog_columns = request_blog_column(id)
    blog_columns = [['https://blog.csdn.net/heian_99/category_11822490.html', 'Jenkins', '11822490', '7'],
                    ['https://blog.csdn.net/heian_99/category_11509281.html', 'Go语言', '11509281', '8'],
                    ['https://blog.csdn.net/heian_99/category_11034339.html', 'Ansible', '11034339', '3'],
                    ['https://blog.csdn.net/heian_99/category_9652886.html', 'Kubernetes', '9652886', '53'],
                    ['https://blog.csdn.net/heian_99/category_10946715.html', 'Kubernetes项目实战', '10946715', '10'],
                    ['https://blog.csdn.net/heian_99/category_10930558.html', 'Kubernetes应用', '10930558', '17'],
                    ['https://blog.csdn.net/heian_99/category_10930341.html', 'Traefik', '10930341', '2'],
                    ['https://blog.csdn.net/heian_99/category_9577365.html', 'Docker', '9577365', '29'],
                    ['https://blog.csdn.net/heian_99/category_9662810.html', 'Prometheus监控', '9662810', '18'],
                    ['https://blog.csdn.net/heian_99/category_8862710.html', 'MySQL', '8862710', '37'],
                    ['https://blog.csdn.net/heian_99/category_9989746.html', 'Zabbix监控', '9989746', '9'],
                    ['https://blog.csdn.net/heian_99/category_9545224.html', 'Nginx', '9545224', '7'],
                    ['https://blog.csdn.net/heian_99/category_8942291.html', 'Python学习', '8942291', '25'],
                    ['https://blog.csdn.net/heian_99/category_10705987.html', '项目实战', '10705987', '9'],
                    ['https://blog.csdn.net/heian_99/category_8750410.html', 'Linux Shell', '8750410', '26'],
                    ['https://blog.csdn.net/heian_99/category_9675115.html', '企业级-Shell脚本案例', '9675115', '30'],
                    ['https://blog.csdn.net/heian_99/category_9288323.html', 'Linux系统入门', '9288323', '1'],
                    ['https://blog.csdn.net/heian_99/category_10149025.html', 'Linux实战操作', '10149025', '20'],
                    ['https://blog.csdn.net/heian_99/category_10148973.html', 'Linux服务应用', '10148973', '16'],
                    ['https://blog.csdn.net/heian_99/category_10148926.html', 'Linux基础', '10148926', '23'],
                    ['https://blog.csdn.net/heian_99/category_9356447.html', 'Java', '9356447', '17'],
                    ['https://blog.csdn.net/heian_99/category_9520385.html', '错误问题解决', '9520385', '14'],
                    ['https://blog.csdn.net/heian_99/category_8961205.html', '软件', '8961205', '5']]

    df = pd.DataFrame(columns=['url', 'title', 'date', 'read_num', 'comment_num', 'type'])
    count = 0

    blogs = []
    # 遍历专栏博客信息的嵌套列表
    for blog_column in blog_columns:
        blog_column_url = blog_column[0]
        blog_column_name = blog_column[1]
        blog_column_id = blog_column[2]
        blog_column_num = int(blog_column[3])
        # 如果专栏博客数量大于40，一页的篇数为40，需要翻页
        if blog_column_num > 40:
            # 计算翻页数量
            page_num = round(blog_column_num / 40)
            # 倒序循环翻页链接
            for i in range(page_num, 0, -1):
                # 拼接翻页链接
                blog_column_url = blog_column[0]
                url_str = blog_column_url.split('.html')[0]
                blog_column_url = url_str + '_' + str(i) + '.html'
                # 将文章信息追加到文章列表中
                append_blog_info(blog_column_url, blog_column_name, blogs)
            # 获取第一页的文章列表信息
            blog_column_url = blog_column[0]
            blogs = append_blog_info(blog_column_url, blog_column_name, blogs)
        # 如果专栏博客数量小于等于40
        else:
            # 获取专栏第一页的文章列表信息
            blogs = append_blog_info(blog_column_url, blog_column_name, blogs)
    # 返回所有文章的信息
    """
                df.loc[count] = [a_url, title, issuing_time, int(read_num), int(comment_num), the_type]
            count += 1
    """
    for blog in blogs:
        print(blog)
        df.loc[count] = [blog['url'], blog['title'], blog['date'], blog['read_num'], blog['comment_num'], blog['type']]
        count += 1
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
    df = pd.DataFrame(
        columns=['href', 'categorize', 'categorize_id', 'column_num', 'num_span', 'article_num', 'read_num',
                 'collect_num'])
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
        df.loc[count] = [href, blog_column, int(blog_id), int(blogs_column_num), int(subscribe_num_span),
                         int(article_num_span), int(read_num_span),
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
    # 获取分类
    df_categorize = get_categorize()
    df_categorize.to_sql("categorize", con=engine, if_exists='replace', index=True)


if __name__ == '__main__':
    run()
