from flask import Blueprint, render_template, request, url_for, g
from flask import redirect

from conf.router_conts import URL_SALES_BYMONTH
from services.srv_user_info import user_info, update_last_login
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

from utils.tools import create_token

blueprint = Blueprint(
    'base_blueprint',
    __name__,
    url_prefix='',
    template_folder='templates',
    static_folder='static'
)


@blueprint.route('/', methods=['POST', 'GET'])
# @user_login_data
def index():
    user = g.user
    print(user,242363636)
    return redirect(URL_SALES_BYMONTH)


# @blueprint.route(URL_SALES_BYMONTH, methods=['POST', 'GET'])
# @user_login_data
# def index():
#     # user = g.user
#     return redirect(URL_LOGIN_SALES_BYMONTH)


@blueprint.route('/login', methods=['POST', 'GET'])
def login():
    # 1.获取参数
    parama_dict = request.form
    brand = parama_dict.get("brand")  # 品牌
    username = parama_dict.get("username")  # 用户名
    password = parama_dict.get('password')  # 密码
    # if request.method == 'GET':
    #     # 判断是否已经在登录状态上:判断session中是否有token的值
    #     # if 'token' in session:
    #     #     # 已经登录了，直接去往首页
    #     #     return redirect('/')
    #     # else:
    #     #     # 没有登录，继续向下判断cookie
    #     #     if 'token' in request.cookies:
    #     #         # 曾经记住过密码,取出值保存进session
    #     #         token = request.cookies.get('token')
    #     #         session['token'] = token
    #     #         return redirect('/')
    #     #     else:
    #     #         # 　之前没有登录过,去往登录页
    #     return render_template('login.html')
    # else:
    # 2.查询数据并验证
    if not all([username, password, brand]):
        return render_template('login.html', errmsg='缺少参数！', errno=0)

    userinfo = user_info(username)  # 查询用户信息
    if not userinfo:
        return render_template('login.html', errmsg='账号有误！', errno=0)

    # print(generate_password_hash(password), '加密密码')
    if check_password_hash(userinfo[0][2], password) == False:  # 验证该密码
        return render_template('login.html', errmsg='密码错误！', errno=0)

    if brand != userinfo[0][4]:
        return render_template('login.html', errmsg='品牌错误！', errno=0)

    # 3.生成token
    token = create_token(userinfo[0][0])
    # token = create_token({"id": userinfo[0][0], "username": userinfo[0][1], "brand": userinfo[0][4]})
    # 4.保存用户的登录状态
    session['token'] = token
    session['user_id'] = userinfo[0][0]
    session['username'] = userinfo[0][1]
    session['brand'] = userinfo[0][4]
    # session['profile_photo_url'] = userinfo[0][3]
    print(token)
    # 5.拼接成功的返回信息
    data = {
        'success': 1,
        'msg': '',
        'user': {
            'user_id': userinfo[0][0],
            "username": username,
            # "profile_photo_url": userinfo[0][3],  # 用户头像
            "token_id": 'token_' + str(userinfo[0][0]),  # token id,token的key
            "brand": userinfo[0][4]
        }
    }
    update_last_login(userinfo[0][0])  # 更新上次登录时间
    print("登录成功！")
    return redirect(url_for(URL_SALES_BYMONTH))
