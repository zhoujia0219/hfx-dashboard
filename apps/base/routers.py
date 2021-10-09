from flask import Blueprint, make_response, jsonify, render_template, request
from flask import redirect

from conf.router_conts import URL_SALES_BYMONTH
from services.srv_user_info import user_info
from werkzeug.security import generate_password_hash, check_password_hash
from flask import  session
blueprint = Blueprint(
    'base_blueprint',
    __name__,
    url_prefix='',
    template_folder='templates',
    static_folder='static'
)


@blueprint.route('/')
def index():
    return redirect(URL_SALES_BYMONTH)


# @blueprint.route('/login')
@blueprint.route('/login', methods=['POST', 'GET'])
def login():
    # 1.获取参数
    parama_dict = request.form
    username = parama_dict.get("username")  # 用户名
    password = parama_dict.get('password')  # 密码
    # 2.查询数据并验证
    if not all([username,password]):
        return render_template('login.html', data={'success': 0, 'msg': '缺少参数！'})
    userinfo = user_info(username)
    if not userinfo:
        return render_template('login.html', data={'success': 0, 'msg': '账号有误！'})
    print(generate_password_hash(password), '加密密码')
    if check_password_hash(userinfo[0][2], password) == False:
        return render_template('login.html', data={'success': 0, 'msg': '密码错误！'})
    # 3.保存用户的登录状态
    session['id'] = userinfo[0][0]
    # 4.拼接成功的返回信息
    data = {
        'success': 1,
        'msg': '',
        'userinfo': {
            "username": username,
            "profile_photo_url": userinfo[0][3]  # 用户头像

        }
    }
    # return render_template('login.html', data=data)

    return jsonify(data)
