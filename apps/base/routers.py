import os

import xlrd as xlrd
import xlwt as xlwt
from flask import Blueprint, render_template, request, url_for, jsonify, make_response, session
from flask import redirect
from werkzeug.exceptions import abort

from apps.base.views.data_transfer import to_lead_view, export_data_view
from apps.base.views.login import login_view, verify_code_view
from conf.router_conts import URL_SALES_BYMONTH
from services.srv_user_info import default_dbname

from utils.db_util import just_execute, query_list
from utils.transfer_export_check import EXPORT_LOAD_TABLENAME_FIELD, dataToLead

blueprint = Blueprint(
    'base_blueprint',
    __name__,
    url_prefix='',
    template_folder='templates',
    static_folder='static'
)


@blueprint.route('/', methods=['POST', 'GET'])
def index():
    return redirect(URL_SALES_BYMONTH)


@blueprint.route('/verify_code/', methods=['POST'])
def verify_code():
    """
    验证码
    """
    im_code = request.json.get("code")  # 获取验证码
    session['im_code'] = im_code
    return jsonify({"code":1})


@blueprint.route('/login', methods=['POST', 'GET'])
def login():
    """
    登录
    """
    if request.method == 'GET':
        return render_template('login.html')
    is_success = login_view()  # 登录逻辑
    if not is_success:
        return render_template('login.html', errmsg='信息有误！', errno=0)
    return redirect(url_for(URL_SALES_BYMONTH))


@blueprint.route('/to_lead/', methods=['GET', 'POST'])
def to_lead():
    """
    数据导入
    """
    if request.method == "GET":
        return render_template('data_transfer.html')
    data = to_lead_view()
    return render_template('data_transfer.html', data=data)


@blueprint.route('/export_data/', methods=['POST', 'GET'])
def export_data():
    """
    数据导出
    将文件下载到指定路径
    """
    # file_path = r'C:\Users\ruipos\Desktop\demo111.xls'
    # table_key = 'fyjh'  # 将决定是用哪组数据库表数据
    # filed_str = ''  # sql字符串中的字段字符串
    # excel_header = EXPORT_LOAD_TABLENAME_FIELD[table_key][4]  # 表头
    # # 判断是否已有的文件
    # if os.path.exists(file_path):
    #     return jsonify(data={"code": 0, "msg": "文件已存在"})
    # for i in EXPORT_LOAD_TABLENAME_FIELD[table_key][1]:
    #     # 拼接sql中的字段组成
    #     if filed_str:
    #         filed_str += ','
    #         filed_str += i
    #     else:
    #         filed_str += i
    # sql = """
    #     select {} from chunbaiwei.{}
    # """.format(filed_str, EXPORT_LOAD_TABLENAME_FIELD[table_key][0])  # sql字符串
    # all_data = query_list(sql, default_dbname)
    # # 先创建表格
    #
    # new_workbook = xlwt.Workbook()
    # worksheet = new_workbook.add_sheet("sheet1")  # 创建sheet
    # for row in range(len(all_data) + 1):  # 数据的行数+表头行
    #     for col in range(len(excel_header)):  # 列
    #         if row == 0:
    #             worksheet.write(row, col, excel_header[col])  # 写入表头
    #         else:
    #             worksheet.write(row, col, all_data[row - 1][col])  # 写入数据
    # new_workbook.save(file_path)  # 保存excel
    data = export_data_view()
    return render_template('data_transfer.html', data=data)
