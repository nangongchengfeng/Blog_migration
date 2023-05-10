import requests
import re
from bs4 import BeautifulSoup
import time
import random
import pandas as pd
from sqlalchemy import create_engine
import datetime as dt
from blogs import blog_list


def get_info():
    headers = {
        'User-Agent': 'Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; Trident/5.0)',
        'referer': 'https: // passport.csdn.net / login',
    }
    url = 'https://blog.csdn.net/tonydz0523/article/details/85779090'
    # url = random.choice(blog_list)
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
        print(df_info)
        return df_info
    except Exception as e:
        print(e)
        # return get_info()
        exit(0)

def get_type(title):
    the_type = '其他'
    article_types = ['项目', 'pytorch', 'flask', 'scikit-learn', 'pyspark', '数据预处理', '每日一练', '数据分析', '爬虫', '数据可视化', 'java', '增长黑客']
    for article_type in article_types:
        if article_type in title:
            the_type = article_type
            break

    return the_type

def get_blog():
    headers = {
        'User-Agent': 'Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; Trident/5.0)',
        'referer': 'https: // passport.csdn.net / login',
    }
    base_url = 'https://blog.csdn.net/tonydz0523/article/list/'
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
            the_type = get_type(title)
            df.loc[count] = [a_url, title, issuing_time, int(read_num), int(comment_num), the_type]
            count += 1
        time.sleep(random.choice([1, 1.1, 1.3]))
    return df

if __name__ == '__main__':
    today = dt.datetime.today().strftime("%Y-%m-%d")  # 过去今天时间
    engine = create_engine('sqlite:///blog.sqlite')
    df_info = get_info()
    df_info.to_sql("info", con=engine, if_exists='replace', index=False)
    print(pd.read_sql("info", con=engine))
    df_article = get_blog()
    df_article.to_sql(today, con=engine, if_exists='replace', index=True)