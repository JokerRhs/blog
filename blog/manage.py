import datetime


import redis
from flask import Flask
from flask_script import Manager
from flask_session import Session

from back.models import db
from back.views import back_blue
from web.views import web_blue

app = Flask(__name__)
app.register_blueprint(blueprint=back_blue, url_prefix='/back')
app.register_blueprint(blueprint=web_blue, url_prefix='/web')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456789@127.0.0.1:3306/blog'
db.init_app(app)
app.secret_key='dfmomlkskgpoefs846fiufhe512'
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)

# PERMANENT_SESSION_LIFETIME = datetime.timedelta(seconds=20)

app.permanent_session_lifetime = datetime.timedelta(hours=6)
# 配置方法：第一种
Session(app)

if __name__ == '__main__':
    manage = Manager(app)
    manage.run()

