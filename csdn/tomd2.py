import re

__all__ = ['Tomd', 'convert']

# 用于存储每个元素标记的Markdown开始和结束字符串
MARKDOWN = {
    'h1': ('\n# ', '\n'),
    'h2': ('\n## ', '\n'),
    'h3': ('\n### ', '\n'),
    'h4': ('\n#### ', '\n'),
    'h5': ('\n##### ', '\n'),
    'h6': ('\n###### ', '\n'),
    'code': ('`', '`'),
    'ul': ('', ''),
    'ol': ('', ''),
    'li': ('- ', ''),
    'blockquote': ('\n> ', '\n'),
    'em': ('**', '**'),
    'strong': ('**', '**'),
    'block_code': ('\n```\n', '\n```\n'),
    'span': ('', ''),
    'p': ('\n', '\n'),
    'p_with_out_class': ('\n', '\n'),
    'inline_p': ('', ''),
    'inline_p_with_out_class': ('', ''),
    'b': ('**', '**'),
    'i': ('*', '*'),
    'del': ('~~', '~~'),
    'hr': ('\n---', '\n\n'),
    'thead': ('\n', '|------\n'),
    'tbody': ('\n', '\n'),
    'td': ('|', ''),
    'th': ('|', ''),
    'tr': ('', '\n')
}

# BlOCK_ELEMENTS（用于存储可识别为块级元素的正则表达式模式）
BlOCK_ELEMENTS = {
    'h1': '<h1.*?>(.*?)</h1>',
    'h2': '<h2.*?>(.*?)</h2>',
    'h3': '<h3.*?>(.*?)</h3>',
    'h4': '<h4.*?>(.*?)</h4>',
    'h5': '<h5.*?>(.*?)</h5>',
    'h6': '<h6.*?>(.*?)</h6>',
    'hr': '<hr/>',
    'blockquote': '<blockquote.*?>(.*?)</blockquote>',
    'ul': '<ul.*?>(.*?)</ul>',
    'ol': '<ol.*?>(.*?)</ol>',
    'block_code': '<pre.*?><code.*?>(.*?)</code></pre>',
    'p': '<p\s.*?>(.*?)</p>',
    'p_with_out_class': '<p>(.*?)</p>',
    'thead': '<thead.*?>(.*?)</thead>',
    'tr': '<tr>(.*?)</tr>'
}
# INLINE_ELEMENTS（用于存储可识别为行内元素的正则表达式模式
INLINE_ELEMENTS = {
    'td': '<td>(.*?)</td>',
    'tr': '<tr>(.*?)</tr>',
    'th': '<th>(.*?)</th>',
    'b': '<b>(.*?)</b>',
    'i': '<i>(.*?)</i>',
    'del': '<del>(.*?)</del>',
    'inline_p': '<p\s.*?>(.*?)</p>',
    'inline_p_with_out_class': '<p>(.*?)</p>',
    'code': '<code.*?>(.*?)</code>',
    'span': '<span.*?>(.*?)</span>',
    'ul': '<ul.*?>(.*?)</ul>',
    'ol': '<ol.*?>(.*?)</ol>',
    'li': '<li.*?>(.*?)</li>',
    'img': '<img.*?src="(.*?)".*?>(.*?)</img>',
    'a': '<a.*?href="(.*?)".*?>(.*?)</a>',
    'em': '<em.*?>(.*?)</em>',
    'strong': '<strong.*?>(.*?)</strong>'
}

# DELETE_ELEMENTS是一个列表，其中包含要从HTML中删除的元素模式
DELETE_ELEMENTS = ['<span.*?>', '</span>', '<div.*?>', '</div>']


