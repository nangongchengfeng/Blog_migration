import requests
import parsel
import tomd
import os
import re


# 对一篇文章的爬取
def spider_csdn(title_url):  # 目标文章的链接
    path = os.getcwd()  # 获取当前的目录路径
    file_name = "/passage"

    final_road = path + file_name
    images_dir = final_road + "/images/"
    if not os.path.exists(images_dir):
        os.mkdir(images_dir)

    if not os.path.exists(final_road):
        os.mkdir(final_road)


    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52",
        "Referer": "https://blog.csdn.net/tansty_zh"
    }
    html = requests.get(url=title_url, headers=head).text
    page = parsel.Selector(html)
    # 创建解释器
    title = page.css(".title-article::text").get()

    content = page.css("article").get()
    content = re.sub(r'<a[^>]*>(.*?)</a>', r'\1', content)
    # content = re.sub("<a.*?a>", "", content)
    content = re.sub("<br>", "", content)
    content = re.sub("&lt;", "<", content)  # 新增
    content = re.sub("&gt;", ">", content)  # 新增
    text = tomd.Tomd(content).markdown
    print(content)
    url_pattern = re.compile(r'<img.*?(https://.*?\.gif|https://.*?\.png).*?">')

    for url in url_pattern.findall(text):

        response = requests.get(url)
        # 保存图片到本地文件夹
        with open(images_dir + url.split('/')[-1], 'wb') as f:
            f.write(response.content)


    # 图片url标准化
    print("============================================================")
    for src_url in url_pattern.finditer(text):
        img_name = src_url.group(1).split('/')[-1]
        md_img = f'![{img_name}](images/{img_name})'
        text = text.replace(src_url.group(0), md_img)

    print("============================================================")
    # print(text)
    # 转换为markdown 文件

    try:
        os.mkdir(images_dir)
        os.mkdir(final_road)
        print('创建成功！')
    except:
        print('目录已经存在或异常')
    # 2、 下载图片
    print(images_dir)

    with open(final_road + r"./" + title + ".md", mode="w", encoding="utf-8") as f:
        f.write("#" + title)
        f.write(text)


def main():
    print("本项目由tansty开发")
    # url = input("请输入网址：")
    spider_csdn("https://blog.csdn.net/heian_99/article/details/129563377")
    # spider_csdn("https://blog.csdn.net/heian_99/article/details/106939828")



if __name__ == '__main__':
    main()
