import os

import xlrd as xlrd
import xlwt as xlwt
from flask import Blueprint, render_template, request, url_for, g, jsonify
from flask import redirect

from conf.router_conts import URL_SALES_BYMONTH
from services.srv_user_info import user_info, update_last_login, default_dbname
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

from utils.db_util import just_execute, query_list
from utils.tools import create_token, md5
from utils.transfer_export_check import EXPORT_LOAD_TABLENAME_FIELD, dataToLead

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
    print(user, 242363636)
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


@blueprint.route('/data_transfe/', methods=['GET', 'POST'])
def data_transfer():
    """
    数据导入
    """
    print(request)
    a1=request.values.get("a") #获取所有参数
    a2=request.values.get("fileinfo") #获取所有参数
    a3 = request.args.get('a')
    a4 = request.form.get('a')
    aa = request.values.get('a')
    print(a1,a2,a3,a4,aa)

    a = request.files.get('file')
    print(a)
    if request.method == "GET":
        return render_template('data_transfer.html')
    file_path = r'C:\Users\ruipos\Desktop\demo.xls'
    table_key = 'fyjh'  # 将决定是用哪组数据库表数据

    data_to_lead = dataToLead()  # 创建数据导入类对象
    # 1.加载excel的数据
    clinic_file = xlrd.open_workbook(file_path)
    table = clinic_file.sheet_by_index(0)
    # 2.对相应的导入做逻辑处理(每一行的数据验证+验证之后所需执行的sql拼接)
    if table_key == 'fyjh':
        sql_str = data_to_lead.fyjh(table)
        if sql_str['code'] == 0:
            return jsonify(sql_str)

        try:
            # 3.当code不等于0的时候表示数据已经通过验证,sql已被拼接,执行拼接好的sql
            just_execute(sql_str["sql"], default_dbname)  # 执行批量插入
        except:
            return render_template('data_transfer.html', data={"code": 0, "msg": "数据库未知错误！"})
    # return render_template('data_transfer.html')
    return jsonify('ok!')
    # return render_template('data_transfer.html', data={"code": 1, "msg": "导入成功！"})


@blueprint.route('/export_data/', methods=['POST', 'GET'])
def export_data():
    """
    数据导出
    将文件下载到指定路径
    """
    file_path = r'C:\Users\ruipos\Desktop\demo111.xls'
    table_key = 'fyjh'  # 将决定是用哪组数据库表数据
    filed_str = ''  # sql字符串中的字段字符串
    excel_header = EXPORT_LOAD_TABLENAME_FIELD[table_key][4]  # 表头
    # 判断是否已有的文件
    if os.path.exists(file_path):
        return jsonify(data={"code": 0, "msg": "文件已存在"})
    for i in EXPORT_LOAD_TABLENAME_FIELD[table_key][1]:
        # 拼接sql中的字段组成
        if filed_str:
            filed_str += ','
            filed_str += i
        else:
            filed_str += i
    sql = """
        select {} from chunbaiwei.{} 
    """.format(filed_str, EXPORT_LOAD_TABLENAME_FIELD[table_key][0])  # sql字符串
    all_data = query_list(sql, default_dbname)
    # 先创建表格

    new_workbook = xlwt.Workbook()
    worksheet = new_workbook.add_sheet("sheet1")  # 创建sheet
    for row in range(len(all_data) + 1):  # 数据的行数+表头行
        for col in range(len(excel_header)):  # 列
            if row == 0:
                worksheet.write(row, col, excel_header[col])  # 写入表头
            else:
                worksheet.write(row, col, all_data[row - 1][col])  # 写入数据
    new_workbook.save(file_path)  # 保存excel

    # return render_template('data_transfer.html', data={"code": 1, "msg": "导出成功！"})
    return jsonify('ok!')
