from flask import make_response, jsonify
from flask import request

from apps.base.routers import blueprint


# @blueprint.route('/register')
# def register():
#     # 1.获取参数
#     parama_dict = request.json
#     username = parama_dict.get("username")
#     passport = parama_dict.get('passport')
#     data = {
#         "username": username,
#         "passport": passport
#     }
#     print(data)
#     return jsonify(data)
