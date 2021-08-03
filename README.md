# hfx-dashboard

基于Dash+Greenplum的数据看板

## 技术选型

| 技术 | 描述 | 官网 |
|-----|----- |-----|
| Flask| Python Web框架| https://dormousehole.readthedocs.io/en/latest/     |
| Dash| 可视化Web框架| https://dash.plotly.com/                            |
| Plotly| Python数据可视化交互式图形库| https://plotly.com/python/|
| Dash-bootstrap-components | Dash ui布局组件|https://dash-bootstrap-components.opensource.faculty.ai/|
| Flask-Caching| Flask 缓存组件| https://flask-caching.readthedocs.io/en/latest/|
| Redis| 分布式缓存数据库| https://redis.io/|
| Greenplum| 基于PostgreSQL的数据分析仓库| https://greenplum.org/|

## 开发环境

- Python 3.8+
- Redis :
    - 部署服务器：192.168.1.182
- Greenplum :
    - 部署服务器：192.168.1.174
    - 用户名密码：gpadmin/gpadmin

## 项目结构

```
hfx-dashboard
│  .gitignore                             # git忽略文件
│  flask_app.py                           # flask 实例
│  main.py                                # 入口运行文件
│  README.md                              # 项目说明文档
│  requirements.txt                       # 项目依赖
│  routers.py                             # 项目路由定义
│                      
├─apps                                    # dash应用
│  │  __init__.py
│  │  app_sales_bymonth.py                # 门店月度销售分析页面代码
│  │  
│  ├─assets                               # 通用样式定义
│  │      content.css
│  │      siderbar.css
│  │      
│  └─components                           # 通用组件定义
│          __init__.py
│          filter_channels.py
│          filter_city_level.py
│          filter_date_range.py
│          filter_store_age.py
│          filter_store_area.py
│          filter_store_star.py
│          
├─conf                                    # 项目配置
│  │  hfx_dashboard.py                    # 项目核心配置
│  └─ router_conts.py                     # 路由常量定义
├─services                                # 数据处理层
│      srv_comm_dim.py                    # 通用维度
│      srv_sales_bymonth.py               # 门店月度销售数据处理函数定义 
└─utils                                   # 通用工具类
   │  __init__.py
   │  date_util.py                        # 日期处理工具类
   └─ db_util.py                          # 数据库连接处理类


```

## 项目配置

- 主要配置文件： conf/hfx_dashboard.py
    - 主要包含：
        - `greenplum` 数据库连接配置
        - `redis` 连接配置
        - 项目主题配置
        - 其他（后续可能新增）
- 其他配置文件： conf/router_conts.py
    - 主要包含路由路径常量定义

## 项目分层定义：

    - UI视图层 - apps  包含：
        - assets: 通用样式
        - components: 通用组件
        - *.py: 可视化应用代码（只包含页面布局代码）
    - 数据处理层 - services  包含:
        - srv_comm_dim.py : 通用维度定义
        - srv_sales_bymonth.py ： 对应可视化应用代码的数据处理逻辑（数据库sql查询代码,和计算处理逻辑代码都在这个文件中）
    - 通用工具层 - utils  包含：
        - date_util: 常用日期处理函数
        - db_util: 数据库连接工具

## 项目规范

### 文件命名规则：

1. 每一个dash.Dash()方法创建的server称之为一个app，其命名方法为: 模块+页面名称.
   > 如 sales_bymonth 表示：销售分析模块的月度分析页面

2. 每一个app的文件命名为：[ app_ ] + [app名称].
   > 如 app_sales_bymonth.py

3. 每一个app对应于一个 URL 路径（不含基地址)，其 URL 路径为 [模块名] + / + [页面名].
   > 如, 月度销售分析页面的地址为 http://host:port/sales/bymonth

4. 每一个app对应于一个service文件，service文件命名为 [ srv_ ] + [app名称]
   > 如, 月度销售分析页面对于的service文件为 srv_sales_bymonth.py

