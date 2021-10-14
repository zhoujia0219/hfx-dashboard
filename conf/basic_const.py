# 开发中的一些基本常量
from pyparsing import basestring

WHITE_URL_LIST = [
    '/login'
]  # 路由白名单

REAL_TIME_SALA_ANALYZE_INTERVAL_TIME = 30 * 1000  # 销售分析图形定时器的刷新时间， 3*1000=3秒
REAL_TIME_TOTAL_SALE_INTERVAL_TIME = 30 * 1000  # 实时页面左侧销售总额的刷新时间， 3*1000=3秒

# 数据导出导入的表名和字段名
EXPORT_LOAD_TABLENAME_FIELD = {
    "fyjh": ["data_transfer",  # 对应的数据表名
             ['column_1', 'column_2', 'column_3', 'column_4', 'column_5', 'column_6', 'column_7', 'column_8'],  # 数据库字段
             [int, int, int, basestring, int, int, basestring, int],  # 对应每个字段的python类型
             ['整数', '整数', '整数', '字符串', '整数', '整数', '字符串', '整数'],  # 类型的中文
             ["字段1", '字段2', '字段3', '字段4', '字段5', '字段6', '字段7', '字段8']  # excel表格数据中的表头
             ]
}
