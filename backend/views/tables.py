from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from models import db, TableDefinition, FieldDefinition, MenuItem
from sqlalchemy import inspect, text

tables_bp = Blueprint('tables', __name__)

@tables_bp.route('/', methods=['GET'])
def get_tables():
    # 临时调试模式：忽略JWT验证
    auth_header = request.headers.get('Authorization')
    
    # 只在开发模式下显示调试信息
    if current_app.config.get('SHOW_DEBUG_INFO', False):
        print(f"收到表格请求，授权头: {auth_header}")
    
    # 获取所有表格
    tables = TableDefinition.query.all()
    return jsonify({
        'tables': [table.to_dict() for table in tables]
    }), 200

@tables_bp.route('/<int:table_id>', methods=['GET'])
def get_table(table_id):
    # 临时调试模式：忽略JWT验证
    table = TableDefinition.query.get(table_id)
    
    if not table:
        return jsonify({'message': '未找到表格'}), 404
    
    return jsonify({
        'table': table.to_dict()
    }), 200

@tables_bp.route('/', methods=['POST'])
def create_table():
    # 临时调试模式：忽略JWT验证
    # 尝试获取请求头中的授权信息
    auth_header = request.headers.get('Authorization')
    print(f"收到创建表格请求，授权头: {auth_header}")
    
    data = request.get_json()
    
    if not data or not all(key in data for key in ['name', 'display_name']):
        return jsonify({'message': '缺少必填字段'}), 400
    
    # 检查表名是否已存在
    if TableDefinition.query.filter_by(name=data['name']).first():
        return jsonify({'message': '表名已存在'}), 400
    
    # 检查字段是否提供
    if 'fields' not in data or not data['fields']:
        return jsonify({'message': '至少需要一个字段'}), 400
    
    # 验证字段名称和显示名称不重复
    field_names = [field['name'] for field in data['fields']]
    duplicate_field_names = set([name for name in field_names if field_names.count(name) > 1])
    if duplicate_field_names:
        return jsonify({'message': f'存在重复的字段名称: {", ".join(duplicate_field_names)}'}), 400
    
    field_display_names = [field['display_name'] for field in data['fields']]
    duplicate_display_names = set([name for name in field_display_names if field_display_names.count(name) > 1])
    if duplicate_display_names:
        return jsonify({'message': f'存在重复的字段显示名称: {", ".join(duplicate_display_names)}'}), 400
    
    # 创建表格定义
    try:
        # 创建表格定义
        table = TableDefinition(
            name=data['name'],
            display_name=data['display_name'],
            description=data.get('description', '')
        )
        db.session.add(table)
        db.session.flush()  # 获取表格ID
        
        # 创建字段
        for i, field_data in enumerate(data['fields']):
            if not all(key in field_data for key in ['name', 'display_name', 'field_type']):
                db.session.rollback()
                return jsonify({'message': f'字段 #{i+1} 缺少必要数据'}), 400
            
            field = FieldDefinition(
                table_id=table.id,
                name=field_data['name'],
                display_name=field_data['display_name'],
                field_type=field_data['field_type'],
                required=field_data.get('required', False),
                default_value=field_data.get('default_value', None),
                order=i
            )
            db.session.add(field)
        
        # 创建动态表
        create_dynamic_table(table, data['fields'])
        
        # 创建菜单项
        tables_menu = MenuItem.query.filter_by(name='tables').first()
        if tables_menu:
            # 检查是否已经存在相同名称的菜单项
            existing_menu_item = MenuItem.query.filter_by(name=f"table-{table.name}").first()
            if existing_menu_item:
                # 如果存在，则更新
                existing_menu_item.display_name = table.display_name
                existing_menu_item.path = f"/tables/{table.name}"
                existing_menu_item.icon = "grid"
            else:
                # 如果不存在，则创建新的
                menu_item = MenuItem(
                    parent_id=tables_menu.id,
                    table_id=table.id,
                    name=f"table-{table.name}",
                    display_name=table.display_name,
                    path=f"/tables/{table.name}",
                    icon="grid",  # 使用grid图标
                    order=99
                )
                db.session.add(menu_item)
        
        db.session.commit()
        
        return jsonify({
            'message': '数据库表创建成功！',
            'table': table.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500

@tables_bp.route('/<int:table_id>', methods=['DELETE'])
def delete_table(table_id):
    # 临时调试模式：忽略JWT验证
    auth_header = request.headers.get('Authorization')
    print(f"收到删除表格请求，授权头: {auth_header}")
    
    table = TableDefinition.query.get(table_id)
    
    if not table:
        return jsonify({'message': 'Table not found'}), 404
    
    try:
        # 删除动态表
        drop_dynamic_table(table.name)
        
        # 删除表格定义（级联删除字段和菜单项）
        db.session.delete(table)
        db.session.commit()
        
        return jsonify({
            'message': 'Table deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500

def create_dynamic_table(table_def, fields):
    """ 在数据库中创建一个新的动态表 """
    table_name = f"dynamic_{table_def.name}"
    
    # 检查表是否存在
    inspector = inspect(db.engine)
    if table_name in inspector.get_table_names():
        raise Exception(f"Table {table_name} already exists in database")
    
    # 创建一个动态表
    columns = []
    columns.append("id INTEGER PRIMARY KEY AUTOINCREMENT" if db.engine.name == 'sqlite' else "id INT AUTO_INCREMENT PRIMARY KEY")
    
    for field in fields:
        col_type = get_sql_type(field['field_type'], db.engine.name)
        nullable = "NULL" if not field.get('required', False) else "NOT NULL"
        columns.append(f"{field['name']} {col_type} {nullable}")
    
    # 添加created_at和updated_at列
    if db.engine.name == 'sqlite':
        columns.append("created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        columns.append("updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
    else:  # mysql
        columns.append("created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        columns.append("updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    
    # 创建表
    create_stmt = f"CREATE TABLE {table_name} ({', '.join(columns)})"
    db.session.execute(text(create_stmt))

def drop_dynamic_table(table_name):
    """Drop a dynamic table from the database"""
    table_name = f"dynamic_{table_name}"
    
    # 检查表是否存在
    inspector = inspect(db.engine)
    if table_name not in inspector.get_table_names():
        return
    
    # 删除动态表
    drop_stmt = f"DROP TABLE {table_name}"
    db.session.execute(text(drop_stmt))

def get_sql_type(field_type, engine_name):
    """ 根据数据库引擎将字段类型转换为SQL列类型 """
    
    sqlite_types = {
        'text': 'TEXT',
        'longtext': 'TEXT',
        'number': 'REAL',
        'integer': 'INTEGER',
        'date': 'DATE',
        'datetime': 'TIMESTAMP',
        'boolean': 'BOOLEAN',
    }
    
    mysql_types = {
        'text': 'VARCHAR(255)',
        'longtext': 'TEXT',
        'number': 'FLOAT',
        'integer': 'INT',
        'date': 'DATE',
        'datetime': 'DATETIME',
        'boolean': 'BOOLEAN',
    }
    
    types = sqlite_types if engine_name == 'sqlite' else mysql_types
    return types.get(field_type.lower(), 'TEXT' if engine_name == 'sqlite' else 'VARCHAR(255)') 