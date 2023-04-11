# @Software: PyCharm
# -*- coding: utf-8 -*-
# @Time    : 2023/1/7 14:49
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : blog.py
# @Software: PyCharm
import os
import random
import re
from datetime import datetime, timedelta

import chardet
import parsel
import requests
import tomd2

# 正则中的%s分割
splits = [
    {1: [('年', '月', '日', '点', '分', '秒'), ('-', '-', '', ':', ':', ''), ('\/', '\/', '', ':', ':', ''),
         ('\.', '\.', '', ':', ':', '')]},
    {2: [('年', '月', '日', '点', '分'), ('-', '-', '', ':', ''), ('\/', '\/', '', ':', ''),
         ('\.', '\.', '', ':', '')]},
    {3: [('年', '月', '日'), ('-', '-', ''), ('\/', '\/', ''), ('\.', '\.', '')]},
    {4: [('年', '月', '日'), ('-', '-', ''), ('\/', '\/', ''), ('\.', '\.', '')]},

    {5: [('月', '日', '点', '分', '秒'), ('-', '', ':', ':', ''), ('\/', '', ':', ':', ''), ('\.', '', ':', ':', '')]},
    {6: [('月', '日', '点', '分'), ('-', '', ':', ''), ('\/', '', ':', ''), ('\.', '', ':', '')]},
    {7: [('月', '日'), ('-', ''), ('\/', ''), ('\.', '')]},

    {8: [('点', '分', '秒'), (':', ':', '')]},
    {9: [('点', '分'), (':', '')]},
]

# 匹配正则表达式
matchs = {
    1: (r'\d{4}%s\d{1,2}%s\d{1,2}%s \d{1,2}%s\d{1,2}%s\d{1,2}%s', '%%Y%s%%m%s%%d%s %%H%s%%M%s%%S%s'),
    2: (r'\d{4}%s\d{1,2}%s\d{1,2}%s \d{1,2}%s\d{1,2}%s', '%%Y%s%%m%s%%d%s %%H%s%%M%s'),
    3: (r'\d{4}%s\d{1,2}%s\d{1,2}%s', '%%Y%s%%m%s%%d%s'),
    4: (r'\d{2}%s\d{1,2}%s\d{1,2}%s', '%%y%s%%m%s%%d%s'),

    # 没有年份
    5: (r'\d{1,2}%s\d{1,2}%s \d{1,2}%s\d{1,2}%s\d{1,2}%s', '%%m%s%%d%s %%H%s%%M%s%%S%s'),
    6: (r'\d{1,2}%s\d{1,2}%s \d{1,2}%s\d{1,2}%s', '%%m%s%%d%s %%H%s%%M%s'),
    7: (r'\d{1,2}%s\d{1,2}%s', '%%m%s%%d%s'),

    # 没有年月日
    8: (r'\d{1,2}%s\d{1,2}%s\d{1,2}%s', '%%H%s%%M%s%%S%s'),
    9: (r'\d{1,2}%s\d{1,2}%s', '%%H%s%%M%s'),
}

parten_other = '\d+天前|\d+分钟前|\d+小时前|\d+秒前'


