from pyquery import PyQuery as pq

# 指定模块 __all__ 属性，以便 import * 时只导入指定的函数
__all__ = ['Tomd', 'convert']

# 定义常量，用于将 HTML 元素转换成 Markdown 格式
MARKDOWN = {
    'h1': "#",
    'h2': "##",
    'h3': "###",
    'h4': "####",
    'h5': "#####",
    'h6': "######",
    "blockquote": ">",
    "li": "-",
    "hr": "---",
    "p": "\n"
}

INLINE = {
    'em': ('*', '*'),
    'strong': ('**', '**'),
    'b': ('**', '**'),
    'i': ('*', '*'),
    'del': ('~~', '~~'),
    "code": ('`', '`')
}

# 定义分隔符，用于将代码块和其他元素区分开来
split_str = "++++++++++++++++++"


# 定义 Tomd 类，用于将 HTML 转换成 Markdown
class Tomd:
    def __init__(self, html=''):
        self.html = html
        self._markdown = ""

    def convert(self, html=""):
        # 使用 pyquery 解析 HTML
        d = pq(html)
        # 移除 head 元素
        d('head').remove()
        # 获取处理后的 HTML
        html = d.html()

        # 处理 span 元素
        d = pq(html)
        for e in d('span'):
            # 将 span 中的文本作为内联元素的标记
            inline_mark = pq(e).text()
            html = html.replace(str(pq(e)), inline_mark)

        # 处理 a 元素
        d = pq(html)
        for e in d('a'):
            # 如果 a 元素的 href 属性中包含 http，则将其转换为 Markdown 的链接格式
            if "http" in pq(e).attr('href'):
                inline_mark = f"[{pq(e).text()}]({pq(e).attr('href')})"
                html = html.replace(str(pq(e)), inline_mark)

        # 处理 img 元素
        d = pq(html)
        for e in d('img'):
            # 将 img 元素转换为 Markdown 的图片格式
            inline_mark = f"![{pq(e).attr('alt')}]({pq(e).attr('src')})"
            html = html.replace(str(pq(e)), inline_mark)

        # 处理表格中的 thead 元素
        d = pq(html)
        for e in d('thead'):
            # 将 thead 元素转换为 Markdown 的表格格式
            inline_mark = pq(e).outer_html() + '|------' * (pq(e)('th').length - 1)
            html = html.replace(str(pq(e)), inline_mark)

        # 处理表格中的 th 和 td 元素
        d = pq(html)
        for e in d('th,td'):
            # 将 th 和 td 元素转换为 Markdown 的表格格式
            inline_mark = "|" + pq(e).text()
            html = html.replace(str(pq(e)), inline_mark)

        d = pq(html)
        # 处理代码块
        for e in d('pre'):
            inline_mark = "```" + split_str + pq(e).html() + split_str + "```" + split_str
            html = html.replace(str(pq(e)), inline_mark)

        # 处理行内元素
        d = pq(html)
        selectors = ','.join(INLINE.keys())
        for e in d(selectors):
            inline_mark = INLINE.get(e.tag)[0] + pq(e).text() + INLINE.get(e.tag)[1]
            html = html.replace(str(pq(e)), inline_mark)

        # 处理块级元素
        d = pq(html)
        selectors = ','.join(MARKDOWN.keys())
        for e in d(selectors):
            inline_mark = split_str + MARKDOWN.get(e.tag) + " " + pq(e).text() + split_str
            html = html.replace(str(pq(e)), inline_mark)

        # 将HTML转化为Markdown格式
        self._markdown = pq(html).text().replace(split_str, '\n')

        print(self._markdown)
        return self._markdown

    # 获取Markdown格式的字符串
    @property
    def markdown(self):
        self.convert(self.html)
        return self._markdown


_inst = Tomd()
convert = _inst.convert
