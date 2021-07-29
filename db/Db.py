import logging

import psycopg2
import psycopg2.extensions
import psycopg2.extras
import psycopg2.pool

from conf import config

logging.getLogger(__name__)


class LoggingCursor(psycopg2.extensions.cursor):
    def execute(self, sql, args=None):
        logger = logging.getLogger('sql_debug')
        logger.info(self.mogrify(sql, args))

        try:
            psycopg2.extensions.cursor.execute(self, sql, args)
        except Exception as exc:
            logger.error("%s: %s" % (exc.__class__.__name__, exc))
            raise


def gp_connect(dbname: str):
    try:
        conn_pool = psycopg2.pool.SimpleConnectionPool(minconn=1, maxconn=5, dbname=dbname,
                                                       user=config.USERNAME,
                                                       password=config.PASSWORD,
                                                       host=config.HOST,
                                                       port=config.PORT)
        # 从数据库连接池获取连接
        conn = conn_pool.getconn()
        return conn
    except psycopg2.DatabaseError as e:
        print("could not connect to Greenplum server", e)


# 查询数据
def query_list(sql: str, dbname: str):
    conn = gp_connect(dbname=dbname)
    cur = conn.cursor(cursor_factory=LoggingCursor)
    try:
        cur.execute(sql)
        return cur.fetchall()
    except Exception as e:
        logging.error("查询异常：{}, sql {}", str(e), sql)
        raise e
    finally:
        conn.close()