### 变量命名规则

1. 每一个组件的Id命名规则为: [组件名称/简称_]+[组件作用]，取名尽量见名知意。
   > 如 筛选组件的渠道组件， f_channel  f: filter 表示筛选组件， channel 是渠道的意思

2. 每一个图形的ID命名规则为：[graph_]+[图形作用]
   > 如 排名图： graph_top

3. 每一个图形上的筛选组件命名规则为：[图形作用_]+[choices_]+[筛选作用]
   > 如 排名图上的月份筛选： top_choices_month

4. 回调函数命名规则为： [update_] + [图形作用_] + [graph]
   > 如 更新排名图的回调方法： update_top_graph

### 注释规范

1. 每一个函数方法, 必须要有方法说明、方法参数、方法返回值都必须有说明，并且需要规定返回值类型(页面组件元素除外)

> 示例：
   ```python
        def calculate_cards(filter_values: dict) -> Dict:
            """
            计算头部的4个card 的数据
            :param filter_values :
                        { 'begin_month': 开始时间: 字符串类型，格式 YYYY-MM,
                          'end_month': 结束时间: 字符串类型，格式 YYYY-MM,
                          'city_level': 城市级别: List类型,
                          'channel': 渠道: List类型,
                          'store_age': 店龄: List类型 ,
                          'store_area': 门店面积: List类型,
                          'store_star': 门店星级: List类型}
            :return dict :
                    {"total_sale": 总销售量: 浮点类型，单位百万(M),
                    "last_month_total": 上月销售量：浮点类型，单位百万(M),
                    "tb_percentage": 同比百分比（上月的数据比去年的数据）：字符串类型，单位%,
                    "hb_percentage": 环比百分比（上月的数据比上上月的数据）：字符串类型，单位%,
                    "c_month_total_sale": 本月总销售量：浮点类型，单位百万(M),
                    "m_growth_rate": 增长率（本月比上月）：字符串类型，单位%,
                    "group_sales": 12个月的销售趋势：Dataframe类型，包含字段[month_group:月份, dealtotal:当月销量]}
            """
            # ...省略计算处理逻辑
            # 返回示例
            return {"total_sale": 15.00,
                    "last_month_total": 12.00,
                    "tb_percentage": '10.00%',
                    "hb_percentage": '-2.00%',
                    "c_month_total_sale": 15.00,
                    "m_growth_rate": '25%',
                    "group_sales": []}
        
   ```

## 项目部署运行

### 本地运行

- 下载依赖包

```shell
pip install -r requirements.txt
```

- 运行
    - 在Windows 直接使用ide工具找到main.py 鼠标右键运行即可

    - Linux上,使用Gunicorn或其他方式（参考flask官网） 部署运行

## 开发新dash_app步骤

### 第一步： 在apps下，按照规则添加页面布局文件(通用组件可直接新增在components下或引入现有的)

- 例如 apps/app_sales_bymonth.py
    - 主要包含代码说明： dash实例化 、初始值变量及数据、默认页面布局构建函数、页面布局代码、回调函数

### 第二步：在services下，添加对应的数据处理逻辑文件

- 例如 services/srv_sales_bymonth.py
    - 主要包含代码说明：全局缓存处理函数、数据计算处理函数、数据库连接查询函数

### 第三步： 页面功能与数据处理联调

### 第四步： 在 routers.py 下 注册访问路由

- 示例

```python

@flask_server.route(URL_SALES_BYMONTH)
def sales_bymonth():
    """
    仅用于测试
    """
    return flask.redirect('/sales_bymonth')


# 将dash应用绑定到flask
app = DispatcherMiddleware(flask_server, {
    '/sales_bymonth': sales_app.server
})


```

## 使用数据库取数

由于数据库使用的是greenplum,greenplumn 又是基于postgresql的，所以连接驱动和postgresql连接驱动一致，都是使用`psycopg2`
连接示例参考 utils/db_util:

