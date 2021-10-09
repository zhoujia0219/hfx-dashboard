from utils import db_util
default_dbname = "data_analysis"


def user_info(username):
    """
    查询用户信息
    """
    query_sql = """
        select id,username,password,profile_photo_url from chunbaiwei.user where username='{}'
        """ .format(username)
    userinfo = db_util.query_list(query_sql, default_dbname)
    print(userinfo)
    return userinfo
