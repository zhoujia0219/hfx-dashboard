import pandas as pd

yesterday_area_sale_ = {
    "area1": ["一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区",
              "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区",
              "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区",
              "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区",
              "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区",
              "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区",
              ],
    "area2": ["一战区一片区", "一战区一片区", "一战区一片区", "一战区一片区", "一战区一片区", "一战区一片区", "一战区一片区", "一战区一片区", "一战区一片区",
              "一战区一片区", "一战区一片区", "一战区一片区", "一战区一片区", '二战区一片区', '二战区一片区', '二战区一片区', '二战区一片区', '二战区一片区', '二战区一片区',
              '二战区一片区', '二战区一片区', '二战区一片区', '二战区一片区', '二战区一片区', '二战区一片区', '二战区一片区',

              '二战区二片区', '二战区二片区', '二战区二片区', '二战区二片区', '二战区二片区', '二战区二片区',
              '二战区二片区', '二战区二片区', '二战区二片区', '二战区二片区', '二战区二片区', '二战区二片区', '二战区二片区',
              '二战区三片区', '二战区三片区', '二战区三片区', '二战区三片区', '二战区三片区', '二战区三片区',
              '二战区三片区', '二战区三片区', '二战区三片区', '二战区三片区', '二战区三片区', '二战区三片区', '二战区三片区',
              '二战区四片区', '二战区四片区', '二战区四片区', '二战区四片区', '二战区四片区', '二战区四片区',
              '二战区四片区', '二战区四片区', '二战区四片区', '二战区四片区', '二战区四片区', '二战区四片区', '二战区四片区',
              '二战区五片区', '二战区五片区', '二战区五片区', '二战区五片区', '二战区五片区', '二战区五片区',
              '二战区五片区', '二战区五片区', '二战区五片区', '二战区五片区', '二战区五片区', '二战区五片区', '二战区五片区',
              ],
    'dealtotal': [11, 20, 13, 11, 11, 23, 36, 11, 63, 11, 11, 52, 11,
                  66, 43, 43, 15, 14, 43, 43, 43, 28, 43, 43, 35, 26,
                  66, 43, 43, 15, 14, 43, 43, 43, 28, 43, 43, 35, 26,
                  66, 43, 43, 15, 14, 43, 43, 43, 28, 43, 43, 35, 26,
                  66, 43, 43, 15, 14, 43, 43, 43, 28, 43, 43, 35, 26,
                  66, 43, 43, 15, 14, 43, 43, 43, 28, 43, 43, 35, 26,
                  ],
    'times': [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
              12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
              12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
              12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
              12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
              12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
              ],
    'rdate': ['2021-03-20', '2021-03-20',
              '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20',
              '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20',
              '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20',
              '2021-03-20', '2021-03-20', '2021-03-20',

              '2021-03-20', '2021-03-20', '2021-03-20',
              '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20',
              '2021-03-20', '2021-03-20', '2021-03-20',
              '2021-03-20', '2021-03-20', '2021-03-20',
              '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20',
              '2021-03-20', '2021-03-20', '2021-03-20',
              '2021-03-20', '2021-03-20', '2021-03-20',
              '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20',
              '2021-03-20', '2021-03-20', '2021-03-20',
              '2021-03-20', '2021-03-20', '2021-03-20',
              '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20',
              '2021-03-20', '2021-03-20', '2021-03-20',
              ]
}

