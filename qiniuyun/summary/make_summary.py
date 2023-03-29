# -*- coding: utf-8 -*-
# @Time    : 2023/3/29 17:48
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : make_summary.py
# @Software: PyCharm
import re

import jieba


# 定义一个函数来获取指定长度的摘要
def get_summary(text, summary_len=100):
    # 使用 jieba 分词将文本拆分成单词列表
    print(text)
    words = jieba.lcut(text)

    # 将单词列表组合成句子列表
    sentences = []
    sentence = ''
    for word in words:
        sentence += word
        if '。' in word or '！' in word or '？' in word:
            sentences.append(sentence)
            sentence = ''

    # 如果没有完整的句子，则将单词列表的前 summary_len 个单词作为摘要
    if not sentences:
        return ''.join(words[:summary_len])

    # 截取摘要的前 summary_len 个字符
    summary = ''
    for i, sentence in enumerate(sentences):
        summary += sentence
        if len(summary) >= summary_len:
            break

    return summary.strip()


def get_filename_url(filename):
    with open('old/' + filename, 'r', encoding='utf-8') as f:
        content = f.read()
        # 分割<!--more-->之前的内容
        content = content.split('<!--more-->')[-1]
        # print(content)
        pattern = re.compile('[\u4e00-\u9fa5，；：！？。、]+')
        chinese_text = ''.join(pattern.findall(content))
        # 取前70个字符并添加省略号
        extracted_text = chinese_text[:100] + '。。。。。。。'
        return extracted_text
        # print(content)


# 示例用法
content = get_filename_url("集群服务器的网络连接状态接入ELK（可视化操作）.md")
summary = get_summary(content)
print(summary)
