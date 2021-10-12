from flask import request, current_app, session
from werkzeug.utils import redirect

from conf.basic_const import WHITE_URL_LIST
from flask_app import create_app

app = create_app()


# 对每一次请求的钩子函数,登录验证
@app.before_request
def requied_login():
    current_url = request.url
    is_white_url = False
    for white_url in WHITE_URL_LIST:
        # 如果是白名单则不需要验证
        if (current_url.replace(white_url, "") + white_url) == current_url:
            is_white_url = True
            break
    if is_white_url:
        return
    token = session.get("token", None)
    if token is None:
        return redirect('/login')  # 如果没有该登录信息就跳到登录页面


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8011, debug=True)