today_area_sale_ = {
    "area1": ["一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "二战区", "二战区", "二战区", "二战区",
              "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区",

              "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区",
              "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区",
              "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区",
              "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", ],

    "area2": ["一战区一片区", "一战区一片区", "一战区一片区", "一战区一片区", "一战区一片区", "一战区一片区", "一战区一片区", "一战区一片区", "一战区一片区", "一战区一片区",
              "一战区一片区",
              '二战区一片区', '二战区一片区', '二战区一片区', '二战区一片区', '二战区一片区', '二战区一片区', '二战区一片区', '二战区一片区', '二战区一片区', '二战区一片区',
              '二战区一片区',
              '二战区二片区', '二战区二片区', '二战区二片区', '二战区二片区', '二战区二片区', '二战区二片区', '二战区二片区', '二战区二片区', '二战区二片区', '二战区二片区',
              '二战区二片区',
              '二战区三片区', '二战区三片区', '二战区三片区', '二战区三片区', '二战区三片区', '二战区三片区',
              '二战区三片区', '二战区三片区', '二战区三片区', '二战区三片区', '二战区三片区',
              '二战区四片区', '二战区四片区', '二战区四片区', '二战区四片区', '二战区四片区', '二战区四片区',
              '二战区四片区', '二战区四片区', '二战区四片区', '二战区四片区', '二战区四片区',
              '二战区五片区', '二战区五片区', '二战区五片区', '二战区五片区', '二战区五片区', '二战区五片区',
              '二战区五片区', '二战区五片区', '二战区五片区', '二战区五片区', '二战区五片区',
              ],
    'dealtotal': [1, 44, 22, 29, 31, 11, 47, 53, 84, 11, 15,
                  2, 43, 25, 8, 43, 14, 43, 25, 18, 5, 10,
                  2, 43, 25, 8, 43, 14, 43, 25, 18, 5, 10,
                  2, 43, 25, 8, 43, 14, 43, 25, 18, 5, 10,
                  2, 43, 25, 8, 43, 14, 43, 25, 18, 5, 10,
                  2, 43, 25, 8, 43, 14, 43, 25, 18, 5, 10,
                  ],
    'times': [1, 4, 3, 2, 5, 6, 7, 8, 9, 10, 11,
              1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
              1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
              1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
              1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
              1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
              ],
    'rdate': ["2021-03-21", "2021-03-21",
              "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21",
              "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21",
              "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21",
              "2021-03-21", "2021-03-21",
              "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21",
              "2021-03-21", "2021-03-21",
              "2021-03-21", "2021-03-21",
              "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21",
              "2021-03-21", "2021-03-21",
              "2021-03-21", "2021-03-21",
              "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21",
              "2021-03-21", "2021-03-21",
              "2021-03-21", "2021-03-21",
              "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21",
              "2021-03-21", "2021-03-21",
              ]
}

# 饼图的模拟数据
pie_key_category_sale_pie_today = {
    "category_name": [
        "饼干", "混沌", "饺子", "面食", "水产品", "冻肉", "鲜奶", "酸奶", "熟食", "方便面", "八宝粥", "咖啡", "茶", "蜜饯果脯", "干海产品"
    ],
    "dealtotal": [12, 23, 34, 45, 56, 67, 78, 89, 90, 122, 111, 131, 32, 63, 72]
}
pie_key_category_sale_pie_yesterday = {
    "category_name": [
        "饼干", "混沌", "饺子", "面食", "水产品", "冻肉", "鲜奶", "酸奶", "熟食", "方便面", "八宝粥", "咖啡", "茶", "蜜饯果脯", "干海产品"
    ],
    "dealtotal": [18, 15, 34, 36, 55, 72, 70, 80, 90, 110, 122, 98, 69, 36, 59]
}

