import pandas as pd

yesterday_area_sale_ = {
    "area1": ["一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区",
              "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区"],
    "area2": ["一战区一片区", "一战区一片区", "一战区一片区", "一战区一片区", "一战区一片区", "一战区一片区", "一战区一片区", "一战区一片区", "一战区一片区",
              "一战区一片区", "一战区一片区", "一战区一片区", "一战区一片区", '二战区一片区', '二战区一片区', '二战区一片区', '二战区一片区', '二战区一片区', '二战区一片区',
              '二战区一片区', '二战区一片区', '二战区一片区', '二战区一片区', '二战区一片区', '二战区一片区', '二战区一片区', ],
    'dealtotal': [11, 20, 13, 11, 11, 23, 36, 11, 63, 11, 11, 52, 11,
                  66, 43, 43, 15, 14, 43, 43, 43, 28, 43, 43, 35, 26, ],
    'times': [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
              12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, ],
    'rdate': ['2021-03-20', '2021-03-20',
              '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20',
              '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20',
              '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20', '2021-03-20',
              '2021-03-20', '2021-03-20', '2021-03-20', ]
}

today_area_sale_ = {
    "area1": ["一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "一战区", "二战区", "二战区", "二战区", "二战区",
              "二战区", "二战区", "二战区", "二战区", "二战区", "二战区", "二战区"],
    "area2": ["一战区一片区", "一战区一片区", "一战区一片区", "一战区一片区", "一战区一片区", "一战区一片区", "一战区一片区", "一战区一片区", "一战区一片区", "一战区一片区",
              "一战区一片区",
              '二战区一片区', '二战区一片区', '二战区一片区', '二战区一片区', '二战区一片区', '二战区一片区', '二战区一片区', '二战区一片区', '二战区一片区', '二战区一片区',
              '二战区一片区'
              ],
    'dealtotal': [1, 44, 22, 29, 31, 11, 47, 53, 84, 11, 15,
                  2, 43, 25, 8, 43, 14, 43, 25, 18, 5, 10, ],
    'times': [1, 4, 3, 2, 5, 6, 7, 8, 9, 10, 11,
              1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    'rdate': ["2021-03-21", "2021-03-21",
              "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21",
              "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21",
              "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21", "2021-03-21"]
}
# if __name__ == '__main__':
#     a = pd.DataFrame(today_area_sale_)
#     b =a.groupby(["area1"])
#     # for i,j in a:
#     #     print(i,88888888888888,j)
#     # print(a.groupby(["area1"]).get_group("一战区"),33)
#     for i,j in b:
#         # print(i,12333333333333333333332,j)
#         for a,d in j.groupby("times"):
#             print(a,9999999999999,d,23223)
#     # print(b)
#     # print(b.values,type(b),b,2)
#
#     啊= [i for i in range(222)]
