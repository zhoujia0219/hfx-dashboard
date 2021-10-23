# clickhouse连接

from clickhouse_driver import Client

host = '192.168.21.50'  # 服务器地址
port = 9000  # 端口
database = 'database'  # 数据库
send_receive_timeout = 115  # 超时时间


class clickHouseConn():
    """
    clickhouse连接的类
    """

    def __init__(self):
        self.host = host  # 服务器地址
        self.port = port  # 端口
        # self.user = user  # 用户名
        # self.password = password  # 密码
        self.database = 'cdp'  # 数据库
        self.send_receive_timeout = send_receive_timeout  # 超时时间

        client = Client(host=self.host, port=self.port, database=self.database,
                        send_receive_timeout=self.send_receive_timeout
                        )

    def connectClickHouse(self):
        """
        连接
        """
        try:
            client = Client(
                host=self.host,
                port=self.port,
                database=self.database,
                send_receive_timeout=self.send_receive_timeout
            )
        except Exception:
            client = False
        return client

    def retryConnect(self, connect_num: int):
        """
        连接，如果失败就重试连接
        params connect_num：重试连接的次数
        """
        client = self.connectClickHouse()
        if client:
            return client
        for num in range(connect_num):
            client = self.connectClickHouse()
            if client:
                return client
        return False

    def query_sql(self, sql):
        """
        查询，有返回值
        """
        client = self.retryConnect(3)

        if client:
            try:
                ans = client.execute(sql)
                return ans
            except Exception as e:
                print(e)
                return "数据库错误！"

    def execute_sql(self, sql):
        """
        只是执行sql 没有返回值
        """
        client = self.retryConnect(3)
        if client:
            try:
                client.execute(sql)
            except Exception as e:
                print(e)
                return "数据库错误！"


if __name__ == '__main__':
    sql = 'select * from pdim_brand'
    sql2 = """
        INSERT INTO cdp.pdim_brand (brand_code,std_brand_code,db_schema,brand_name,trade_code,company_code,version_time)
            VALUES ('1','1','1','1','1','1',1);
        """
    test = clickHouseConn()
    ass=test.query_sql(sql)
    print(ass)