# 区域销售排名横向对比条形图 今天
area_sale_rank_bar_today = {
    'area1': ['一战区', "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区",
              '二战区', "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区",
              '三战区', "三战区", "三战区", "三战区", "三战区", "三战区", "三战区", "三战区", "三战区", "三战区", "三战区", "三战区", "三战区", "三战区", "三战区",
              '四战区', "四战区", "四战区", "四战区", "四战区", "四战区", "四战区", "四战区", "四战区", "四战区", "四战区", "四战区", "四战区", "四战区", "四战区",
              '五战区', "五战区", "五战区", "五战区", "五战区", "五战区", "五战区", "五战区", "五战区", "五战区", "五战区", "五战区", "五战区", "五战区", "五战区",
              '六战区', "六战区", "六战区", "六战区", "六战区", "六战区", "六战区", "六战区", "六战区", "六战区", "六战区", "六战区", "六战区", "六战区", "六战区",
              '七战区', "七战区", "七战区", "七战区", "七战区", "七战区", "七战区", "七战区", "七战区", "七战区", "七战区", "七战区", "七战区", "七战区", "七战区",
              '八战区', "八战区", "八战区", "八战区", "八战区", "八战区", "八战区", "八战区", "八战区", "八战区", "八战区", "八战区", "八战区", "八战区", "八战区",
              '九战区', "九战区", "九战区", "九战区", "九战区", "九战区", "九战区", "九战区", "九战区", "九战区", "九战区", "九战区", "九战区", "九战区", "九战区",
              '十战区', "十战区", "十战区", "十战区", "十战区", "十战区", "十战区", "十战区", "十战区", "十战区", "十战区", "十战区", "十战区", "十战区", "十战区",
              '十一战区', "十一战区", "十一战区", "十一战区", "十一战区", "十一战区", "十一战区", "十一战区", "十一战区", "十一战区", "十一战区", "十一战区", "十一战区",
              "十一战区", "十一战区",
              # '十二战区', "十二战区", "十二战区", "十二战区", "十二战区", "十二战区", "十二战区", "十二战区", "十二战区", "十二战区", "十二战区", "十二战区", "十二战区",
              # "十二战区", "十二战区",
              # '十三战区', "十三战区", "十三战区", "十三战区", "十三战区", "十三战区", "十三战区", "十三战区", "十三战区", "十三战区", "十三战区", "十三战区", "十三战区",
              # "十三战区", "十三战区",
              # '十四战区', "十四战区", "十四战区", "十四战区", "十四战区", "十四战区", "十四战区", "十四战区", "十四战区", "十四战区", "十四战区", "十四战区", "十四战区",
              # "十四战区", "十四战区",
              # '十五战区', "十五战区", "十五战区", "十五战区", "十五战区", "十五战区", "十五战区", "十五战区", "十五战区", "十五战区", "十五战区", "十五战区", "十五战区",
              # "十五战区", "十五战区",
              ],
    'area2': ['一战区一片区', '一战区二片区', '一战区三片区', '一战区四片区', '一战区五片区', '一战区六片区', '一战区七片区', '一战区八片区', '一战区九片区', '一战区十片区',
              '一战区十一片区', '一战区十二片区', '一战区十三片区', '一战区十四片区', '一战区一十五片区',
              '二战区一片区', '二战区二片区', '二战区三片区', '二战区四片区', '二战区五片区', '二战区六片区', '二战区七片区', '二战区八片区', '二战区九片区', '二战区十片区',
              '二战区十一片区', '二战区十二片区', '二战区十三片区', '二战区十四片区', '二战区一十五片区',
              '三战区一片区', '三战区二片区', '三战区三片区', '三战区四片区', '三战区五片区', '三战区六片区', '三战区七片区', '三战区八片区', '三战区九片区', '三战区十片区',
              '三战区十一片区', '三战区十二片区', '三战区十三片区', '三战区十四片区', '三战区一十五片区',
              '四战区一片区', '四战区二片区', '四战区三片区', '四战区四片区', '四战区五片区', '四战区六片区', '四战区七片区', '四战区八片区', '四战区九片区', '四战区十片区',
              '四战区十一片区', '四战区十二片区', '四战区十三片区', '四战区十四片区', '四战区一十五片区',
              '五战区一片区', '五战区二片区', '五战区三片区', '五战区四片区', '五战区五片区', '五战区六片区', '五战区七片区', '五战区八片区', '五战区九片区', '五战区十片区',
              '五战区十一片区', '五战区十二片区', '五战区十三片区', '五战区十四片区', '五战区一十五片区',
              '六战区一片区', '六战区二片区', '六战区三片区', '六战区四片区', '六战区五片区', '六战区六片区', '六战区七片区', '六战区八片区', '六战区九片区', '六战区十片区',
              '六战区十一片区', '六战区十二片区', '六战区十三片区', '六战区十四片区', '六战区一十五片区',
              '七战区一片区', '七战区二片区', '七战区三片区', '七战区四片区', '七战区五片区', '七战区六片区', '七战区七片区', '七战区八片区', '七战区九片区', '七战区十片区',
              '七战区十一片区', '七战区十二片区', '七战区十三片区', '七战区十四片区', '七战区一十五片区',
              '八战区一片区', '八战区二片区', '八战区三片区', '八战区四片区', '八战区五片区', '八战区六片区', '八战区七片区', '八战区八片区', '八战区九片区', '八战区十片区',
              '八战区十一片区', '八战区十二片区', '八战区十三片区', '八战区十四片区', '八战区一十五片区',
              '九战区一片区', '九战区二片区', '九战区三片区', '九战区四片区', '九战区五片区', '九战区六片区', '九战区七片区', '九战区八片区', '九战区九片区', '九战区十片区',
              '九战区十一片区', '九战区十二片区', '九战区十三片区', '九战区十四片区', '九战区一十五片区',
              '十战区一片区', '十战区二片区', '十战区三片区', '十战区四片区', '十战区五片区', '十战区六片区', '十战区七片区', '十战区八片区', '十战区九片区', '十战区十片区',
              '十战区十一片区', '十战区十二片区', '十战区十三片区', '十战区十四片区', '十战区一十五片区',
              '十一战区一片区', '十一战区二片区', '十一战区三片区', '十一战区四片区', '十一战区五片区', '十一战区六片区', '十一战区七片区', '十一战区八片区', '十一战区九片区',
              '十一战区十片区', '十一战区十一片区', '十一战区十二片区', '十一战区十三片区', '十一战区十四片区', '十一战区一十五片区',
              # '十二战区一片区', '十二战区二片区', '十二战区三片区', '十二战区四片区', '十二战区五片区', '十二战区六片区', '十二战区七片区', '十二战区八片区', '十二战区九片区',
              # '十二战区十片区', '十二战区十一片区', '十二战区十二片区', '十二战区十三片区', '十二战区十四片区', '十二战区一十五片区',
              # '十三战区一片区', '十三战区二片区', '十三战区三片区', '十三战区四片区', '十三战区五片区', '十三战区六片区', '十三战区七片区', '十三战区八片区', '十三战区九片区',
              # '十三战区十片区', '十三战区十一片区', '十三战区十二片区', '十三战区十三片区', '十三战区十四片区', '十三战区一十五片区',
              # '十四战区一片区', '十四战区二片区', '十四战区三片区', '十四战区四片区', '十四战区五片区', '十四战区六片区', '十四战区七片区', '十四战区八片区', '十四战区九片区',
              # '十四战区十片区', '十四战区十一片区', '十四战区十二片区', '十四战区十三片区', '十四战区十四片区', '十四战区一十五片区',
              # '十五战区一片区', '十五战区二片区', '十五战区三片区', '十五战区四片区', '十五战区五片区', '十五战区六片区', '十五战区七片区', '十五战区八片区', '十五战区九片区',
              # '十五战区十片区', '十五战区十一片区', '十五战区十二片区', '十五战区十三片区', '十五战区十四片区', '十五战区一十五片区',
              ],
    "dealtotal": [
        1, 5, 4, 14, 6, 7, 8, 9, 3, 5, 17, 19, 21, 12, 19,
        2, 2, 4, 14, 6, 7, 8, 9, 3, 5, 17, 19, 21, 12, 11,
        3, 3, 4, 7, 6, 7, 8, 9, 4, 5, 17, 19, 21, 12, 9,
        4, 4, 4, 14, 6, 7, 8, 9, 5, 5, 17, 19, 21, 12, 12,
        5, 5, 4, 14, 6, 7, 8, 9, 6, 5, 17, 19, 21, 12, 11,
        6, 6, 4, 14, 6, 7, 8, 9, 3, 5, 17, 19, 21, 12, 14,
        2, 7, 4, 9, 6, 7, 8, 9, 4, 5, 17, 19, 15, 12, 21,
        3, 8, 4, 14, 6, 7, 8, 9, 3, 5, 17, 19, 17, 12, 6,
        4, 9, 4, 11, 6, 7, 8, 9, 3, 5, 17, 19, 12, 12, 19,
        5, 0, 4, 14, 6, 7, 8, 9, 3, 5, 17, 19, 21, 12, 19,
        6, 1, 4, 14, 6, 7, 8, 9, 3, 5, 17, 19, 9, 12, 19,
        # 7, 3, 4, 12, 6, 7, 8, 9, 3, 5, 17, 19, 21, 12, 19,
        # 11, 5, 4, 10, 6, 7, 8, 9, 3, 5, 17, 19, 11, 12, 14,
        # 10, 8, 4, 14, 6, 7, 8, 9, 3, 5, 17, 19, 20, 12, 19,
        # 1, 5, 4, 14, 6, 7, 8, 9, 3, 5, 17, 19, 21, 12, 19,

    ],
}
area_sale_rank_bar_yesterday = {
    'area1': ['一战区', "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区",
              '二战区', "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区",
              '三战区', "三战区", "三战区", "三战区", "三战区", "三战区", "三战区", "三战区", "三战区", "三战区", "三战区", "三战区", "三战区", "三战区", "三战区",
              '四战区', "四战区", "四战区", "四战区", "四战区", "四战区", "四战区", "四战区", "四战区", "四战区", "四战区", "四战区", "四战区", "四战区", "四战区",
              '五战区', "五战区", "五战区", "五战区", "五战区", "五战区", "五战区", "五战区", "五战区", "五战区", "五战区", "五战区", "五战区", "五战区", "五战区",
              '六战区', "六战区", "六战区", "六战区", "六战区", "六战区", "六战区", "六战区", "六战区", "六战区", "六战区", "六战区", "六战区", "六战区", "六战区",
              '七战区', "七战区", "七战区", "七战区", "七战区", "七战区", "七战区", "七战区", "七战区", "七战区", "七战区", "七战区", "七战区", "七战区", "七战区",
              '八战区', "八战区", "八战区", "八战区", "八战区", "八战区", "八战区", "八战区", "八战区", "八战区", "八战区", "八战区", "八战区", "八战区", "八战区",
              '九战区', "九战区", "九战区", "九战区", "九战区", "九战区", "九战区", "九战区", "九战区", "九战区", "九战区", "九战区", "九战区", "九战区", "九战区",
              '十战区', "十战区", "十战区", "十战区", "十战区", "十战区", "十战区", "十战区", "十战区", "十战区", "十战区", "十战区", "十战区", "十战区", "十战区",
              '十一战区', "十一战区", "十一战区", "十一战区", "十一战区", "十一战区", "十一战区", "十一战区", "十一战区", "十一战区", "十一战区", "十一战区", "十一战区",
              "十一战区", "十一战区",
              # '十二战区', "十二战区", "十二战区", "十二战区", "十二战区", "十二战区", "十二战区", "十二战区", "十二战区", "十二战区", "十二战区", "十二战区", "十二战区",
              # "十二战区", "十二战区",
              # '十三战区', "十三战区", "十三战区", "十三战区", "十三战区", "十三战区", "十三战区", "十三战区", "十三战区", "十三战区", "十三战区", "十三战区", "十三战区",
              # "十三战区", "十三战区",
              # '十四战区', "十四战区", "十四战区", "十四战区", "十四战区", "十四战区", "十四战区", "十四战区", "十四战区", "十四战区", "十四战区", "十四战区", "十四战区",
              # "十四战区", "十四战区",
              # '十五战区', "十五战区", "十五战区", "十五战区", "十五战区", "十五战区", "十五战区", "十五战区", "十五战区", "十五战区", "十五战区", "十五战区", "十五战区",
              # "十五战区", "十五战区",
              ],
    'area2': ['一战区一片区', '一战区二片区', '一战区三片区', '一战区四片区', '一战区五片区', '一战区六片区', '一战区七片区', '一战区八片区', '一战区九片区', '一战区十片区',
              '一战区十一片区', '一战区十二片区', '一战区十三片区', '一战区十四片区', '一战区一十五片区',
              '二战区一片区', '二战区二片区', '二战区三片区', '二战区四片区', '二战区五片区', '二战区六片区', '二战区七片区', '二战区八片区', '二战区九片区', '二战区十片区',
              '二战区十一片区', '二战区十二片区', '二战区十三片区', '二战区十四片区', '二战区一十五片区',
              '三战区一片区', '三战区二片区', '三战区三片区', '三战区四片区', '三战区五片区', '三战区六片区', '三战区七片区', '三战区八片区', '三战区九片区', '三战区十片区',
              '三战区十一片区', '三战区十二片区', '三战区十三片区', '三战区十四片区', '三战区一十五片区',
              '四战区一片区', '四战区二片区', '四战区三片区', '四战区四片区', '四战区五片区', '四战区六片区', '四战区七片区', '四战区八片区', '四战区九片区', '四战区十片区',
              '四战区十一片区', '四战区十二片区', '四战区十三片区', '四战区十四片区', '四战区一十五片区',
              '五战区一片区', '五战区二片区', '五战区三片区', '五战区四片区', '五战区五片区', '五战区六片区', '五战区七片区', '五战区八片区', '五战区九片区', '五战区十片区',
              '五战区十一片区', '五战区十二片区', '五战区十三片区', '五战区十四片区', '五战区一十五片区',
              '六战区一片区', '六战区二片区', '六战区三片区', '六战区四片区', '六战区五片区', '六战区六片区', '六战区七片区', '六战区八片区', '六战区九片区', '六战区十片区',
              '六战区十一片区', '六战区十二片区', '六战区十三片区', '六战区十四片区', '六战区一十五片区',
              '七战区一片区', '七战区二片区', '七战区三片区', '七战区四片区', '七战区五片区', '七战区六片区', '七战区七片区', '七战区八片区', '七战区九片区', '七战区十片区',
              '七战区十一片区', '七战区十二片区', '七战区十三片区', '七战区十四片区', '七战区一十五片区',
              '八战区一片区', '八战区二片区', '八战区三片区', '八战区四片区', '八战区五片区', '八战区六片区', '八战区七片区', '八战区八片区', '八战区九片区', '八战区十片区',
              '八战区十一片区', '八战区十二片区', '八战区十三片区', '八战区十四片区', '八战区一十五片区',
              '九战区一片区', '九战区二片区', '九战区三片区', '九战区四片区', '九战区五片区', '九战区六片区', '九战区七片区', '九战区八片区', '九战区九片区', '九战区十片区',
              '九战区十一片区', '九战区十二片区', '九战区十三片区', '九战区十四片区', '九战区一十五片区',
              '十战区一片区', '十战区二片区', '十战区三片区', '十战区四片区', '十战区五片区', '十战区六片区', '十战区七片区', '十战区八片区', '十战区九片区', '十战区十片区',
              '十战区十一片区', '十战区十二片区', '十战区十三片区', '十战区十四片区', '十战区一十五片区',
              '十一战区一片区', '十一战区二片区', '十一战区三片区', '十一战区四片区', '十一战区五片区', '十一战区六片区', '十一战区七片区', '十一战区八片区', '十一战区九片区',
              '十一战区十片区', '十一战区十一片区', '十一战区十二片区', '十一战区十三片区', '十一战区十四片区', '十一战区一十五片区',
              # '十二战区一片区', '十二战区二片区', '十二战区三片区', '十二战区四片区', '十二战区五片区', '十二战区六片区', '十二战区七片区', '十二战区八片区', '十二战区九片区',
              # '十二战区十片区', '十二战区十一片区', '十二战区十二片区', '十二战区十三片区', '十二战区十四片区', '十二战区一十五片区',
              # '十三战区一片区', '十三战区二片区', '十三战区三片区', '十三战区四片区', '十三战区五片区', '十三战区六片区', '十三战区七片区', '十三战区八片区', '十三战区九片区',
              # '十三战区十片区', '十三战区十一片区', '十三战区十二片区', '十三战区十三片区', '十三战区十四片区', '十三战区一十五片区',
              # '十四战区一片区', '十四战区二片区', '十四战区三片区', '十四战区四片区', '十四战区五片区', '十四战区六片区', '十四战区七片区', '十四战区八片区', '十四战区九片区',
              # '十四战区十片区', '十四战区十一片区', '十四战区十二片区', '十四战区十三片区', '十四战区十四片区', '十四战区一十五片区',
              # '十五战区一片区', '十五战区二片区', '十五战区三片区', '十五战区四片区', '十五战区五片区', '十五战区六片区', '十五战区七片区', '十五战区八片区', '十五战区九片区',
              # '十五战区十片区', '十五战区十一片区', '十五战区十二片区', '十五战区十三片区', '十五战区十四片区', '十五战区一十五片区',
              ],
    "dealtotal": [
        11, 2, 3, 4, 5, 6, 7, 18, 9, 10, 11, 12, 13, 14, 15,
        2, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        3, 2, 3, 4, 5, 6, 17, 18, 19, 10, 11, 12, 13, 14, 15,
        4, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        5, 2, 3, 4, 5, 16, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        6, 12, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        7, 2, 3, 14, 5, 6, 7, 18, 9, 10, 11, 12, 13, 14, 15,
        8, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        9, 2, 13, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        10, 2, 3, 14, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        # 12, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        # 13, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        # 14, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        # 15, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
    ],
}

