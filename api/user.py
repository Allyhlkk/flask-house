import json

from flask import Blueprint, request, Response, jsonify

from models import User
from config import db

user_api = Blueprint('user_api', __name__)

@user_api.route('/regiser', methods=['POST'])
def register():
    #获取用户名
    username = request.form['username']
    #密码
    passward = request.form['passward']
    #邮箱
    email = request.form['email']

    #检查数据库当中是否存在用户
    result = User.query.filter(User.name == username),all()

    #如果查询出来的数据长度为0的话，则该用户名没有被注册过
    if len(result) == 0:
        user = User(name=username, passward=passward, email=email)
        #将用户对象添加到数据库当中
        db.session.add(user)
        db.session.commit()

        json_str = json.dumps({'valid':1, 'msg': user.name})
        #实例化的过程需要给他传入响应的内容
        res = Response(json_str)
        res.set_cookie('name', user.name, 3600 * 2)
        return res
    else
        return jsonify({'valid':0, 'msg': '该用户已被注册'})
    
#用户登录
@user_api.route('/login')

