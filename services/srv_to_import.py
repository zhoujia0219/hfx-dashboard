from utils.clickhouse_conn import clickHouseConn

client = clickHouseConn()


def pay_mode_all_data_code():
    """查询支付方式的编码"""
    sql = """
        select  pay_mode_code from cdp.cdim_pay_mode
    """
    return client.query_sql(sql)


def pay_mode_all_data_other():
    """查询支付方式的编码之外的数据"""
    sql = """
        select  pay_mode_name from cdp.cdim_pay_mode
    """
    return client.query_sql(sql)


def pay_channel_all_data_code():
    """查询支付渠道的编码"""
    sql = """
        select  pay_channel_code from cdp.cdim_pay_channel
    """
    return client.query_sql(sql)


def pay_channel_all_data_other():
    """查询支付渠道的编码之外的数据"""
    sql = """
        select  pay_channel_name from cdp.cdim_pay_channel
    """
    return client.query_sql(sql)
