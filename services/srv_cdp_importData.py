import math

from utils.clickhouse_conn import clickHouseConn
from pandas.core.frame import DataFrame

client = clickHouseConn()  # 建立导入类的对象


# 时间段方法
def switchStr(minsrt, maxstr):
    if (len(str(minsrt)) == 1):
        minsrt = '0{}:00'.format(minsrt)
    else:
        minsrt = '{}:00'.format(minsrt)
    if (len(str(maxstr)) == 1):
        maxstr = '0{}:00'.format(maxstr)
    else:
        maxstr = '{}:00'.format(maxstr)
    return minsrt + "-" + maxstr


if __name__ == '__main__':
    switchStr(1, 2)
# 取一天内的时间段
sql_time_order = """
    select time_period_code,min_value,max_value from cdp.cdim_time_period
"""
query_time_order = client.query_sql(sql_time_order)
time_order = []
for row in query_time_order:
    time_order.append([row[0], switchStr(row[1], row[2])])

# 取计算门店数量的数据
sql_store_count = """
    select time_period.time_period_code,count(time_period.quantity)/2 
    from cdp.sd_trade_byday array join time_period 
    group by `time_period.time_period_code` 
    having `time_period.quantity` !='0' 
    order by `time_period.time_period_code`;
"""
query_store_count = client.query_sql(sql_store_count)

# 取所有门店都在营业的时间段（11点-21点间）的平均销售额
sql_all_store_avg = """
    select time_period.time_period_code,AVG(time_period.amount) 
    from cdp.sd_trade_byday array join time_period 
    group by `time_period.time_period_code` 
    having `time_period.time_period_code` BETWEEN '2021090111' AND '2021090121' 
    order by `time_period.time_period_code`; 
"""
query_all_store_avg = client.query_sql(sql_all_store_avg)

# 取营业额和利润排名前20且重合的门店在一天的时段内的平均销售额
sql_order_data = """
    select store_name,sum(trade_amount_avg),sum(net_profit_total) 
    from cdp.sd_trade_bymonth 
    group by store_name 
    order by sum(trade_amount_avg) DESC ,sum(net_profit_total) DESC LIMIT 20
"""
query_order_data = client.query_sql(sql_order_data)

sql_store_merge = """
    select store_name,store_code
    from cdp.bo_store
"""
query_store_merge = client.query_sql(sql_store_merge)

sql_order_store_avg = """
    select time_period.time_period_code,AVG(time_period.amount) 
    from cdp.sd_trade_byday array join time_period 
    WHERE store_code in ('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20')
    group by `time_period.time_period_code` 
    order by `time_period.time_period_code`; """
query_order_store_avg = client.query_sql(sql_order_store_avg)

# 取堂食、外卖占比 & 营业额、利润排名
sql_proport_total = """
    select y.store_name,x.ts_data,x.wm_data from
(select a.store_code,sum(a.ts/a.total) as ts_data,sum(b.wm/b.total2) as wm_data from 
(select store_code,SUM(`marketing_channel.quantity`) as ts,SUM(`time_period.quantity`) as total 
FROM cdp.sd_trade_byday array join marketing_channel,time_period
group by store_code
having `marketing_channel.marketing_channel_name` ='堂食' ) a
LEFT JOIN
(select store_code,SUM(`marketing_channel.quantity`) as wm,sum(`time_period.quantity`) as total2
FROM cdp.sd_trade_byday array join marketing_channel,time_period
group by store_code
having `marketing_channel.marketing_channel_name` ='外卖' ) b
on a.store_code=b.store_code
group BY a.store_code) x
INNER JOIN 
(select DISTINCT store_code,store_name from cdp.bo_store) y
on x.store_code=y.store_code
where store_name != ''
"""
query_proport_total = client.query_sql(sql_proport_total)

sql_profit_amount_order = """
    select store_name,sum(trade_amount_avg) as amount,sum(net_profit_total) as profit 
    from cdp.sd_trade_bymonth 
    group by store_name 
    order by sum(trade_amount_avg) DESC,sum(net_profit_total) DESC """
query_profit_amount_order = client.query_sql(sql_profit_amount_order)
query_profit_amount_order_rank = [list(i) for i in query_profit_amount_order]
a = query_profit_amount_order_rank
# 进行排序，提取下标
# for i in a:
#     print(i)
# print('排序后：-----------')

# 先对第一列进行排序

# 中括号内填写按哪行排序
list_data = sorted(a, key=lambda x: (x[1]))
# 倒序输出
return_list = []
index = 1  # 自定义下标
for row in reversed(list_data):
    return_list.append([row[0], row[1], row[2], index])
    index = index + 1

# 第一列数据排序处理完毕，再对第二列进行排序
# 中括号内填写按哪行排序
list_data_2 = sorted(return_list, key=lambda x: (x[2]))
# 倒序输出
return_list_2 = []
index2 = 1  # 自定义下标
for row in reversed(list_data_2):
    return_list_2.append([row[0], row[1], row[2], row[3], index2])
    index2 = index2 + 1


# 转换成dataframe类型
query_time_order = [list(i) for i in time_order]
query_store_count = [list(i) for i in query_store_count]
query_all_store_avg = [list(i) for i in query_all_store_avg]
query_order_store_avg = [list(i) for i in query_order_store_avg]
query_store_merge = [list(i) for i in query_store_merge]
query_order_data = [list(i) for i in query_order_data]
query_proport_total = [list(i) for i in query_proport_total]

df_time_order = DataFrame(query_time_order)
df_store_count = DataFrame(query_store_count, dtype=int)
df_all_store_avg = DataFrame(query_all_store_avg)
df_order_store_avg = DataFrame(query_order_store_avg)
df_store_merge = DataFrame(query_store_merge)
df_order_data = DataFrame(query_order_data)
df_proport_total = DataFrame(query_proport_total)
df_rank = DataFrame(return_list_2)

# 门店数量数据加工
def demo(data):
    res = []
    for i in range(6): # 整体数据分成了6份
        pd_data = data[i*4:(i+1)*4]
        demo_list = list()
        for j in range(4):  # 把每份数据往后加4次
            demo_list.append(pd_data.loc[j+(i*4)]['1_x'])
            demo_list.append(pd_data.loc[j+(i*4)]['1_y'])
        res.append(demo_list)
    pd_data = DataFrame(res)
    return pd_data
# 门店数量数据
data_time_storecount = df_time_order.merge(df_store_count, left_on=0, right_on=0)
res= demo(data_time_storecount)

# 所有门店时段内平均销售额
data_time_allstore_avg = df_time_order.merge(df_all_store_avg, left_on=0, right_on=0)
# (1)合并门店表和月营业排名表 and (2)继续合并时段平均销售额表
data_month_order = df_time_order.merge(df_order_store_avg, left_on=0, right_on=0)
# 合并销售占比
data_sales_proport = df_rank.merge(df_proport_total, left_on=0, right_on=0)
