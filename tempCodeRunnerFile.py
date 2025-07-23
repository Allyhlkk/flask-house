#项目入口文件
from flask import Flask, render_template
from config import Config, db

#首页
from page.index import index_page
#搜索页
from page.query import query_page
#列表页
from page.list import list_page
#详情页
from page.detail import detail_page

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

#注册首页
app.register_blueprint(index_page, url_prefix='/')
#注册搜索页
app.register_blueprint(query_page, url_prefix='/')
#注册列表页
app.register_blueprint(list_page, url_prefix='/')
#注册详情页
app.register_blueprint(detail_page, url_prefix='/')

app
if __name__ == '__main__':
    app.run(debug=True)