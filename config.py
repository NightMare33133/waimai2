import os

#数据库配置
HOSTNAME = "127.0.0.1"
PORT     = "3306"
DATABASE = "zhijiang_flask"
USERNAME = "root"
PASSWORD = "245442"
DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)

SQLALCHEMY_DATABASE_URI= DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS= True

SECRET_KEY = "2525252"

#邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = True
MAIL_USERNAME = "2381576759@qq.com"
MAIL_PASSWORD = "dthyilimqkpoebdf"
MAIL_DEFAULT_SENDER = "2381576759@qq.com"

# 头像上传配置
ALLOWED_EXTENSIONS = ['jpg','png','gif','bmp']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR,'static')
UPLOAD_ICON_DIR = os.path.join(STATIC_DIR,'upload/icon')