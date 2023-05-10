# -*- coding: utf-8 -*-
# @Time    : 2023/5/10 14:34
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : app.py
# @Software: PyCharm
from csdn_spider import get_info, get_blog
from dash import dcc
import dash
from dash import html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import datetime as dt
from sqlalchemy import create_engine
from flask_caching import Cache
import numpy as np

# 今天的时间
today = dt.datetime.today().strftime("%Y-%m-%d")

# 连接数据库
engine = create_engine('mysql+pymysql://root:123456@192.168.102.20/csdn?charset=utf8')

# 导入css样式
external_css = [
    "https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
    "http://raw.githack.com/ffzs/DA_dash_hr/master/css/my.css"
]

# 创建一个实例
app = dash.Dash(__name__, external_stylesheets=external_css)
server = app.server

# 可以选择使用缓存, 减少频繁的数据请求
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})

# 读取info表的数据
info = pd.read_sql('info', con=engine)

# print(info)
# 图表颜色
color_scale = ['#2c0772', '#3d208e', '#8D7DFF', '#CDCCFF', '#C7FFFB', '#ff2c6d', '#564b43', '#161d33']


def indicator(text, id_value):
    """第一列的文字及数字信息显示"""
    return html.Div([
        html.P(text, className="twelve columns indicator_text"),
        html.P(id=id_value, className="indicator_value"),
    ], className="col indicator")


def get_news_table(data):
    """获取文章列表, 根据阅读排序"""
    df = data.copy()
    df.sort_values('read_num', inplace=True, ascending=False)
    titles = df['title'].tolist()
    urls = df['url'].tolist()

    return html.Table([html.Tbody([
        html.Tr([
            html.Td(
                html.A(titles[i], href=urls[i], target="_blank", ))
        ], style={'height': '30px', 'fontSize': '16'}) for i in range(min(len(df), 100))
    ])], style={"height": "90%", "width": "98%"})


@cache.memoize(timeout=3590)
def get_catego():
    """获取当日最新的文章数据"""
    df = pd.read_sql("categorize", con=engine)
    return df


# @cache.memoize(timeout=3590), 可选择设置缓存, 我没使用
def get_df():
    """获取当日最新的文章数据"""
    # 设置pandas参数，使其以完整显示模式打印DataFrame
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', None)
    df = pd.read_sql(today, con=engine)
    df['date_day'] = df['date'].apply(lambda x: x.split(' ')[0]).astype('datetime64[ns]')
    df['date_month'] = df['date'].apply(lambda x: x[:7].split('-')[0] + "年" + x[:7].split('-')[-1] + "月")
    df['weekday'] = df['date_day'].dt.weekday
    df['year'] = df['date_day'].dt.year
    df['month'] = df['date_day'].dt.month
    df['week'] = df['date_day'].dt.isocalendar().week
    # print(df)
    return df


# 导航栏的图片及标题
head = html.Div([
    html.Div(html.Img(
        src='https://www.ownit.top/img/avatar_hu227367ba8544f2fc7811ed9508937bec_102665_300x0_resize_box_3.png',
        height="100%"),
        style={"float": "left", "height": "90%", "margin-top": "5px", "border-radius": "50%",
               "overflow": "hidden"}),
    html.Span("{}博客的Dashboard".format(info['author_name'][0]), className='app-title'),
], className="row header")

# 第一列的文字及数字信息
columns = info.columns[3:]
col_name = ['文章数', '关注数', '喜欢数', '评论数', '等级', '访问数', '积分', '排名']
row1 = html.Div([
    indicator(col_name[i], col) for i, col in enumerate(columns)
], className='row')

# 第二列
row2 = html.Div([
    html.Div([
        html.P("每月文章写作情况"),
        dcc.Graph(id="bar", style={"height": "90%", "width": "98%"}, config=dict(displayModeBar=False), )
    ], className="col-4 chart_div", ),
    html.Div([
        html.P("各类型文章占比情况"),
        dcc.Graph(id="pie", style={"height": "90%", "width": "98%"}, config=dict(displayModeBar=False), )
    ], className="col-4 chart_div"),
    html.Div([
        html.P("各类型文章阅读情况"),
        dcc.Graph(id="mix", style={"height": "90%", "width": "98%"}, config=dict(displayModeBar=False), )
    ], className="col-4 chart_div", )
], className='row')