class TimeFinder(object):

    def __init__(self, base_date=None):
        self.base_date = base_date
        self.match_item = []

        self.init_args()
        self.init_match_item()

    def init_args(self):
        # 格式化基础时间
        if not self.base_date:
            self.base_date = datetime.now()
        if self.base_date and not isinstance(self.base_date, datetime):
            try:
                self.base_date = datetime.strptime(self.base_date, '%Y-%m-%d %H:%M:%S')
            except Exception as e:
                raise Exception('type of base_date must be str of%Y-%m-%d %H:%M:%S or datetime')

    def init_match_item(self):
        # 构建穷举正则匹配公式 及提取的字符串转datetime格式映射
        for item in splits:
            for num, value in item.items():
                match = matchs[num]
                for sp in value:
                    tmp = []
                    for m in match:
                        tmp.append(m % sp)
                    self.match_item.append(tuple(tmp))

    def get_time_other(self, text):
        m = re.search('\d+', text)
        if not m:
            return None
        num = int(m.group())
        if '天' in text:
            return self.base_date - timedelta(days=num)
        elif '小时' in text:
            return self.base_date - timedelta(hours=num)
        elif '分钟' in text:
            return self.base_date - timedelta(minutes=num)
        elif '秒' in text:
            return self.base_date - timedelta(seconds=num)

        return None

    def find_time(self, text):
        # 格式化text为str类型
        if isinstance(text, bytes):
            encoding = chardet.detect(text)['encoding']
            text = text.decode(encoding)

        res = []
        parten = '|'.join([x[0] for x in self.match_item])

        parten = parten + '|' + parten_other
        match_list = re.findall(parten, text)
        if not match_list:
            return None
        for match in match_list:
            for item in self.match_item:
                try:
                    date = datetime.strptime(match, item[1].replace('\\', ''))
                    if date.year == 1900:
                        date = date.replace(year=self.base_date.year)
                        if date.month == 1:
                            date = date.replace(month=self.base_date.month)
                            if date.day == 1:
                                date = date.replace(day=self.base_date.day)
                    res.append(datetime.strftime(date, '%Y-%m-%d %H:%M:%S'))
                    break
                except Exception as e:
                    date = self.get_time_other(match)
                    if date:
                        res.append(datetime.strftime(date, '%Y-%m-%d %H:%M:%S'))
                        break
        if not res:
            return None
        return res


# 判断目录是否存在，不存在则创建
def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def handleDate(time_str):
    result = None
    # 定义日期格式
    timefinder = TimeFinder(base_date='2020-01-01 00:00:00')
    parsed_time = timefinder.find_time(time_str.replace("\t", "").replace("\n", ""))
    if parsed_time is None:
        if time_str.find("年") >= 0:
            parsed_time = timefinder.find_time(time_str.replace(" ", "").replace("\t", ""))
            if parsed_time is not None:
                result = parsed_time[0]
    else:
        result = parsed_time[0]
    return result


# 返回图片地址
def get_images_url():
    list_image = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
                  '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34',
                  '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51',
                  '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68',
                  '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85',
                  '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99']
    x = random.choice(list_image)
    image_url = f"post/4kdongman/{x}.jpg"
    return image_url


