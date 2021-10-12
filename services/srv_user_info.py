from utils import db_util
default_dbname = "data_analysis"


def user_info(username):
    """
    查询用户信息
    """
    query_sql = """
        select id,username,password,profile_photo_url,brand from chunbaiwei.user where username='{}'
        """ .format(username)
    userinfo = db_util.query_list(query_sql, default_dbname)
    # print(userinfo)
    return userinfo


def update_last_login(id):
    """
    更新上次登录时间
    """
    sql = """
        update chunbaiwei.user set last_login=now() where id='{}'
    """.format(id)
    db_util.just_execute(sql, default_dbname)