# 年数统计, 我的是2019 2020 2021
years = get_df()['year'].unique()
select_list = ['每月文章', '类型占比', '类型阅读量', '每日情况']

# 两个可交互的下拉选项
dropDowm1 = html.Div([
    html.Div([
        dcc.Dropdown(id='dropdown1',
                     options=[{'label': '{}年'.format(year), 'value': year} for year in years],
                     value=years[1], style={'width': '40%'})
    ], className='col-6', style={'padding': '2px', 'margin': '0px 5px 0px'}),
    html.Div([
        dcc.Dropdown(id='dropdown2',
                     options=[{'label': select_list[i], 'value': item} for i, item in
                              enumerate(['bar', 'pie', 'mix', 'heatmap'])],
                     value='heatmap', style={'width': '40%'})
    ], className='col-6', style={'padding': '2px', 'margin': '0px 5px 0px'})
], className='row')

# 第三列
row3 = html.Div([
    html.Div([
        html.P("每日写作情况"),
        dcc.Graph(id="heatmap", style={"height": "90%", "width": "98%"}, config=dict(displayModeBar=False), )
    ], className="col-6 chart_div", ),
    html.Div([
        html.P("文章列表"),
        html.Div(get_news_table(get_df()), id='click-data'),
    ], className="col-6 chart_div", style={"overflowY": "scroll"})
], className='row')

# 总体情况
app.layout = html.Div([
    # 定时器
    dcc.Interval(id="stream", interval=1000 * 60, n_intervals=0),
    dcc.Interval(id="river", interval=1000 * 60 * 60, n_intervals=0),
    html.Div(id="load_info", style={"display": "none"}, ),
    html.Div(id="load_click_data", style={"display": "none"}, ),
    head,
    html.Div([
        row1,
        row2,
        dropDowm1,
        row3,
    ], style={'margin': '0% 30px'}),
])


# 回调函数, 60秒刷新info数据, 即第一列的数值实时刷新
@app.callback(Output('load_info', 'children'), [Input("stream", "n_intervals")])
def load_info(n):
    try:
        df = pd.read_sql('info', con=engine)
        return df.to_json()
    except:
        pass


# 回调函数, 60分钟刷新今日数据, 即第二、三列的数值实时刷新(爬取文章数据, 并写入数据库中)
@app.callback(Output('load_click_data', 'children'), [Input("river", "n_intervals")])
def cwarl_data(n):
    if n != 0:
        df_article = get_blog()
        df_article.to_sql(today, con=engine, if_exists='replace', index=True)


# 回调函数, 第一个柱状图
@app.callback(Output('bar', 'figure'), [Input("river", "n_intervals")])
def get_bar(n):
    df = get_df()
    df_date_month = pd.DataFrame(df['date_month'].value_counts(sort=False))
    df_date_month.sort_index(inplace=True)
    # print(df_date_month)
    date_month_list = df_date_month.index.tolist()  # 将date_month列转换为列表
    count_list = df_date_month['count'].tolist()  # 将count列转换为列表

    print(date_month_list, count_list)
    x = ['Product A', 'Product B', 'Product C']
    y = [20, 14, 23]
    trace = go.Bar(
        x=date_month_list,
        y=count_list,
        text=count_list,
        textposition='auto',
        marker=dict(color=color_scale[:len(date_month_list)])
    )
    layout = go.Layout(
        margin=dict(l=40, r=40, t=10, b=50)
    )
    return go.Figure(data=[trace], layout=layout)


