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
    'PayMode': [  # 支付方式
        'cdim_pay_mode',  # 对应的数据表名
        ['pay_mode_code', 'pay_mode_name'],  # 数据库字段
        ['支付方式编码', '支付方式名称']  # excel表格数据中的表头
    ],

    'payChannel': [  # 支付渠道
        'cdim_pay_channel',  # 对应的数据表名
        ['pay_channel_code', 'pay_channel_name'],  # 数据库字段
        ['支付渠道编码', '支付渠道名称']  # excel表格数据中的表头
    ],

    'Charge': [  # 费用
        '',  # 对应的数据表名
        [],  # 数据库字段
        []  # excel表格数据中的表头
    ],

    'CustDistrict': [  # 定义城市区划
        '',  # 对应的数据表名
        [],  # 数据库字段
        []  # excel表格数据中的表头
    ],

}