# 区域销售分布地理分析图
china_data = {
    'ad_name': [
        '西藏自治区', '江西省', '澳门特别行政区', '河北省', '香港特别行政区', '天津市', '北京市', '吉林省', '新疆维吾尔自治区', '河南省',
        '山东省', '海南省', '江苏省', '湖南省', '青海省', '宁夏回族自治区', '浙江省', '山西省', '重庆市', '上海市',
        '辽宁省', '内蒙古自治区', '广东省', '湖北省', '陕西省', '安徽省', '广西壮族自治区', '甘肃省', '四川省', '中华人民共和国',
        '黑龙江省', '贵州省', '福建省', '江西省', '西藏自治区', '台湾省', '云南省'
    ],
    'sales': [
        262626, 7372727, 1111272411, 515172643, 1621616, 161166577, 53823615, 616238737, 5161727, 4256366,
        6362726, 12365536, 61246623, 62126168, 5225252, 32223623, 5233135361, 51513446, 52638960, 52152525,
        42625252, 5251525, 1526646572, 42536322, 52526262, 62627328, 215236772, 26221111, 52623632, 93242487430,
        52526236, 252525261, 12579000, 963252502, 2637747000, 426262664, 663611111
    ]
}

if __name__ == '__main__':
    a = pd.DataFrame(pie_key_category_sale_pie_today)
    print(a, 5315451515)
    a = pd.DataFrame(today_area_sale_)
    b = a.groupby(["area1"])
    # for i,j in a:
    #     print(i,88888888888888,j)
    # print(a.groupby(["area1"]).get_group("一战区"),33)
    for i, j in b:
        # print(i,12333333333333333333332,j)
        for a, d in j.groupby("times"):
            print(a, 9999999999999, d, 23223)
    # print(b)
    # print(b.values,type(b),b,2)
