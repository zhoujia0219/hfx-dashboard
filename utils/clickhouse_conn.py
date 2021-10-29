# clickhouse连接
from clickhouse_sqlalchemy import make_session
from sqlalchemy import create_engine
from clickhouse_driver import Client

host = '192.168.21.55'  # 服务器地址
port = 9090  # 端口
user = 'ckuser'
password = 'ckuser'
database = 'database'  # 数据库
send_receive_timeout = 115  # 超时时间
db = 'cdp'


class clickHouseConn_driver():
    """
    clickhouse连接的类
    """

    def __init__(self):
        self.host = host  # 服务器地址
        self.port = port  # 端口
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


class clickHouseConn():
    """
    clickhouse连接的类
    """

    def __init__(self):
        # self.conf = {"server_host": host, "port": port, "db": "cdp"}
        # self.connection = 'clickhouse://@{server_host}:{port}/{db}'.format(**self.conf)
        # self.engine = create_engine(self.connection, pool_size=100, pool_recycle=3600, pool_timeout=20)
        self.conf = {
            "user": "ckuser",
            "password": "ckuser",
            "server_host": "192.168.21.55",
            "port": "9090",
            "db": "cdp"
        }
        self.engine = create_engine(
            'clickhouse://{user}:{password}@{server_host}:{port}/{db}'.format(**self.conf),
            echo=False,
            pool_size=5,
            max_overflow=10
        )

    def get_session(self, engine):
        return make_session(engine)

    def query_sql(self, sql):
        """
        查询：列表嵌元组的形式
        """
        session = self.get_session(self.engine)
        cursor = session.execute(sql)
        try:
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            raise e
        finally:
            cursor.close()
            session.close()

    def execute(self, sql):
        """
        查询：列表嵌字典的形式，
        """
        session = self.get_session(self.engine)
        cursor = session.execute(sql)
        try:
            fields = cursor._metadata.keys
            return [dict(zip(fields, item)) for item in cursor.fetchall()]
        except Exception as e:
            raise e
        finally:
            cursor.close()
            session.close()

    def execute_sql(self, sql):
        """
        执行，没有返回值
        """
        try:
            session = self.get_session(self.engine)
            cursor = session.execute(sql)
            cursor.close()
            session.close()
        except Exception as e:
            raise e


if __name__ == '__main__':
    sql = '        select  pay_mode_code from cdp.cdim_pay_mode'
    sql2 = """
        INSERT INTO cdp.pdim_brand (brand_code,std_brand_code,db_schema,brand_name,trade_code,company_code,version_time)
            VALUES ('1','1','1','1','1','1',1);
        """
    test = clickHouseConn()
    ass = test.execute(sql)
    print(ass)