# 回调函数, 中间的饼图
@app.callback(Output('pie', 'figure'), [Input("river", "n_intervals")])
def get_pie(n):
    df = get_catego()
    df_types = pd.DataFrame(df[['categorize', 'column_num']])
    # print("测试pie",df_types)
    trace = go.Pie(
        labels=df_types['categorize'],
        values=df_types['column_num'],
        marker=dict(colors=color_scale[:len(df_types.index)])
    )
    layout = go.Layout(
        margin=dict(l=50, r=50, t=50, b=50),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return go.Figure(data=[trace], layout=layout)


# 回调函数, 左下角热力图
@app.callback(Output('heatmap', 'figure'),
              [Input("dropdown1", "value"), Input('river', 'n_intervals')])
def get_heatmap(value, n):
    df = get_df()
    grouped_by_year = df.groupby('year')
    data = grouped_by_year.get_group(value)
    cross = pd.crosstab(data['weekday'], data['week'])
    cross.sort_index(inplace=True)
    trace = go.Heatmap(
        x=['第{}周'.format(i) for i in cross.columns],
        y=["星期{}".format(i + 1) if i != 6 else "星期日" for i in cross.index],
        z=cross.values,
        colorscale="Blues",
        reversescale=False,
        xgap=4,
        ygap=5,
        showscale=False
    )
    layout = go.Layout(
        margin=dict(l=50, r=40, t=30, b=50),
    )
    return go.Figure(data=[trace], layout=layout)


# 回调函数, 第二个柱状图(柱状图+折线图)
@app.callback(Output('mix', 'figure'), [Input("river", "n_intervals")])
def get_mix(n):
    df = get_catego()
    df_type_visit_sum = pd.DataFrame(df['read_num'].groupby(df['categorize']).sum())
    # df_type_visit_sum = pd.DataFrame(df[['read_num','categorize']])
    df_type_visit_sum = df_type_visit_sum.sort_values(by='read_num', ascending=False).nlargest(15, 'read_num')

    trace1 = go.Bar(
        x=df_type_visit_sum.index,
        y=df_type_visit_sum['read_num'],
        name='总阅读',
        marker=dict(color='#ffc97b'),
        yaxis='y',
    )
    trace2 = go.Scatter(
        x=df_type_visit_sum.index,
        y=df_type_visit_sum.index,
        name='平均阅读',
        yaxis='y2',
        line=dict(color='#161D33')
    )
    layout = go.Layout(
        margin=dict(l=60, r=60, t=30, b=50),
        showlegend=False,
        yaxis=dict(
            side='left',
            title='阅读总数',
            gridcolor='#e2e2e2'
        ),
        yaxis2=dict(
            showgrid=False,  # 网格
            title='阅读平均',
            anchor='x',
            overlaying='y',
            side='right'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return go.Figure(data=[trace1], layout=layout)


# 点击事件, 选择两个下拉选项, 点击对应区域的图表, 文章列表会刷新
@app.callback(Output('click-data', 'children'),
              [Input('pie', 'clickData'),
               Input('bar', 'clickData'),
               Input('mix', 'clickData'),
               Input('heatmap', 'clickData'),
               Input('dropdown1', 'value'),
               Input('dropdown2', 'value'),
               ])
def display_click_data(pie, bar, mix, heatmap, d_value, fig_type):
    try:
        df = get_df()
        if fig_type == 'pie':
            type_value = pie['points'][0]['label']
            # date_month_value = clickdata['points'][0]['x']
            data = df[df['type'] == type_value]
        elif fig_type == 'bar':
            date_month_value = bar['points'][0]['x']
            data = df[df['date_month'] == date_month_value]
        elif fig_type == 'mix':
            type_value = mix['points'][0]['x']
            data = df[df['type'] == type_value]
        else:
            z = heatmap['points'][0]['z']
            if z == 0:
                return None
            else:
                week = heatmap['points'][0]['x'][1:-1]
                weekday = heatmap['points'][0]['y'][-1]
                if weekday == '日':
                    weekday = 7
                year = d_value
                data = df[(df['weekday'] == int(weekday) - 1) & (df['week'] == int(week)) & (df['year'] == year)]
        return get_news_table(data)
    except:
        return None


# 第一列的数值
def update_info(col):
    def get_data(json, n):
        df = pd.read_json(json)
        return df[col][0]

    return get_data


for col in columns:
    app.callback(Output(col, "children"),
                 [Input('load_info', 'children'), Input("stream", "n_intervals")]
                 )(update_info(col))

if __name__ == '__main__':
    # debug模式, 端口7777
    app.run_server(debug=True, threaded=True, port=7777)
    # 正常模式, 网页右下角的调试按钮将不会出现
    # app.run_server(port=7777)