# Python类Element，它表示在HTML文档中的元素。构造函数接受包含元素标签内内容的字符串content，
# 起始位置和结束位置的整数start_pos和end_pos，元素标记的字符串tag以及一个布尔值is_block来指示该元素是否是块级元素。
class Element:
    def __init__(self, start_pos, end_pos, content, tag, lang, is_block=False):
        self.start_pos = start_pos  # 元素起始位置
        self.end_pos = end_pos  # 元素结束位置
        self.content = content  # 元素内容
        self._elements = []  # 子元素列表
        self.is_block = is_block  # 是否是块级元素
        self.tag = tag  # 元素标记
        self.lang = lang  # 语言标记
        self._result = None  # 转换为Markdown格式的结果字符串

        if self.is_block:  # 如果是块级元素
            self.parse_inline()  # 解析行内元素

    # __str__方法将该元素转换为Markdown格式的字符串
    def __str__(self):
        wrapper = MARKDOWN.get(self.tag)  # 获取该标签的Markdown格式包装
        if self.tag == 'block_code':
            wrapper = (f'\n```{self.lang}\n', '\n```')
            print(self.lang)
            self._result = '{}{}{}'.format(wrapper[0], self.content, wrapper[1])  # 使用Markdown格式包装将标签内容包装
        else:
            self._result = '{}{}{}'.format(wrapper[0], self.content, wrapper[1])  # 使用Markdown格式包装将标签内容包装
        return self._result

    # parse_inline方法解析块级元素内的所有行内元素，并将其替换为相应的Markdown代码
    def parse_inline(self):
        # 遍历内联元素规则，逐一替换对应的Markdown格式字符串
        for tag, pattern in INLINE_ELEMENTS.items():

            if tag == 'a':  # 如果是a标签
                self.content = re.sub(pattern, '[\g<2>](\g<1>)', self.content)  # 将内容替换为Markdown格式的链接
            elif tag == 'img':
                self.content = re.sub(pattern, '![\g<2>](\g<1>)', self.content)
            elif self.tag == 'ul' and tag == 'li':
                self.content = re.sub(pattern, '- \g<1>', self.content)
            elif self.tag == 'ol' and tag == 'li':
                self.content = re.sub(pattern, '1. \g<1>', self.content)
            elif self.tag == 'thead' and tag == 'tr':
                self.content = re.sub(pattern, '\g<1>\n', self.content.replace('\n', ''))
            elif self.tag == 'tr' and tag == 'th':
                self.content = re.sub(pattern, '|\g<1>', self.content.replace('\n', ''))
            elif self.tag == 'tr' and tag == 'td':
                self.content = re.sub(pattern, '|\g<1>', self.content.replace('\n', ''))
            else:
                # 如果是其他内联元素，替换成 Markdown 格式
                wrapper = MARKDOWN.get(tag)
                self.content = re.sub(pattern, '{}\g<1>{}'.format(wrapper[0], wrapper[1]), self.content)


# 这段什么意思，结合上面的变量，请代码格式化输出这一段，并在上面加上中文注释
class Tomd:
    def __init__(self, html='', options=None):
        # 初始化Tomd对象，传入的参数是HTML字符串和转换选项
        self.html = html
        self.options = options
        # 初始化一个空字符串，用于存储转换后的Markdown
        self._markdown = ''

    def convert(self, html, options=None):
        # 将HTML字符串转换成Markdown字符串
        elements = []
        # 遍历所有块级元素的正则表达式
        for tag, pattern in BlOCK_ELEMENTS.items():
            # 在HTML字符串中查找所有符合当前块级元素的模式的匹配
            for m in re.finditer(pattern, html, re.I | re.S | re.M):
                code_pattern = r'language-(\w+)'
                code_match = re.search(code_pattern, m.group())
                if code_match:
                    lang = code_match.group(1)
                    lang_code = re.search(r'\b(java|python|ruby|shell|bash)\b', lang)
                    if lang_code:
                        lang = lang_code.group(0)
                    else:
                        lang = 'bash'
                else:
                    lang = None
                # 创建一个Element对象，包含匹配的起始位置、结束位置、内容、标签、是否为块级元素等属性
                element = Element(start_pos=m.start(),
                                  end_pos=m.end(),
                                  content=''.join(m.groups()),
                                  tag=tag,
                                  lang=lang,
                                  is_block=True)
                can_append = True
                # 检查当前Element对象是否已经被包含在另一个Element对象中
                for e in elements:
                    if e.start_pos < m.start() and e.end_pos > m.end():
                        can_append = False
                    elif e.start_pos > m.start() and e.end_pos < m.end():
                        elements.remove(e)
                # 如果当前Element对象不被包含在任何一个已有的Element对象中，则将其添加到elements列表中
                if can_append:
                    elements.append(element)
        # 将elements列表中的所有元素按起始位置进行排序
        elements.sort(key=lambda element: element.start_pos)

        # 将elements列表中的所有Element对象转换成Markdown字符串
        self._markdown = ''.join([str(e) for e in elements])

        # 从Markdown字符串中删除所有要删除的元素
        for index, element in enumerate(DELETE_ELEMENTS):
            self._markdown = re.sub(element, '', self._markdown)
        # 返回转换后的Markdown字符串
        return self._markdown

    @property
    def markdown(self):
        # 获取HTML字符串的Markdown表示形式
        self.convert(self.html, self.options)
        # 返回转换后的Markdown字符串
        return self._markdown


# 创建一个Tomd对象实例
_inst = Tomd()
# 将convert方法赋值给一个名为convert的变量，方便调用
convert = _inst.convert

if __name__ == '__main__':
    print(INLINE_ELEMENTS)
    for i in INLINE_ELEMENTS:
        print(i)
