from io import BytesIO

from flask import request, session, render_template
from werkzeug.security import check_password_hash

from services.srv_user_info import update_last_login, user_info
from utils.tools import create_token
from utils.verification_code import get_verify_code


def verify_code_view():
    """
    验证码
    """
    image, code = get_verify_code()
    # 图片以二进制形式写入
    buf = BytesIO()
    image.save(buf, 'gif')
    buf_str = buf.getvalue()  # 图片数据
    session["image"] = code
    return buf_str, code


def login_view():
    # 1.获取参数
    parama_dict = request.form
    brand = parama_dict.get("brand")  # 品牌
    username = parama_dict.get("username")  # 用户名
    password = parama_dict.get('password')  # 密码
    img_code = parama_dict.get('verify_img')  # 验证码

    # 2.查询数据并验证
    if not all([username, password, brand]):
        return False
    print(session.get("im_code", None),img_code)
    if session.get("im_code", None).lower() != img_code.lower():
        return False
    userinfo = user_info(username)  # 查询用户信息
    if not userinfo:
        return False
    # print(generate_password_hash(password), '加密密码')
    if not check_password_hash(userinfo[0][2], password):  # 验证该密码
        return False

    if brand != userinfo[0][4]:
        return False

    # 3.生成token
    token = create_token(userinfo[0][0])
    # 4.保存用户的登录状态
    session['token'] = token
    session['user_id'] = userinfo[0][0]
    session['username'] = userinfo[0][1]
    session['brand'] = userinfo[0][4]
    print(token)
    # # 5.拼接成功的返回信息
    # data = {
    #     'success': 1,
    #     'msg': '',
    #     'data': {
    #         'user_id': userinfo[0][0],
    #         "user_name": username,
    #         "token_id": 'token_' + str(userinfo[0][0]),  # token id,token的key
    #         "brand": userinfo[0][4]
    #     }
    # }
    update_last_login(userinfo[0][0])  # 更新上次登录时间
    print("登录成功！")
    return True