```python
import logging

import psycopg2
import psycopg2.extensions
import psycopg2.extras
import psycopg2.pool

from conf import hfx_dashboard

logging.getLogger(__name__)


class LoggingCursor(psycopg2.extensions.cursor):
    def execute(self, sql, args=None):
        logger = logging.getLogger('sql_debug')
        logger.info(self.mogrify(sql, args))

        try:
            psycopg2.extensions.cursor.execute(self, sql, args)
        except Exception as exc:
            logger.error("%s: %s" % (exc.__class__.__name__, exc))
            raise


def gp_connect(dbname: str):
    try:
        conn_pool = psycopg2.pool.SimpleConnectionPool(minconn=1, maxconn=5,
                                                       # 默认db 
                                                       dbname="",
                                                       # 用户名
                                                       user=hfx_dashboard.USERNAME,
                                                       # 密码
                                                       password=hfx_dashboard.PASSWORD,
                                                       # 服务器地址
                                                       host=hfx_dashboard.HOST,
                                                       # 服务器端口
                                                       port=hfx_dashboard.PORT)
        # 从数据库连接池获取连接
        conn = conn_pool.getconn()
        return conn
    except psycopg2.DatabaseError as e:
        print("could not connect to Greenplum server", e)


# 查询数据
def query_list(sql: str, dbname: str):
    """
    查询列表
    :param sql: 要执行的sql
    :param dbname:  默认的schema 
    :return:
    """
    conn = gp_connect(dbname=dbname)
    cur = conn.cursor(cursor_factory=LoggingCursor)
    try:
        cur.execute(sql)
        return cur.fetchall()
    except Exception as e:
        logging.error("查询异常：{}, sql {}", str(e), sql)
        raise e
    finally:
        conn.close()

```

根据上面的封装工具，测试一个查询（目前暂时只封装了查询方法）：

```python
from utils import db_util

# 查询渠道列表
channel_list = db_util.query_list(""" 
                select distinct businessname 
                from  chunbaiwei.fact_storesale_weather
                """, "data_analysis")

print(channel_list)

```

> 结果：[('开放平台-扫码点餐',), ('到店销售',), ('开放平台-淳乐送',), ('堂食销售',), ('网络销售',)]

根据上面查询的结果，转换一下格式：

```python

channels = [{"channel": d[0]} for d in channel_list]

print(channels)
```

> 执行结果: [{'channel': '开放平台-扫码点餐'}, {'channel': '到店销售'}, {'channel': '开放平台-淳乐送'}, {'channel': '堂食销售'}, {'channel': '网络销售'}]

## 缓存使用

根据dash官方文档推荐，使用Flask-Caching + Redis来进行缓存，缓存的数据通过一个函数访问，该函数的输出由其输入参数缓存和键控 缓存使用示例：

- 第一步：首先需要进行配置
  > 配置内容位置在 flask_app.py 中
    ```python
    import flask
    from flask_caching import Cache
    
    from conf import hfx_dashboard
    
    #########################
    # flask
    #########################
    flask_server = flask.Flask(__name__)
    
    #########################
    # 缓存
    #########################
    
    cache = Cache()
    CACHE_CONFIG = {
        # try 'filesystem' if you don't want to setup redis
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_URL': hfx_dashboard.REDIS_URL,
        'CACHE_DEFAULT_TIMEOUT': hfx_dashboard.REDIS_CACHE_DEFAULT_TIMEOUT
    }
    cache.init_app(flask_server, config=CACHE_CONFIG)
    
    ```
  > 如果是纯dash应用，则配置如下
    ```python
        import dash
        import dash_bootstrap_components as dbc
        import dash_html_components as html
        from flask_caching import Cache
        
        from conf import hfx_dashboard
        
        #########################
        # dash
        #########################
        app = dash.Dash(__name__, external_stylesheets=hfx_dashboard.BOOTSTRAP_THEME)
        server = app.server
        
        #########################
        # 缓存
        #########################
        
        cache = Cache()
        CACHE_CONFIG = {
            # try 'filesystem' if you don't want to setup redis
            'CACHE_TYPE': 'redis',
            'CACHE_REDIS_URL': hfx_dashboard.REDIS_URL,
            'CACHE_DEFAULT_TIMEOUT': hfx_dashboard.REDIS_CACHE_DEFAULT_TIMEOUT
        }
        cache.init_app(server, config=CACHE_CONFIG)
    ```

