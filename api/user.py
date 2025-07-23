import json
from flask import Blueprint, request, Response, jsonify

from models import User
from config import db

user_api = Blueprint('user_api', __name__)

@user_api.route('/register', methods=['POST'])
def register():
    #获取用户名
    username = request.form['username']
    #密码
    password = request.form['password']
    #邮箱
    email = request.form['email']

    #检查数据库当中是否存在该用户
    result = User.query.filter(User.name == username).all()

    #如果查询出来的数据长度为0的话，则该用户名没有被注册过
    if len(result) == 0:
        user = User(name=username, password=password, email=email)
        #将用户对象添加到数据库当中
        db.session.add(user)
        db.session.commit()

        json_str = json.dumps({'valid':1, 'msg': user.name})
        #实例化的过程需要给他传入响应的内容
        res = Response(json_str)
        res.set_cookie('name', user.name, 3600 * 2)
        return res
    else:
        return jsonify({'valid':0, 'msg': '该用户已被注册'})
    

#用户登录
@user_api.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    #查询用户是否存在
    user = User.query.filter(User.name == username).first()
    #如果用户存在
    if user:
        #判断密码是否相等
        if user.password == password:
            result = {'valid':1, 'msg': user.name}
            result_json = json.dumps(result)
            res = Response(result_json)
            res.set_cookie('name', user.name, 3600 * 2)
            return res
        else:
            return jsonify({'valid':0, 'msg': '密码错误'})
    else:
        return jsonify({'valid': 0, 'msg': '用户不存在'})
    
#退出登录
@user_api.route('/logout')
def logout():
    #先从cookie中获取用户信息
    name = request.cookies.get('name')
    if name:
        result = {'valid': 1, 'msg': '退出登录成功'}
        json_str = json.dumps(result)
        res = Response(json_str)
        res.delete_cookie('name')
        return res
    else:
        return jsonify({'valid':0, 'msg':'未登录'})

#用户信息修改
@user_api.route('/modify/userinfo/<field>', methods=['POST'])
def modify_userinfo(field):
    y_name = request.form.get('y_name')
    new_value = request.form.get('new_value')

    user = User.query.filter_by(name=y_name).first()
    if not user or not new_value:
        return jsonify({'ok': '0'})

    if field == 'name':
        user.name = new_value
    elif field == 'addr':
        user.addr = new_value
    elif field == 'email':
        user.email = new_value
    elif field == 'pd':
        user.password = new_value
    else:
        return jsonify({'ok': '0'})

    db.session.commit()
    return jsonify({'ok': '1'})

#收藏
@user_api.route('/collect_on', methods=['POST'])
def collect_on():
    house_id = request.form.get('house_id')
    username = request.form.get('user_name')
    user = User.query.filter_by(name=username).first()

    if not user:
        return jsonify({'valid': '0', 'msg': '用户不存在'})

    ids = user.collect_id.split(',') if user.collect_id else []
    if house_id not in ids:
        ids.append(house_id)
        user.collect_id = ','.join(ids)
        db.session.commit()

    return jsonify({'valid': '1', 'msg': '收藏成功'})

#清空浏览记录
@user_api.route('/del_record', methods=['POST'])
def del_record():
    username = request.form.get('user_name')
    user = User.query.filter_by(name=username).first()
    if not user:
        return jsonify({'valid': '0', 'msg': '用户不存在'})

    user.seen_id = ''  # 清空记录
    db.session.commit()
    return jsonify({'valid': '1', 'msg': '浏览记录已清空'})

#取消收藏
@user_api.route('/collect_off', methods=['POST'])
def collect_off():
    house_id = request.form.get('house_id')
    username = request.form.get('user_name')
    user = User.query.filter_by(name=username).first()

    if not user:
        return jsonify({'valid': '0', 'msg': '用户不存在'})

    if user.collect_id:
        ids = user.collect_id.split(',')
        if house_id in ids:
            ids.remove(house_id)
            user.collect_id = ','.join(ids)
            db.session.commit()
            return jsonify({'valid': '1', 'msg': '取消收藏成功'})
        else:
            return jsonify({'valid': '0', 'msg': '房源未收藏'})
    else:
        return jsonify({'valid': '0', 'msg': '收藏列表为空'})

