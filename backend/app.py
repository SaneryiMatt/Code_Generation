from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import get_config
from models import db
from views.auth import auth_bp
from views.tables import tables_bp
from views.dynamic_tables import dynamic_tables_bp
from views.debug import debug_bp
from commands import register_commands

def create_app(config_class=None):
    # 如果未指定配置，使用环境变量确定的配置
    if config_class is None:
        config_class = get_config()
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化数据库扩展，并使用CORS扩展和JWT扩展
    db.init_app(app)
    CORS(app)
    JWTManager(app)
    
    # 注册所有路由
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(tables_bp, url_prefix='/api/tables')
    app.register_blueprint(dynamic_tables_bp, url_prefix='/api/dynamic')
    
    # 仅在开发模式下注册调试蓝图
    if app.config.get('DEBUG', False):
        app.register_blueprint(debug_bp, url_prefix='/api/debug')
    
    # 注册命令行指令
    register_commands(app)
    
    @app.route('/')
    def index():
        return {"message": "动态表格管理系统API服务正在运行"}
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.config.get('DEBUG', True)) 