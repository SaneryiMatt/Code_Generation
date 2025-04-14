import os
import logging
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 环境配置
ENVIRONMENT = os.environ.get('FLASK_ENV', 'development')
DEBUG_MODE = os.environ.get('FLASK_DEBUG', '1') == '1'

class Config:
    # Basic 配置
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key')
    
    # Database 配置
    DATABASE_TYPE = os.environ.get('DATABASE_TYPE', 'sqlite')
    
    if DATABASE_TYPE == 'sqlite':
        SQLITE_DB_PATH = os.environ.get('SQLITE_DB_PATH', 'instance/dynamic_tables.db')
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{SQLITE_DB_PATH}'
    else:  # mysql
        MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
        MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')
        MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
        MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'password')
        MYSQL_DB = os.environ.get('MYSQL_DB', 'dynamic_tables')
        SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
    
    # SQLAlchemy 配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT 配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour 
    
    # 日志配置
    LOG_LEVEL = logging.DEBUG if DEBUG_MODE else logging.INFO
    
    # 是否显示调试信息
    SHOW_DEBUG_INFO = DEBUG_MODE
    
class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    LOG_LEVEL = logging.WARNING
    SHOW_DEBUG_INFO = False
    
# 根据环境选择配置
def get_config():
    if ENVIRONMENT == 'production':
        return ProductionConfig
    else:
        return DevelopmentConfig 