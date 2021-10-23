import pandas as pd
import numpy as np

from utils.clickhouse_util import client


###############
# Sql
###############

sql_bo_store = """
    select store_code, store_name, ad_code, investment
    from bo_store 
    where store_status='2' 
"""

sql_pdim_admin = """
    select ad_code, ad_name, ad_level
    from pdim_admin_district
"""

sql_sd_trade_bymonth = """
    select 
        store_name, 
        ad_name, 
        business_district_name, 
        round(avg(trade_amount_avg*business_days), 0) as amount_month,
        round(avg(net_profit_total), 0) as profit_month,
        sum(trade_amount_avg*business_days) as amount_quarter,
        sum(net_profit_total) as profit_quarter
    from sd_trade_bymonth
    where sd_month in ('6', '7', '8')
    group by store_name, ad_name, business_district_name
"""


###############
# Data_raw 
###############

# df_bo_store
data_bo_store = client.execute(sql_bo_store)
df_bo_store = pd.DataFrame(data_bo_store, columns=['store_code', 'store_name', 'ad_code', 'investment'])

# df_pdim_admin
data_pdim_admin = client.execute(sql_pdim_admin)
df_pdim_admin = pd.DataFrame(data_pdim_admin, columns=['ad_code', 'ad_name', 'ad_level'])

# df_sd_trade_bymonth
data_sd_trade_bymonth = client.execute(sql_sd_trade_bymonth)
df_sd_trade_bymonth = pd.DataFrame(data_sd_trade_bymonth, 
                                    columns=[
                                            'store_name', 
                                            'ad_name', 
                                            'business_district_name',
                                            'amount_month',
                                            'profit_month',
                                            'amount_quarter',
                                            'profit_quarter'
                                    ])

###############
# Data_mart
###############

# df_cs
df_cs = df_bo_store.merge(df_pdim_admin, on='ad_code', how='left')['ad_name'].value_counts().to_frame()\
        .reset_index().rename(columns={'index': 'ad_name', 'ad_name': 'ad_count'})

# df_md_pm_db
df_md_ana = df_sd_trade_bymonth.merge(df_bo_store, on='store_name', how='left')\
                .drop(columns=['store_code', 'ad_code'], axis=1)  # 联表
df_md_ana['roi_expect'] = round(df_md_ana['investment']/df_md_ana['profit_month'], 1)  # 投资回报周期
df_md_ana['amount_rank'] = df_md_ana['amount_quarter'].rank(ascending=False).astype(int)  # 营业额排名
df_md_ana['profit_rank'] = df_md_ana['profit_quarter'].rank(ascending=False).astype(int)  # 利润排名
df_md_pm_db = df_md_ana[['store_name', 'amount_rank', 'profit_rank']].sort_values(by='amount_rank')  # 排序
df_md_pm_db.rename(columns={'store_name': '门店名', 'amount_rank': '营业额排名', 'profit_rank': '净利润排名'}, inplace=True) # 重命名
df_md_pm_db = df_md_pm_db.melt(
    id_vars='门店名', 
    value_vars=['营业额排名', '净利润排名'], 
    var_name='排名类别', 
    value_name='排名'
)  # 融合

# df_md_pm
df_md_pm = df_md_ana.drop(['investment', 'roi_expect'], axis=1).rename(columns={
    'store_name': '门店名',
    'ad_name': '城市',
    'business_district_name': '商圈',
    'amount_month': '月度营业额',
    'profit_month': '月度利润',
    'amount_quarter': '季度营业额',
    'profit_quarter': '季度净利润',  
    'amount_rank': '营业额排名', 
    'profit_rank': '净利润排名'
}).sort_values(by='净利润排名')
df_md_pm['房租'] = np.random.randint(8000,9000,20)
df_md_pm['人工'] = np.random.randint(10000,14000,20)
col = ['门店名', '城市', '商圈', '房租', '人工', '月度营业额', '月度利润', '季度营业额', '季度净利润', '营业额排名', '净利润排名',]
df_md_pm = df_md_pm[col]

# df_qy
df_qy = pd.DataFrame({
    '区域': ['市辖区', '县', '县级市', '镇'],
    '个数': [44,4,1,1]
})

# df_md
df_md = pd.DataFrame({
    '数据范围': ['前20家门店', '前50家门店'],
    '房租': [8032, 7382],
    '人工': [14000, 13000],
    '季度营业额': [300000, 320000],
    '月均营业额': [100000, 110000],
    '净利润月': [20000, 19000],
    '净利润年': [240000, 221000],
    '投资回报周期': [6.3, 7.7],
})

# df_tz
df_tz = pd.DataFrame({
    '区域': ['成都市', '县级市', '其他市', '县', '镇'],
    '周期': [9.6, 4.8, 9.2, 6.4, 7.4]
})