def get_article_info(url):
    html = requests.get(url, headers=headers).text
    # print(html)
    selector = parsel.Selector(html)
    ##articleMeList-blog > div.article-list > div > h4 > a
    urls = selector.css('.mainContent').xpath('.//@href').getall()
    # print(urls)
    urls = ['https://blog.csdn.net/heian_99/article/details/106939828',
            'https://blog.csdn.net/heian_99/article/details/105689982',
            'https://blog.csdn.net/heian_99/article/details/128495053',
            'https://blog.csdn.net/heian_99/article/details/128476559',
            'https://blog.csdn.net/heian_99/article/details/128476370',
            'https://blog.csdn.net/heian_99/article/details/128369623',
            'https://blog.csdn.net/heian_99/article/details/128129761',
            'https://blog.csdn.net/heian_99/article/details/127828348',
            'https://blog.csdn.net/heian_99/article/details/127610131',
            'https://blog.csdn.net/heian_99/article/details/126989356',
            'https://blog.csdn.net/heian_99/article/details/126972415',
            'https://blog.csdn.net/heian_99/article/details/126884386',
            'https://blog.csdn.net/heian_99/article/details/125979933',
            'https://blog.csdn.net/heian_99/article/details/125618555',
            'https://blog.csdn.net/heian_99/article/details/125594954',
            'https://blog.csdn.net/heian_99/article/details/124986269',
            'https://blog.csdn.net/heian_99/article/details/124985786',
            'https://blog.csdn.net/heian_99/article/details/124816190',
            'https://blog.csdn.net/heian_99/article/details/124815450',
            'https://blog.csdn.net/heian_99/article/details/124814780',
            'https://blog.csdn.net/heian_99/article/details/124809338',
            'https://blog.csdn.net/heian_99/article/details/124808858',
            'https://blog.csdn.net/heian_99/article/details/124748299',
            'https://blog.csdn.net/heian_99/article/details/124613972',
            'https://blog.csdn.net/heian_99/article/details/123938428',
            'https://blog.csdn.net/heian_99/article/details/123584909',
            'https://blog.csdn.net/heian_99/article/details/123522929',
            'https://blog.csdn.net/heian_99/article/details/123447452',
            'https://blog.csdn.net/heian_99/article/details/123405383',
            'https://blog.csdn.net/heian_99/article/details/123398209',
            'https://blog.csdn.net/heian_99/article/details/123380912',
            'https://blog.csdn.net/heian_99/article/details/122842521',
            'https://blog.csdn.net/heian_99/article/details/122447855',
            'https://blog.csdn.net/heian_99/article/details/122239214',
            'https://blog.csdn.net/heian_99/article/details/122216521',
            'https://blog.csdn.net/heian_99/article/details/122142609',
            'https://blog.csdn.net/heian_99/article/details/122108856',
            'https://blog.csdn.net/heian_99/article/details/122002534',
            'https://blog.csdn.net/heian_99/article/details/121912558',
            'https://blog.csdn.net/heian_99/article/details/121851358',
            'https://blog.csdn.net/heian_99/article/details/121680945',
            'https://blog.csdn.net/heian_99/article/details/121628241',
            'https://blog.csdn.net/heian_99/article/details/121472415',
            'https://blog.csdn.net/heian_99/article/details/121432620',
            'https://blog.csdn.net/heian_99/article/details/121125188',
            'https://blog.csdn.net/heian_99/article/details/121077163',
            'https://blog.csdn.net/heian_99/article/details/121050983',
            'https://blog.csdn.net/heian_99/article/details/120769584',
            'https://blog.csdn.net/heian_99/article/details/120728780',
            'https://blog.csdn.net/heian_99/article/details/120416564',
            'https://blog.csdn.net/heian_99/article/details/120322803',
            'https://blog.csdn.net/heian_99/article/details/120304109',
            'https://blog.csdn.net/heian_99/article/details/120249465',
            'https://blog.csdn.net/heian_99/article/details/120249334',
            'https://blog.csdn.net/heian_99/article/details/119875829',
            'https://blog.csdn.net/heian_99/article/details/119874180',
            'https://blog.csdn.net/heian_99/article/details/119825171',
            'https://blog.csdn.net/heian_99/article/details/119579945',
            'https://blog.csdn.net/heian_99/article/details/119359459',
            'https://blog.csdn.net/heian_99/article/details/119305545',
            'https://blog.csdn.net/heian_99/article/details/119296719',
            'https://blog.csdn.net/heian_99/article/details/119112807',
            'https://blog.csdn.net/heian_99/article/details/119089888',
            'https://blog.csdn.net/heian_99/article/details/118965863',
            'https://blog.csdn.net/heian_99/article/details/118914376',
            'https://blog.csdn.net/heian_99/article/details/118579426',
            'https://blog.csdn.net/heian_99/article/details/117855814',
            'https://blog.csdn.net/heian_99/article/details/117753840',
            'https://blog.csdn.net/heian_99/article/details/117151435',
            'https://blog.csdn.net/heian_99/article/details/116401940',
            'https://blog.csdn.net/heian_99/article/details/116329525',
            'https://blog.csdn.net/heian_99/article/details/115499159',
            'https://blog.csdn.net/heian_99/article/details/115488011',
            'https://blog.csdn.net/heian_99/article/details/115486589',
            'https://blog.csdn.net/heian_99/article/details/115477746',
            'https://blog.csdn.net/heian_99/article/details/115468779',
            'https://blog.csdn.net/heian_99/article/details/115433372',
            'https://blog.csdn.net/heian_99/article/details/115422781',
            'https://blog.csdn.net/heian_99/article/details/115422455',
            'https://blog.csdn.net/heian_99/article/details/115405034',
            'https://blog.csdn.net/heian_99/article/details/115308283',
            'https://blog.csdn.net/heian_99/article/details/115304849',
            'https://blog.csdn.net/heian_99/article/details/115137827',
            'https://blog.csdn.net/heian_99/article/details/115017473',
            'https://blog.csdn.net/heian_99/article/details/114991111',
            'https://blog.csdn.net/heian_99/article/details/114984598',
            'https://blog.csdn.net/heian_99/article/details/114971123',
            'https://blog.csdn.net/heian_99/article/details/114963427',
            'https://blog.csdn.net/heian_99/article/details/114953970',
            'https://blog.csdn.net/heian_99/article/details/114950602',
            'https://blog.csdn.net/heian_99/article/details/114901750',
            'https://blog.csdn.net/heian_99/article/details/114840056',
            'https://blog.csdn.net/heian_99/article/details/114763052',
            'https://blog.csdn.net/heian_99/article/details/114647051',
            'https://blog.csdn.net/heian_99/article/details/114601309',
            'https://blog.csdn.net/heian_99/article/details/114556056',
            'https://blog.csdn.net/heian_99/article/details/114525084',
            'https://blog.csdn.net/heian_99/article/details/114490830',
            'https://blog.csdn.net/heian_99/article/details/114481938',
            'https://blog.csdn.net/heian_99/article/details/114477612',
            'https://blog.csdn.net/heian_99/article/details/114461218',
            'https://blog.csdn.net/heian_99/article/details/114440031',
            'https://blog.csdn.net/heian_99/article/details/114185044',
            'https://blog.csdn.net/heian_99/article/details/114080095',
            'https://blog.csdn.net/heian_99/article/details/114079900',
            'https://blog.csdn.net/heian_99/article/details/113407684',
            'https://blog.csdn.net/heian_99/article/details/112977386',
            'https://blog.csdn.net/heian_99/article/details/112792036',
            'https://blog.csdn.net/heian_99/article/details/112766784',
            'https://blog.csdn.net/heian_99/article/details/112759177',
            'https://blog.csdn.net/heian_99/article/details/103904945',
            'https://blog.csdn.net/heian_99/article/details/110404785',
            'https://blog.csdn.net/heian_99/article/details/110240655',
            'https://blog.csdn.net/heian_99/article/details/109712182',
            'https://blog.csdn.net/heian_99/article/details/109390532',
            'https://blog.csdn.net/heian_99/article/details/108686154',
            'https://blog.csdn.net/heian_99/article/details/107622712',
            'https://blog.csdn.net/heian_99/article/details/107582393',
            'https://blog.csdn.net/heian_99/article/details/107293684',
            'https://blog.csdn.net/heian_99/article/details/106647572',
            'https://blog.csdn.net/heian_99/article/details/106644755',
            'https://blog.csdn.net/heian_99/article/details/106409378',
            'https://blog.csdn.net/heian_99/article/details/106386701',
            'https://blog.csdn.net/heian_99/article/details/106219924',
            'https://blog.csdn.net/heian_99/article/details/106101006',
            'https://blog.csdn.net/heian_99/article/details/106023595',
            'https://blog.csdn.net/heian_99/article/details/105844538',
            'https://blog.csdn.net/heian_99/article/details/105631692',
            'https://blog.csdn.net/heian_99/article/details/105601448',
            'https://blog.csdn.net/heian_99/article/details/105513825',
            'https://blog.csdn.net/heian_99/article/details/105428325',
            'https://blog.csdn.net/heian_99/article/details/105223832',
            'https://blog.csdn.net/heian_99/article/details/105197561',
            'https://blog.csdn.net/heian_99/article/details/105165477',
            'https://blog.csdn.net/heian_99/article/details/105123382',
            'https://blog.csdn.net/heian_99/article/details/105099552',
            'https://blog.csdn.net/heian_99/article/details/105044761',
            'https://blog.csdn.net/heian_99/article/details/104993333',
            'https://blog.csdn.net/heian_99/article/details/104944575',
            'https://blog.csdn.net/heian_99/article/details/104914945',
            'https://blog.csdn.net/heian_99/article/details/104904238',
            'https://blog.csdn.net/heian_99/article/details/104893746',
            'https://blog.csdn.net/heian_99/article/details/104892517',
            'https://blog.csdn.net/heian_99/article/details/104868409',
            'https://blog.csdn.net/heian_99/article/details/104420466',
            'https://blog.csdn.net/heian_99/article/details/104263089',
            'https://blog.csdn.net/heian_99/article/details/104262901',
            'https://blog.csdn.net/heian_99/article/details/104239982',
            'https://blog.csdn.net/heian_99/article/details/104227668',
            'https://blog.csdn.net/heian_99/article/details/104226982',
            'https://blog.csdn.net/heian_99/article/details/104223555',
            'https://blog.csdn.net/heian_99/article/details/104201990',
            'https://blog.csdn.net/heian_99/article/details/104198929',
            'https://blog.csdn.net/heian_99/article/details/104198552',
            'https://blog.csdn.net/heian_99/article/details/104188299',
            'https://blog.csdn.net/heian_99/article/details/104181104',
            'https://blog.csdn.net/heian_99/article/details/104174390',
            'https://blog.csdn.net/heian_99/article/details/104167639',
            'https://blog.csdn.net/heian_99/article/details/104162175',
            'https://blog.csdn.net/heian_99/article/details/104161525',
            'https://blog.csdn.net/heian_99/article/details/104154643',
            'https://blog.csdn.net/heian_99/article/details/104154043',
            'https://blog.csdn.net/heian_99/article/details/104069075',
            'https://blog.csdn.net/heian_99/article/details/104063746',
            'https://blog.csdn.net/heian_99/article/details/104063402',
            'https://blog.csdn.net/heian_99/article/details/104062967',
            'https://blog.csdn.net/heian_99/article/details/104062470',
            'https://blog.csdn.net/heian_99/article/details/104061818',
            'https://blog.csdn.net/heian_99/article/details/104061361',
            'https://blog.csdn.net/heian_99/article/details/104061077',
            'https://blog.csdn.net/heian_99/article/details/104040379',
            'https://blog.csdn.net/heian_99/article/details/104039886',
            'https://blog.csdn.net/heian_99/article/details/104039706',
            'https://blog.csdn.net/heian_99/article/details/104032121',
            'https://blog.csdn.net/heian_99/article/details/104031458',
            'https://blog.csdn.net/heian_99/article/details/104030173',
            'https://blog.csdn.net/heian_99/article/details/104030019',
            'https://blog.csdn.net/heian_99/article/details/104028739',
            'https://blog.csdn.net/heian_99/article/details/104028407',
            'https://blog.csdn.net/heian_99/article/details/104028229',
            'https://blog.csdn.net/heian_99/article/details/104027379',
            'https://blog.csdn.net/heian_99/article/details/104018522',
            'https://blog.csdn.net/heian_99/article/details/103959379',
            'https://blog.csdn.net/heian_99/article/details/103958032',
            'https://blog.csdn.net/heian_99/article/details/103956931',
            'https://blog.csdn.net/heian_99/article/details/103956583',
            'https://blog.csdn.net/heian_99/article/details/103952955',
            'https://blog.csdn.net/heian_99/article/details/103937535',
            'https://blog.csdn.net/heian_99/article/details/103933928',
            'https://blog.csdn.net/heian_99/article/details/103918683',
            'https://blog.csdn.net/heian_99/article/details/103888459',
            'https://blog.csdn.net/heian_99/article/details/103829912',
            'https://blog.csdn.net/heian_99/article/details/103824234',
            'https://blog.csdn.net/heian_99/article/details/103820693',
            'https://blog.csdn.net/heian_99/article/details/103819637',
            'https://blog.csdn.net/heian_99/article/details/103818231',
            'https://blog.csdn.net/heian_99/article/details/103817642',
            'https://blog.csdn.net/heian_99/article/details/103817375',
            'https://blog.csdn.net/heian_99/article/details/103683153',
            'https://blog.csdn.net/heian_99/article/details/103609082',
            'https://blog.csdn.net/heian_99/article/details/103599750',
            'https://blog.csdn.net/heian_99/article/details/103569873',
            'https://blog.csdn.net/heian_99/article/details/103504464',
            'https://blog.csdn.net/heian_99/article/details/103476254',
            'https://blog.csdn.net/heian_99/article/details/103475880',
            'https://blog.csdn.net/heian_99/article/details/103474709',
            'https://blog.csdn.net/heian_99/article/details/103461853',
            'https://blog.csdn.net/heian_99/article/details/103454612',
            'https://blog.csdn.net/heian_99/article/details/103452223',
            'https://blog.csdn.net/heian_99/article/details/103452072',
            'https://blog.csdn.net/heian_99/article/details/103451944',
            'https://blog.csdn.net/heian_99/article/details/103403143',
            'https://blog.csdn.net/heian_99/article/details/103391454',
            'https://blog.csdn.net/heian_99/article/details/103391378',
            'https://blog.csdn.net/heian_99/article/details/103323734',
            'https://blog.csdn.net/heian_99/article/details/103298249',
            'https://blog.csdn.net/heian_99/article/details/103292763',
            'https://blog.csdn.net/heian_99/article/details/103264404',
            'https://blog.csdn.net/heian_99/article/details/103250453',
            'https://blog.csdn.net/heian_99/article/details/103145574',
            'https://blog.csdn.net/heian_99/article/details/103144874',
            'https://blog.csdn.net/heian_99/article/details/103117319',
            'https://blog.csdn.net/heian_99/article/details/103089408',
            'https://blog.csdn.net/heian_99/article/details/103072006',
            'https://blog.csdn.net/heian_99/article/details/103013889',
            'https://blog.csdn.net/heian_99/article/details/102835825',
            'https://blog.csdn.net/heian_99/article/details/102835164',
            'https://blog.csdn.net/heian_99/article/details/102776037',
            'https://blog.csdn.net/heian_99/article/details/102759058',
            'https://blog.csdn.net/heian_99/article/details/102753123',
            'https://blog.csdn.net/heian_99/article/details/102752974',
            'https://blog.csdn.net/heian_99/article/details/102482992',
            'https://blog.csdn.net/heian_99/article/details/102477556',
            'https://blog.csdn.net/heian_99/article/details/102400260',
            'https://blog.csdn.net/heian_99/article/details/101613518',
            'https://blog.csdn.net/heian_99/article/details/101612415',
            'https://blog.csdn.net/heian_99/article/details/101458234',
            'https://blog.csdn.net/heian_99/article/details/101454487',
            'https://blog.csdn.net/heian_99/article/details/101270457',
            'https://blog.csdn.net/heian_99/article/details/101266165',
            'https://blog.csdn.net/heian_99/article/details/101203824',
            'https://blog.csdn.net/heian_99/article/details/100899244',
            'https://blog.csdn.net/heian_99/article/details/100601716',
            'https://blog.csdn.net/heian_99/article/details/100601244',
            'https://blog.csdn.net/heian_99/article/details/100557054',
            'https://blog.csdn.net/heian_99/article/details/100556646',
            'https://blog.csdn.net/heian_99/article/details/100556560',
            'https://blog.csdn.net/heian_99/article/details/100556433',
            'https://blog.csdn.net/heian_99/article/details/100158832',
            'https://blog.csdn.net/heian_99/article/details/99963775',
            'https://blog.csdn.net/heian_99/article/details/99957582',
            'https://blog.csdn.net/heian_99/article/details/90320984',
            'https://blog.csdn.net/heian_99/article/details/90217162',
            'https://blog.csdn.net/heian_99/article/details/90216301',
            'https://blog.csdn.net/heian_99/article/details/90215703',
            'https://blog.csdn.net/heian_99/article/details/90146007',
            'https://blog.csdn.net/heian_99/article/details/89684394',
            'https://blog.csdn.net/heian_99/article/details/89607814',
            'https://blog.csdn.net/heian_99/article/details/89576698',
            'https://blog.csdn.net/heian_99/article/details/89484004',
            'https://blog.csdn.net/heian_99/article/details/89461696',
            'https://blog.csdn.net/heian_99/article/details/89441218',
            'https://blog.csdn.net/heian_99/article/details/89441119',
            'https://blog.csdn.net/heian_99/article/details/89440812',
            'https://blog.csdn.net/heian_99/article/details/89422787',
            'https://blog.csdn.net/heian_99/article/details/89422328',
            'https://blog.csdn.net/heian_99/article/details/89410099',
            'https://blog.csdn.net/heian_99/article/details/89409908',
            'https://blog.csdn.net/heian_99/article/details/89390371',
            'https://blog.csdn.net/heian_99/article/details/89389495',
            'https://blog.csdn.net/heian_99/article/details/89383210',
            'https://blog.csdn.net/heian_99/article/details/89367651',
            'https://blog.csdn.net/heian_99/article/details/89358160',
            'https://blog.csdn.net/heian_99/article/details/89342729',
            'https://blog.csdn.net/heian_99/article/details/89339520',
            'https://blog.csdn.net/heian_99/article/details/89331002',
            'https://blog.csdn.net/heian_99/article/details/89326404',
            'https://blog.csdn.net/heian_99/article/details/89323383',
            'https://blog.csdn.net/heian_99/article/details/89323328',
            'https://blog.csdn.net/heian_99/article/details/89323274',
            'https://blog.csdn.net/heian_99/article/details/89303821',
            'https://blog.csdn.net/heian_99/article/details/89302303',
            'https://blog.csdn.net/heian_99/article/details/89301718',
            'https://blog.csdn.net/heian_99/article/details/89222331',
            'https://blog.csdn.net/heian_99/article/details/89195974',
            'https://blog.csdn.net/heian_99/article/details/89164144',
            'https://blog.csdn.net/heian_99/article/details/88979279',
            'https://blog.csdn.net/heian_99/article/details/88959650',
            'https://blog.csdn.net/heian_99/article/details/88955260',
            'https://blog.csdn.net/heian_99/article/details/88769852',
            'https://blog.csdn.net/heian_99/article/details/88727764',
            'https://blog.csdn.net/heian_99/article/details/88699584',
            'https://blog.csdn.net/heian_99/article/details/88675318',
            'https://blog.csdn.net/heian_99/article/details/88625227',
            'https://blog.csdn.net/heian_99/article/details/88562605',
            'https://blog.csdn.net/heian_99/article/details/88560250',
            'https://blog.csdn.net/heian_99/article/details/88430654',
            'https://blog.csdn.net/heian_99/article/details/88427082',
            'https://blog.csdn.net/heian_99/article/details/88359032',
            'https://blog.csdn.net/heian_99/article/details/88254043',
            'https://blog.csdn.net/heian_99/article/details/88205283',
            'https://blog.csdn.net/heian_99/article/details/88204612',
            'https://blog.csdn.net/heian_99/article/details/88199567',
            'https://blog.csdn.net/heian_99/article/details/88196569',
            'https://blog.csdn.net/heian_99/article/details/88195866',
            'https://blog.csdn.net/heian_99/article/details/86764111',
            'https://blog.csdn.net/heian_99/article/details/86761020',
            'https://blog.csdn.net/heian_99/article/details/86760760',
            'https://blog.csdn.net/heian_99/article/details/86751835',
            'https://blog.csdn.net/heian_99/article/details/86751693',
            'https://blog.csdn.net/heian_99/article/details/86743862',
            'https://blog.csdn.net/heian_99/article/details/86726181',
            'https://blog.csdn.net/heian_99/article/details/86725989',
            'https://blog.csdn.net/heian_99/article/details/86708327',
            'https://blog.csdn.net/heian_99/article/details/86692562',
            'https://blog.csdn.net/heian_99/article/details/86691863',
            'https://blog.csdn.net/heian_99/article/details/86678634',
            'https://blog.csdn.net/heian_99/article/details/86670442',
            'https://blog.csdn.net/heian_99/article/details/86658815',
            'https://blog.csdn.net/heian_99/article/details/86657141',
            'https://blog.csdn.net/heian_99/article/details/86651933',
            'https://blog.csdn.net/heian_99/article/details/86651652',
            'https://blog.csdn.net/heian_99/article/details/86634177',
            'https://blog.csdn.net/heian_99/article/details/86618970',
            'https://blog.csdn.net/heian_99/article/details/86617160',
            'https://blog.csdn.net/heian_99/article/details/86555639',
            'https://blog.csdn.net/heian_99/article/details/86035721',
            'https://blog.csdn.net/heian_99/article/details/85924646',
            'https://blog.csdn.net/heian_99/article/details/85851144',
            'https://blog.csdn.net/heian_99/article/details/85790244',
            'https://blog.csdn.net/heian_99/article/details/85711660',
            'https://blog.csdn.net/heian_99/article/details/85709014',
            'https://blog.csdn.net/heian_99/article/details/85703269',
            'https://blog.csdn.net/heian_99/article/details/85624511']
    # urls = []
    # urls.append('https://blog.csdn.net/heian_99/article/details/127610131')
    print('共找到%d篇文章...' % len(urls))
    return urls


