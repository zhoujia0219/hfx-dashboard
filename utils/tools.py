# 其他的类型工具
import functools
from copy import copy
from flask import current_app, g
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import session
from flask import session
from werkzeug.utils import redirect


def big_number_conduct(numb, decimal_point: int):
    """大的数字的处理
    param numb:传入的数字
    param decimal_point:保留小数的位数
    return:带单位万或者亿的字符串
    """
    try:
        result = float(copy(numb))
    except Exception:
        return numb
    numb_constant = float(copy(numb))
    million_1 = 1000000  # 100万
    million_100 = 100000000  # 1亿
    # 先处理成为万的单位(小于1亿大于等于1百万)
    if numb_constant < million_100 and numb_constant >= million_1:
        result = format(round((numb_constant / 10000), decimal_point), ',') + "万"
        result = result if len(result.split('.')[1]) == decimal_point + 1 else result.replace("万", '0' * (
                decimal_point - (len(result.split('.')[1]) - 1)) + "万")
    # 再如果可以处理成为亿的单位则处理成为亿的单位
    elif numb_constant > million_100:
        result = format(round((numb_constant / million_100), decimal_point), ',') + "亿"
        result = result if len(result.split('.')[1]) == 3 else result.replace("亿", '0' * (
                decimal_point - (len(result.split('.')[1]) - 1)) + "亿")
    else:
        result = format(result, ',')
    return result


def create_token(user_id):
    '''
    生成token
    :param api_user:用户id
    :return: token
    '''

    # 第一个参数是内部的私钥，这里写在共用的配置信息里了，如果只是测试可以写死
    # 第二个参数是有效期(秒)
    # s = Serializer('fwfwgweh', expires_in=3600)
    s = Serializer(current_app.config["SECRET_KEY"], expires_in=3600)
    # 接收用户id转换与编码
    token = s.dumps(user_id).decode("ascii")
    return token


def verify_token(token_id):
    '''
    校验token
    :param token:前端所带的token
    :return: 用户信息 or None
    '''
    # 参数为私有秘钥，跟上面方法的秘钥保持一致
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        server_token = session.get(token_id, "")  # 保存在服务器的token值
        if server_token and token_id:
            user = {
                "user_id": session["user_id"],
                "username": session["username"],
                "brand": session["brand"],
                # "profile_photo_url": session["profile_photo_url"],
                "token": token_id
            }
            return user
        else:
            return None
    except Exception:
        return None


def user_login_data(f):
    # 装饰内层函数，使其在路由引入时候函数名字不是相同
    """
    通过@user_login_data的形式装饰到需要验证的页面的路由上
    例如：
        @blueprint.route('/', methods=['POST', 'GET'])
        @user_login_data
        def index():
            pass
    当需要取用户信息的时候，user = g.user 即可取到相应的登录用户信息
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        token = session.get("token", None)
        user = None
        if token:
            try:
                # 查询用户登录信息
                user = {
                    "user_id": session.get("user_id", None),
                    "username": session.get("username", None),
                    "brand": session.get("brand", None),
                }
                print("token验证成功！", token)

            except Exception as e:
                current_app.logger.error(e)
        else:
            return redirect('/login')  # 如果没有该登录信息就跳到登录页面
        g.user = user
        return f(*args, **kwargs)

    return wrapper


if __name__ == '__main__':
    a = create_token({'user_id': 1, 'username': "fewfe", "brand": "测试品牌"})
    print(a)
