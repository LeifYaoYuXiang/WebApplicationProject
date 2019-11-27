# 这里是从Flask框架中引入Flask对象
from flask import Flask
# 从blogapp.config中引入Config对象
from blogapp.config import Config
# 从flask_sqlalchemy中引入SQLAlchemy对象
from flask_sqlalchemy import SQLAlchemy


# 将传入的变量__name__初始化Flask对象，Flask用这个参数确定程序的根目录
# __name__表示的是该模块本身的名称
app = Flask(__name__)
# 是对默认配置的修改和添加
app.config.from_object(Config)
# SQLAlchemy函数，将刚刚创建的Flask框架与工程所需要使用的数据库绑定到一起，以便实现工程与数据库连接，实现数据操作。
db = SQLAlchemy(app)

from blogapp import routes,models
