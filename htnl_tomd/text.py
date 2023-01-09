# -*- coding: <encoding name> -*-
# 1. 获取整个页面数据
import requests

url = 'https://blog.csdn.net/heian_99/article/details/128476559'
html = requests.get(url=url).content

# 2. 提取正文中的HTML文本
from bs4 import BeautifulSoup
text="""
<article class="baidu_pl">
        <div id="article_content" class="article_content clearfix">
        <link rel="stylesheet" href="https://csdnimg.cn/release/blogv2/dist/mdeditor/css/editerView/kdoc_html_views-fbd6fff466.css">
        <link rel="stylesheet" href="https://csdnimg.cn/release/blogv2/dist/mdeditor/css/editerView/ck_htmledit_views-6e43165c0a.css">
                <div id="content_views" class="markdown_views prism-atom-one-dark">
                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <path stroke-linecap="round" d="M5,0 0,2.5 5,5z" id="raphael-marker-block" style="-webkit-tap-highlight-color: rgba(0, 0, 0, 0);"></path>
                    </svg>
                    <h3><a name="t0"></a><a id="HTMLMarkdown_0"></a>爬虫：页面内容提取，HTML直接输出为Markdown格式</h3> 
<p>注意：对内联公式效果较差，建议用https://editor.mdnice.com/的SitDown</p> 
<h1><a name="t1"></a><a id="HTMLMarkdownCSDN_4"></a>爬虫：页面内容提取，HTML直接输出为Markdown格式，对CSDN博客有效</h1> 
<p>这种方法也可以提取博客中<a href="https://so.csdn.net/so/search?q=%E6%B0%B4%E5%8D%B0&amp;spm=1001.2101.3001.7020" target="_blank" class="hl hl-1" data-report-click="{&quot;spm&quot;:&quot;1001.2101.3001.7020&quot;,&quot;dest&quot;:&quot;https://so.csdn.net/so/search?q=%E6%B0%B4%E5%8D%B0&amp;spm=1001.2101.3001.7020&quot;,&quot;extra&quot;:&quot;{\&quot;searchword\&quot;:\&quot;水印\&quot;}&quot;}" data-tit="水印" data-pretit="水印">水印</a>图片的原图。</p> 
<h2><a name="t2"></a><a id="1_HTML_6"></a>1. 提取HTML中的作者、发布日期与内容信息</h2> 
<pre data-index="0" class="prettyprint"><code class="prism language-text has-numbering" onclick="mdcp.copyCode(event)" style="position: unset;">pip install gne
<div class="hljs-button {2}" data-title="复制"></div></code><ul class="pre-numbering" style=""><li style="color: rgb(153, 153, 153);">1</li></ul></pre> 
<pre data-index="1" class="prettyprint"><code class="prism language-python has-numbering" onclick="mdcp.copyCode(event)" style="position: unset;"><span class="token comment"># 1. 获取页面文本</span>
<span class="token keyword">import</span> requests
<span class="token keyword">import</span> kuser_agent <span class="token comment">#pip install kuser_agent</span>

url <span class="token operator">=</span> <span class="token string">'https://blog.csdn.net/weixin_54227557?type=blog'</span>
html <span class="token operator">=</span> requests<span class="token punctuation">.</span>get<span class="token punctuation">(</span>url<span class="token operator">=</span>url<span class="token punctuation">,</span>headers<span class="token operator">=</span><span class="token punctuation">{<!-- --></span><span class="token string">'User-Agent'</span><span class="token punctuation">:</span>kuser_agent<span class="token punctuation">.</span>get<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">.</span>text


<span class="token comment"># 2.提取关键内容</span>
<span class="token keyword">import</span> gne
extractor <span class="token operator">=</span> gne<span class="token punctuation">.</span>GeneralNewsExtractor<span class="token punctuation">(</span><span class="token punctuation">)</span>
result <span class="token operator">=</span> extractor<span class="token punctuation">.</span>extract<span class="token punctuation">(</span>html<span class="token punctuation">)</span>

<span class="token keyword">for</span> key <span class="token keyword">in</span> result<span class="token punctuation">.</span>keys<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">:</span>
    <span class="token keyword">print</span><span class="token punctuation">(</span>key<span class="token punctuation">,</span><span class="token string">':'</span><span class="token punctuation">,</span>result<span class="token punctuation">[</span>key<span class="token punctuation">]</span><span class="token punctuation">)</span>
<div class="hljs-button {2}" data-title="复制"></div></code><ul class="pre-numbering" style=""><li style="color: rgb(153, 153, 153);">1</li><li style="color: rgb(153, 153, 153);">2</li><li style="color: rgb(153, 153, 153);">3</li><li style="color: rgb(153, 153, 153);">4</li><li style="color: rgb(153, 153, 153);">5</li><li style="color: rgb(153, 153, 153);">6</li><li style="color: rgb(153, 153, 153);">7</li><li style="color: rgb(153, 153, 153);">8</li><li style="color: rgb(153, 153, 153);">9</li><li style="color: rgb(153, 153, 153);">10</li><li style="color: rgb(153, 153, 153);">11</li><li style="color: rgb(153, 153, 153);">12</li><li style="color: rgb(153, 153, 153);">13</li><li style="color: rgb(153, 153, 153);">14</li><li style="color: rgb(153, 153, 153);">15</li></ul></pre> 
<h2><a name="t3"></a><a id="2_HTMLMarkdown_31"></a>2. 把HTML转成Markdown的文本</h2> 
<pre data-index="2" class="prettyprint"><code class="prism language-python has-numbering" onclick="mdcp.copyCode(event)" style="position: unset;"><span class="token comment"># 1. 获取整个页面数据</span>
<span class="token keyword">import</span> requests
<span class="token keyword">import</span> kuser_agent
url <span class="token operator">=</span> <span class="token string">'https://blog.csdn.net/weixin_54227557/article/details/122254246?spm=1001.2014.3001.5502'</span>
html <span class="token operator">=</span> requests<span class="token punctuation">.</span>get<span class="token punctuation">(</span>url<span class="token operator">=</span>url<span class="token punctuation">,</span>headers<span class="token operator">=</span><span class="token punctuation">{<!-- --></span><span class="token string">'User-Agent'</span><span class="token punctuation">:</span>kuser_agent<span class="token punctuation">.</span>get<span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">.</span>content

<span class="token comment"># 2. 提取正文中的HTML文本</span>
<span class="token keyword">from</span> bs4 <span class="token keyword">import</span> BeautifulSoup
bs <span class="token operator">=</span> BeautifulSoup<span class="token punctuation">(</span>html<span class="token punctuation">)</span>
text <span class="token operator">=</span> bs<span class="token punctuation">.</span>find<span class="token punctuation">(</span>attrs<span class="token operator">=</span><span class="token punctuation">{<!-- --></span><span class="token string">'id'</span><span class="token punctuation">:</span><span class="token string">'article_content'</span><span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">.</span>prettify<span class="token punctuation">(</span><span class="token punctuation">)</span>

<span class="token comment"># 3. 将HTML文本转成Markdown格式</span>
<span class="token keyword">import</span> html2text

ht <span class="token operator">=</span> html2text<span class="token punctuation">.</span>HTML2Text<span class="token punctuation">(</span><span class="token punctuation">)</span>
<span class="token comment"># 一般的参数设置</span>
ht<span class="token punctuation">.</span>bypass_tables <span class="token operator">=</span> <span class="token boolean">False</span>
ht<span class="token punctuation">.</span>mark_code <span class="token operator">=</span> <span class="token boolean">True</span>
ht<span class="token punctuation">.</span>code <span class="token operator">=</span> <span class="token boolean">True</span>
<span class="token comment"># --------------</span>
result <span class="token operator">=</span> ht<span class="token punctuation">.</span>handle<span class="token punctuation">(</span>text<span class="token punctuation">)</span>
<span class="token keyword">print</span><span class="token punctuation">(</span>result<span class="token punctuation">)</span>
<div class="hljs-button {2}" data-title="复制"></div></code><ul class="pre-numbering" style=""><li style="color: rgb(153, 153, 153);">1</li><li style="color: rgb(153, 153, 153);">2</li><li style="color: rgb(153, 153, 153);">3</li><li style="color: rgb(153, 153, 153);">4</li><li style="color: rgb(153, 153, 153);">5</li><li style="color: rgb(153, 153, 153);">6</li><li style="color: rgb(153, 153, 153);">7</li><li style="color: rgb(153, 153, 153);">8</li><li style="color: rgb(153, 153, 153);">9</li><li style="color: rgb(153, 153, 153);">10</li><li style="color: rgb(153, 153, 153);">11</li><li style="color: rgb(153, 153, 153);">12</li><li style="color: rgb(153, 153, 153);">13</li><li style="color: rgb(153, 153, 153);">14</li><li style="color: rgb(153, 153, 153);">15</li><li style="color: rgb(153, 153, 153);">16</li><li style="color: rgb(153, 153, 153);">17</li><li style="color: rgb(153, 153, 153);">18</li><li style="color: rgb(153, 153, 153);">19</li><li style="color: rgb(153, 153, 153);">20</li><li style="color: rgb(153, 153, 153);">21</li><li style="color: rgb(153, 153, 153);">22</li></ul></pre>
                </div>
                <link href="https://csdnimg.cn/release/blogv2/dist/mdeditor/css/editerView/markdown_views-22a2fefd3b.css" rel="stylesheet">
                <link href="https://csdnimg.cn/release/blogv2/dist/mdeditor/css/style-4566211012.css" rel="stylesheet">
        </div>
        <div id="treeSkill" style="display: block;"><div class="skill-tree-box"><div class="skill-tree-head">文章知识点与官方知识档案匹配，可进一步学习相关知识</div><div class="skill-tree-body"><div class="skill-tree-item"><span class="skill-tree-href"><a data-report-click="{&quot;spm&quot;:&quot;1001.2101.3001.6866&quot;,&quot;dest&quot;:&quot;https://edu.csdn.net/skill/python/&quot;}" href="https://edu.csdn.net/skill/python/" target="_blank">Python入门技能树</a><i></i><a data-report-click="{&quot;spm&quot;:&quot;1001.2101.3001.6866&quot;,&quot;dest&quot;:&quot;https://edu.csdn.net/skill/python/&quot;}" href="https://edu.csdn.net/skill/python/" target="_blank">首页</a><i></i><a data-report-click="{&quot;spm&quot;:&quot;1001.2101.3001.6866&quot;,&quot;dest&quot;:&quot;https://edu.csdn.net/skill/python/&quot;}" href="https://edu.csdn.net/skill/python/" target="_blank">概览</a></span><span class="skill-tree-con"><span class="skill-tree-count">211446</span> 人正在系统学习中</span></div></div></div></div>
    </article>
"""
# 3. 将HTML文本转成Markdown格式
import html2text

ht = html2text.HTML2Text()
# 一般的参数设置
ht.bypass_tables = False
ht.mark_code = True
ht.code = True
# --------------
result = ht.handle(text)
print(result)