- 第二步：使用dcc.Store添加触发回调的信号
  > 内容位置在 apps/app_sales_bymonth.py
    ```python
        import dash
        import dash_core_components as dcc
        import dash_html_components as html
        from flask_app import flask_server
        from conf.hfx_dashboard import BOOTSTRAP_THEME
        from conf.router_conts import URL_SALES_BYMONTH
        ###############
        # dash
        ###############
        
        sales_app = dash.Dash(__name__,
                              server=flask_server,
                              title="门店月度销售分析",
                              update_title="数据载入中...",
                              suppress_callback_exceptions=True,
                              url_base_pathname=URL_SALES_BYMONTH,
                              external_stylesheets=[BOOTSTRAP_THEME])
        # 侧边栏和内容省略，具体参看apps/app_sales_bymonth.py
        sidebar = html.Div()
        content = html.Div()
        
        sales_app.layout = html.Div([
            sidebar,
            content,
            # signal value to trigger callbacks
            dcc.Store(id='signal')
        ])
    ```


- 第三步： 将触发取数的值缓存到dcc.Store, 并以此触发缓存方法和其他的回调计算
  > 代码位置： apps/app_sales_bymonth.py
  > 在此方法中，Input参数会动态实时的调用此回调方法，State表示只取值，不触发回调。
  > 此函数表示点击提交按钮后，根据所有筛选值作为dcc.Store的值，会触发其他回调方法的计算
    ```python
    @sales_app.callback(
        Output('signal', 'data'),
        [
            Input("f_submit", "n_clicks"),
            # 日期筛选
            State('f_begin_month', 'value'),
            State('f_end_month', 'value'),
            # 城市筛选
            State('f_cities', 'value'),
            # 渠道筛选
            State('f_channels', 'value'),
            # 店龄筛选
            State('f_store_age', 'value'),
            # 门店面积筛选
            State('f_store_area', 'value'),
            # 门店星级筛选
            State('f_store_star', 'value'),
        ]
    )
    def compute_value(n_clicks, begin_month, end_month, city_level, channel, store_age, store_area, store_star):
        """
        点击提交按钮后，保存筛选值到signal
        :param n_clicks 提交按钮点击次数
        :param begin_month 结束日期
        :param end_month 开始日期
        :param city_level  城市级别
        :param channel 渠道
        :param store_age 店龄
        :param store_area 店面积
        :param store_star 门店星级
        :return 返回筛选的所有选中值（用于取缓存）
    
        """
        filter_values = {'begin_month': begin_month, 'end_month': end_month,
                         'city_level': city_level, 'channel': channel,
                         'store_age': store_age, 'store_area': store_area, 'store_star': store_star}
        # compute value and send a signal when done
        srv_sales_bymonth.global_store(filter_values)
        return filter_values
    ```

- 第四步： 添加全局缓存方法
  > 具体内容位置在 services/srv_sales_bymonth.py.
  > 根据dcc.Store的值, 从数据库或者从缓存中取得计算数据
    ```python
    from flask_app import cache
    from utils import db_util
    from typing import List, Dict
    @cache.memoize()
    def global_store(filter_values: dict) -> List[Dict]:
        """
        全局缓存
        @:param filter_values: 筛选值 json类型参数 { 'begin_month': begin_month, 'end_month': end_month,
                                    'city_level':city_level, 'channel':channel,
                                    'store_age':store_age, 'store_area':store_area, 'store_star':store_star}
        @:return:
        """
        d = cache.get(str(filter_values))
        if d:
            return d
        else:
            # 取数据库的值
            result = find_sales_list(filter_values)
            if result:
                cache.set(str(filter_values), result)
            return result
    
    ```

