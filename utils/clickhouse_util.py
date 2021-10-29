from clickhouse_driver import Client

client = Client(host='192.168.21.51', port='9000', database='cdp')

###########################################
import logging
from clickhouse_sqlalchemy import make_session
from sqlalchemy import create_engine

logging.getLogger(__name__)


def get_session(dbname: str):
    conf = {"user": "default", "password": "", "server_host": "192.168.21.51", "port": "8123", "db": dbname}
    connection = 'clickhouse://{user}:{password}@{server_host}:{port}/{db}'.format(**conf)
    engine = create_engine(connection, pool_size=100, pool_recycle=3600, pool_timeout=20)

    return make_session(engine)


def execute(dbname: str, sql: str):
    session = get_session(dbname)
    cursor = session.execute(sql)
    try:
        fields = cursor._metadata.keys
        return [dict(zip(fields, item)) for item in cursor.fetchall()]
    except Exception as e:
        logging.error("执行SQL异常：{}, sql {}", str(e), sql)
        raise e
    finally:
        cursor.close()
        session.close()
