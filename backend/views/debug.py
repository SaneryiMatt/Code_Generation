from flask import Blueprint, jsonify
from models import db, MenuItem
from sqlalchemy import inspect

debug_bp = Blueprint('debug', __name__)

@debug_bp.route('/ping', methods=['GET'])
def ping():
    """ 用于检查API是否正常运行的简单端点 """
    return jsonify({
        'status': 'success',
        'message': 'API运行正常'
    }), 200

@debug_bp.route('/db-check', methods=['GET'])
def db_check():
    """ 检查数据库连接和配置 """
    try:
        # 测试数据库连接是否正常
        db.session.execute('SELECT 1')
        
        # 获取数据库引擎信息和表结构
        engine_name = db.engine.name
        tables = inspect(db.engine).get_table_names()
        
        return jsonify({
            'status': 'success',
            'database': {
                'type': engine_name,
                'uri': str(db.engine.url).replace(':password@', ':​**​*@'),  # 隐藏密码的安全显示
                'tables': tables  # 数据库中的所有表
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)  # 返回错误信息
        }), 500

@debug_bp.route('/menu', methods=['GET'])
def get_menu():
    """ 获取菜单结构 """
    try:
        # 查询所有顶级菜单项（parent_id为空的项）
        top_menus = MenuItem.query.filter_by(parent_id=None).order_by(MenuItem.order).all()
        
        # 将菜单项转换为字典格式
        menu = [item.to_dict() for item in top_menus]
        
        return jsonify({
            'status': 'success',
            'menu': menu  # 返回完整的菜单结构
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)  # 返回错误信息
        }), 500