## 回调函数取数

根据上面的dcc.Store的值作为输入参数，取出缓存的计算数据，然后输出card_data的内容。
> 具体内容位置： apps/app_sales_bymonth.py

```python

def build_layout_title_cards(filter_values: dict):
    """
    头部卡片
    :param filter_values: 筛选值
    :return 卡片内容
    """
    # 封装结果数据
    datas = srv_sales_bymonth.calculate_cards(filter_values)

    total_sale = datas["total_sale"] if datas else '0'
    begin_month = filter_values["begin_month"] if filter_values else ''
    end_month = filter_values["end_month"] if filter_values else ''
    last_month_total = datas["last_month_total"] if datas else '0'

    tb_percentage = datas["tb_percentage"] if datas else '0'
    hb_percentage = datas["hb_percentage"] if datas else '0'
    c_month_total_sale = datas["c_month_total_sale"] if datas else '0'
    m_growth_rate = datas["m_growth_rate"] if datas else '0'
    group_sales = datas["group_sales"] if datas else []
    fig = build_group_sales_fig(group_sales) if len(group_sales) > 0 else {}

    return [
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("总销售额"),
            html.H4(['￥', total_sale, 'M'], id='title_1', style={"color": "darkred"}),
            html.Label(begin_month + " - " + end_month),
        ]), className='title-card'), className='title-col mr-2'),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("上月销售额"),
            html.H4(['￥', last_month_total, 'M'], id='title_2', style={"color": "darkred"}),
            html.Label("同比:" + tb_percentage + "  环比：" + hb_percentage),
        ]), className='title-card'), className='title-col mr-2'),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6(["本月销售额", "(", end_month, ")"]),
            html.H4(['￥', c_month_total_sale, 'M'], id='title_3', style={"color": "darkred"}),
            html.Label("增长率：" + m_growth_rate),
        ]), className='title-card'), className='title-col mr-2'),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6(["近12月销售趋势", "(", begin_month + " - " + end_month, ")"]),
            dcc.Graph(id='title_4', figure=fig, style={"height": "60px"}),
        ]), className='title-card'), className='title-col col-5', style={'paddingRight': 15}),
    ]


# 顶部 12月趋势图
def build_group_sales_fig(df: DataFrame):
    """
    12个月销售趋势图
    :param df: 包含月份和销售额的dataframe 数据
    :return 返回图形
    """
    fig = px.bar(df, x="month_group", y="dealtotal", width=200, height=60)
    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        margin=dict(t=10, l=10, b=10, r=10)
    )
    return fig


@sales_app.callback(Output('card_data', 'children'), Input('signal', 'data'))
def update_card_data(filter_values):
    """
    更新card数值
    :param filter_values: 筛选值
    :return  返回顶部的card
    """
    return build_layout_title_cards(filter_values)


```

> 回调数据的计算逻辑： services/srv_sales_bymonth.py

