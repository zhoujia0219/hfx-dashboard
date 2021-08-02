# hfx-dashboard

基于Dash+Greenplum的数据看板

## 技术选型

| 技术 | 描述 | 官网 |
|-------|-----|---- |
| Flask| Python Web框架| https://dormousehole.readthedocs.io/en/latest/     |
| Dash| 可视化Web框架| https://dash.plotly.com/                            |
| Plotly| Python数据可视化交互式图形库| https://plotly.com/python/|
| Dash-bootstrap-components | Dash ui布局组件|https://dash-bootstrap-components.opensource.faculty.ai/|
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

### 第一步： 在apps下，按照规则添加页面布局文件(通用组件可直接新增在components下或引入现有的),在services层添加对应的数据处理逻辑文件

> 例如 apps/app_sales_bymonth.py -> services/srv_sales_bymonth.py

### 第二步： 在 routers.py 下 注册访问路由

> 示例

```python

@flask_server.route(URL_SALES_BYMONTH)
def dev_debug():
    """
    仅用于测试
    """
    return flask.redirect('/sales_bymonth')


# 将dash应用绑定到flask
app = DispatcherMiddleware(flask_server, {
    '/sales_bymonth': sales_app.server
})


```
