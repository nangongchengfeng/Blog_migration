# -*- coding: utf-8 -*-
# @Time    : 2023/1/9 18:18
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : ui.py
# @Software: PyCharm
import requests
from lxml import etree

from bs4 import BeautifulSoup
"""
new_url = 'https://pic.netbian.com/e/search/result/index.php?page=0&searchid=1164'
headers = {
    'Users-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}

res = requests.get(new_url, headers=headers).text
soup = BeautifulSoup(res, "html.parser")
res.encode('UTF-8').decode('UTF-8')
div_class = soup.find(name='ul', attrs={"class": "clearfix"})
a_name = div_class.find_all(name='a')
image_url=[]

for i in a_name:
    # print(i)

    image_url.append('http://pic.netbian.com' +i['href'])
print(image_url)"""

new_url = 'http://pic.netbian.com/tupian/30351.html'
headers = {
    'Users-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}
res = requests.get(new_url, headers=headers).text
soup = BeautifulSoup(res, "html.parser")
res.encode('UTF-8').decode('UTF-8')
div_class = soup.find(name='div', attrs={"class": "photo-pic"})
a_name = div_class.find_all(name='img')
print(a_name)
for i in a_name:
    print("https://pic.netbian.com/"+i['src'])