```python

def calculate_cards(filter_values: dict) -> Dict:
    """
    计算头部的4个card 的数据
    :param filter_values :
                    { 'begin_month': 开始时间: 字符串类型，格式 YYYY-MM,
                      'end_month': 结束时间: 字符串类型，格式 YYYY-MM,
                      'city_level': 城市级别: List类型,
                      'channel': 渠道: List类型,
                      'store_age': 店龄: List类型 ,
                      'store_area': 门店面积: List类型,
                      'store_star': 门店星级: List类型}
    :return dict :
            {"total_sale": 总销售量: 浮点类型，单位百万(M),
            "last_month_total": 上月销售量：浮点类型，单位百万(M),
            "tb_percentage": 同比百分比（上月的数据比去年的数据）：字符串类型，单位%,
            "hb_percentage": 环比百分比（上月的数据比上上月的数据）：字符串类型，单位%,
            "c_month_total_sale": 本月总销售量：浮点类型，单位百万(M),
            "m_growth_rate": 增长率（本月比上月）：字符串类型，单位%,
            "group_sales": 12个月的销售趋势：Dataframe类型，包含字段[month_group:月份, dealtotal:当月销量]}
    """
    card_datas = global_store(filter_values)
    df = pd.DataFrame(card_datas)

    # 总营业额
    total_sale = round((df["dealtotal"].sum() / trans_num), 2) if len(df) > 0 else 0.00
    # 当前月份(以时间筛选的截止日期为准)的上月数据
    ve_date = datetime.strptime(filter_values["end_month"], "%Y-%m")
    s_date = date_util.get_last_month_first_day(ve_date).date()
    e_date = date_util.get_last_month_last_day(ve_date).date()
    last_month_df = df[(df["rdate"] >= s_date) & (df["rdate"] < e_date)] if len(df) > 0 else []
    last_month_total = round((last_month_df["dealtotal"].sum()) / trans_num, 2) if len(last_month_df) > 0 else 0.00

    # 同比 取去年当月数据
    tb_sdate = (s_date - relativedelta(years=1))
    tb_edate = (e_date - relativedelta(years=1))
    # 去年的数据
    tb_df = df[(df["rdate"] >= tb_sdate) & (df["rdate"] < tb_edate)] if len(df) > 0 else []
    # 去年的总营业额
    tb_total_sale = round((tb_df["dealtotal"].sum() / trans_num), 2) if len(tb_df) > 0 else 0.00

    # 同比增长率计算 =（本期数－同期数）/同期数×100%
    tb_percentage = "%.2f%%" % round(
        ((last_month_total - tb_total_sale) / tb_total_sale * 100) if tb_total_sale > 0 else 0, 2)

    # 环比 取上月数据
    hb_sdate = date_util.get_last_month_first_day(s_date).date()
    hb_edate = date_util.get_last_month_last_day(e_date).date()

    # 上月数据
    hb_df = df[(df["rdate"] >= hb_sdate) & (df["rdate"] < hb_edate)] if len(df) > 0 else []
    # 上月总营业额
    hb_total_sale = round((hb_df["dealtotal"].sum() / trans_num), 2) if len(hb_df) > 0 else 0.00

    # 环比增长率计算= （本期数-上期数）/上期数×100%。
    hb_percentage = "%.2f%%" % round(
        ((last_month_total - hb_total_sale) / hb_total_sale * 100) if hb_total_sale > 0 else 0, 2)
    # 本月销售额
    c_sdate = date_util.get_month_first_day(ve_date).date()
    c_edate = date_util.get_month_last_day(ve_date).date()
    c_month_df = df[(df["rdate"] >= c_sdate) & (df["rdate"] < c_edate)] if len(df) > 0 else []
    c_month_total_sale = round((c_month_df["dealtotal"].sum() / trans_num), 2) if len(c_month_df) > 0 else 0.00

    # 本月营业额与上月对比营业额 增长率 - 月增长率 =（本月营业额-上月营业额）/上月营业额*100%
    m_growth_rate = "%.2f%%" % round(
        ((c_month_total_sale - last_month_total) / last_month_total * 100) if last_month_total > 0 else 0, 2)

    # 近12月销售趋势
    group_df = df
    month_groups = group_df.groupby(by=["month_group"], as_index=False)["dealtotal"].sum() if len(group_df) > 0 else []
    group_sales = pd.DataFrame(month_groups)
    # 封装结果数据
    return {"total_sale": total_sale, "last_month_total": last_month_total,
            "tb_percentage": tb_percentage, "hb_percentage": hb_percentage,
            "c_month_total_sale": c_month_total_sale, "m_growth_rate": m_growth_rate,
            "group_sales": group_sales}

```