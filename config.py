# 项目配置文件
from flask_sqlalchemy import SQLAlchemy
import os

# 创建flask-sqlalchemy的实例对象
db = SQLAlchemy()

class Config:
    DEBUG = False
    # 正确的配置项名称，注意大写
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), "house.db")}'
    # 关闭警告信息（通常设置为False以避免警告）
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 建议设置一个秘钥（用于会话安全等）
    SECRET_KEY = 'your_very_secret_key_here'