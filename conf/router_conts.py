#
# 此文件用以配置 URL 路径和 Dash 应用的对应关系
#
# 文件命名规则：
# 1. 每一个dash.Dash()方法创建的server称之为一个app，其命名方法为: 模块+页面名称，如 sales_bymonth 表示：销售分析模块的月度分析页面
# 2. 每一个app的文件命名为：[ app_ ] + [app名称], 如 app_sales_bymonth.py
# 3. 每一个app对应于一个 URL 路径（不含基地址)，其 URL 路径为 [模块名] + / + [页面名].
#   如, 月度销售分析页面的地址为 http://host:port/sales/bymonth
# 4. 每一个app对应于一个service文件，service文件命名为 [ srv_ ] + [app名称]
#   如, 月度销售分析页面对于的service文件为 srv_sales_bymonth.py


# 门店月度销售分析
URL_SALES_BYMONTH = "/sales/bymonth/"
# 实时销售页面
URL_REAL_TIME_SALE = "/real_time/"
# 巡检看板页面
URL_STORE_INSPECTION = "/store_inspection/"
# 自检
URL_SELF_CHECKING = "/self/checking/"
