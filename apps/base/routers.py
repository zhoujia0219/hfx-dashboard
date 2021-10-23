from flask import Blueprint, render_template, request, url_for, jsonify, session
from flask import redirect
from apps.base.views.data_transfer import to_import_view, export_data_view
from apps.base.views.login import login_view
from conf.router_conts import URL_SALES_BYMONTH

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
    return jsonify({"code": 1})


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


@blueprint.route('/to_import/', methods=['GET', 'POST'])
def to_import():
    """
    数据导入路由
    """
    # 1.判断请求方法，GET方法则直接跳转到页面不做处理
    if request.method == "GET":  # get方法则是显示导入的页面
        return render_template('data_transfer.html')
    # 2.取参数
    file = request.files.get('file')
    table_key = 'brand'  # 将决定是用哪组数据库表数据

    # 3.调用视图处理逻辑，得到逻辑结果
    data = to_import_view(file, table_key)

    # 4.返回响应
    # return render_template('data_transfer.html', data=data)
    return jsonify(data)  # 返回处理的结果


@blueprint.route('/export_data/', methods=['POST', 'GET'])
def export_data():
    """
    数据导出
    将文件下载到指定路径
    """
    data = export_data_view()
    return render_template('data_transfer.html', data=data)
