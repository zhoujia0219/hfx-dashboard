from datetime import datetime

from db import DbUtil

default_dbname = "data_analysis"


def find_sales_list(values):
    query_sql = """
                   SELECT 
                   areauid3, areaname3, areauid4, areaname4, storeuid, storename, weeks, rdate :: date, province, 
                   province_name, city, city_name, county, county_name, businessname, vctype, areasize, 
                   billcount, dealtotal::float, rebillcount, redealtotal, weather, weather_desc, temperature, wind_direction, 
                   "month", "year", city_level, to_char(rdate,'YYYY年MM月') as month_group
                   FROM chunbaiwei.fact_storesale_weather
                   WHERE 1 = 1
           """
    if values:
        if values["begin_month"] and values["end_month"]:
            query_sql += """  and to_char(rdate,'YYYY-MM') >= '{begin_month}'
                                     and to_char(rdate,'YYYY-MM') <= '{end_month}'
                   """.format(begin_month=values["begin_month"], end_month=values["end_month"])
        if values["city"]:
            # 长度大于1 循环处理
            citys = tuple(str(c) for c in values["city"]) if len(values['city']) > 1 \
                else "(" + str(values['city'][0]) + ")"
            query_sql += """ and city_level in {city}""".format(city=citys)
        # if values["channel"]:
        #     channels = tuple(str(c) for c in values["channel"])
        #     query_sql += """ and businessname in {channel}""".format(channel=channels)
        # if values["store_age"]:
        #     query_sql += """
        #     """

    # 从数据库查询
    data = DbUtil.query_list(query_sql, default_dbname)

    result = [{"areauid3": d[0], "areaname3": d[1], "areauid4": d[2], "areaname4": d[3], "storeuid": d[4],
               "storename": d[5], "weeks": d[6], "rdate": datetime.strptime(str(d[7]), '%Y-%m-%d').date(),
               "province": d[8], "province_name": d[9], "city": d[10], "city_name": d[11], "county": d[12],
               "county_name": d[13], "businessname": d[14], "vctype": d[15], "areasize": d[16],
               "billcount": d[17], "dealtotal": d[18], "rebillcount": d[19], "redealtotal": float(d[20]),
               "weather": d[21], "weather_desc": d[22], "temperature": d[23], "wind_direction": d[24],
               "month": d[25], "year": d[26], "city_level": int(d[27]), "month_group": d[28]} for d in data]
    return result