def get_html_from_csdn(url):
    html = requests.get(url, headers=headers).text
    # print(html)
    selector = parsel.Selector(html)
    title = selector.css('div.article-title-box > h1::text').get()
    article = selector.css('div.article_content').get()
    category = selector.css('div.blog-tags-box > div > a::text').getall()

    category_list = []
    for i in category:
        list_ca = i.replace('#', '')
        category_list.append(list_ca)

    tags = selector.css('div.blog-tags-box > div > a[data-report-click*="mod"]::text').getall()

    result = filter(lambda x: x not in tags, category_list)

    category_list = list(result)
    time_stamp = selector.css('div > span.time::text').get()
    author = selector.css('#uid > span.name::text').get()
    origin = url
    return title, article, category_list, tags, time_stamp, author, origin


def html_to_md(title, article, category_list, tags, time_stamp, author, origin):
    md = tomd.convert(article)
    # print(md)
    # 图片url标准化
    url_pattern = re.compile(r'<img.*?(https://.*?\.gif|https://.*?\.png).*?">')
    for src_url in url_pattern.finditer(md):
        img_name = src_url.group(1).split('/')[-1]
        md = md.replace(src_url.group(0), '![%s](%s)' % (img_name, src_url.group(1)))
    time_stamp = handleDate(time_stamp)
    # file_dir = time_stamp.split(" ")[0]
    year = time_stamp.split("-")[0]
    month = time_stamp.split("-")[1]
    dir_file = "articles/" + year + "/" + month
    create_directory_if_not_exists(dir_file)

    print('正在下载 %s' % title)
    # text = "> 标题: %s <br> 日期: %s<br> 标签: [%s]<br> 分类: %s<br> \n\n> 作者: %s\n> 原文链接: %s\n%s" % (
    #     title, time_stamp, ', '.join(tags), category, author, origin, md)

    ########################
    # text = "+++ \ntitle: %s\ndate: %s\ntags: [%s]\ncategories: %s\n---\n\n> author: %s\n> 原文链接: %s +++\n%s" % (
    #     title, time_stamp, ', '.join(tags), category, author, origin, md)
    url_image = get_images_url()
    text = f"""+++\nauthor = "{author}"\ntitle = "{title}"\ndate = "{time_stamp}"\ntags={tags}\ncategories={category_list}\nimage = "{url_image}"\n+++\n[作者：{author}   原文链接:{origin}]({origin})\n{md}"""
    ########################
    # Windows下文件名字不能包含特殊符号

    file_name = re.sub(r'[\\/:*?"<>|]', ' ', title)
    with open('%s/%s.md' % (dir_file, file_name.strip()), 'w', encoding='utf-8') as f:
        f.write(text)


def main(url):
    if not os.path.exists('articles'):
        os.mkdir('articles')
    article_urls = get_article_info(url)
    for article_url in article_urls:
        title, article, category, tags, time_stamp, author, origin = get_html_from_csdn(article_url)
        html_to_md(title, article, category, tags, time_stamp, author, origin)
    print('完成%d篇文章的下载' % len(article_urls))


if __name__ == '__main__':
    headers = {
        'Host': 'blog.csdn.net',
        'Referer': 'https://blog.csdn.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3542.0 Safari/537.36'
    }
    start_url = "https://blog.csdn.net/heian_99"
    main(start_url)
