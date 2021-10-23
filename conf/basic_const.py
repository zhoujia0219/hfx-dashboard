# 开发中的一些基本常量
from pyparsing import basestring

WHITE_URL_LIST = [
    '/login',
    '/verify_code/'
]  # 路由白名单

REAL_TIME_SALA_ANALYZE_INTERVAL_TIME = 30 * 1000  # 销售分析图形定时器的刷新时间， 3*1000=3秒
REAL_TIME_TOTAL_SALE_INTERVAL_TIME = 30 * 1000  # 实时页面左侧销售总额的刷新时间， 3*1000=3秒

# 数据导出导入的表名和字段名
IMPORT_EXPORT_TABLENAME_FIELD = {  # 导入和导出的数据配置
    "fyjh": [
        "data_transfer",  # 对应的数据表名
        ['column_1', 'column_2', 'column_3', 'column_4', 'column_5', 'column_6', 'column_7', 'column_8'],  # 数据库字段
        ["字段1", '字段2', '字段3', '字段4', '字段5', '字段6', '字段7', '字段8']  # excel表格数据中的表头
    ],
    'brand': [
        'pdim_brand',  # 对应的数据表名
        ['brand_code', 'std_brand_code', 'db_schema', 'brand_name', 'trade_code', 'company_code', 'version_time'],
        ["品牌编码", '标准品牌编码（随主数据）', '数据库或schema名称', '品牌名称', '行业编码', '公司编码', '版本编码']  # excel表格数据中的表头
    ]
}
