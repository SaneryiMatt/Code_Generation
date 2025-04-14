from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, TableDefinition
from sqlalchemy import text, inspect

dynamic_tables_bp = Blueprint('dynamic_tables', __name__)

@dynamic_tables_bp.route('/<string:table_name>', methods=['GET'])
def get_table_data(table_name):
    # 临时调试模式：忽略JWT验证
    auth_header = request.headers.get('Authorization')
    print(f"收到获取表格数据请求，表名: {table_name}，授权头: {auth_header}")
    
    # 检查表格是否存在
    table_def = TableDefinition.query.filter_by(name=table_name).first()
    if not table_def:
        return jsonify({'message': '表格不存在'}), 404
    
    # 分页查询参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 构建动态查询
    try:
        # 计算偏移量和限制
        offset = (page - 1) * per_page
        limit = per_page
        
        # 获取总记录数
        count_query = f"SELECT COUNT(*) as count FROM dynamic_{table_name}"
        count_result = db.session.execute(text(count_query)).fetchone()
        total = count_result.count if count_result else 0
        
        # 分页获取数据
        query = f"SELECT * FROM dynamic_{table_name} ORDER BY id DESC LIMIT {limit} OFFSET {offset}"
        result = db.session.execute(text(query))
        
        # 将结果转换为字典列表
        data = []
        for row in result:
            item = {}
            for column, value in row._mapping.items():
                item[column] = value
            data.append(item)
        
        return jsonify({
            'data': data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        }), 200
    except Exception as e:
        return jsonify({'message': f'错误: {str(e)}'}), 500

@dynamic_tables_bp.route('/<string:table_name>/<int:record_id>', methods=['GET'])
def get_record(table_name, record_id):
    # 临时调试模式：忽略JWT验证
    auth_header = request.headers.get('Authorization')
    print(f"收到获取记录请求，表名: {table_name}，记录ID: {record_id}，授权头: {auth_header}")
    
    # 检查表格是否存在
    table_def = TableDefinition.query.filter_by(name=table_name).first()
    if not table_def:
        return jsonify({'message': '表格不存在'}), 404
    
    try:
        # 根据ID获取记录
        query = f"SELECT * FROM dynamic_{table_name} WHERE id = {record_id}"
        result = db.session.execute(text(query)).fetchone()
        
        if not result:
            return jsonify({'message': '记录不存在'}), 404
        
        # 转换为字典
        record = {}
        for column, value in result._mapping.items():
            record[column] = value
        
        return jsonify({
            'record': record
        }), 200
    except Exception as e:
        return jsonify({'message': f'错误: {str(e)}'}), 500

@dynamic_tables_bp.route('/<string:table_name>', methods=['POST'])
def create_record(table_name):
    # 临时调试模式：忽略JWT验证
    auth_header = request.headers.get('Authorization')
    print(f"收到创建记录请求，表名: {table_name}，授权头: {auth_header}")
    
    # 检查表格是否存在
    table_def = TableDefinition.query.filter_by(name=table_name).first()
    if not table_def:
        return jsonify({'message': '表格不存在'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'message': '未提供数据'}), 400
    
    try:
        # 获取表结构以验证字段
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns(f"dynamic_{table_name}")
                  if col['name'] not in ['id', 'created_at', 'updated_at']]
        
        # 过滤无效字段
        valid_data = {k: v for k, v in data.items() if k in columns}
        
        if not valid_data:
            return jsonify({'message': '未提供有效字段'}), 400
        
        # 使用SQLAlchemy更安全的参数传递方式
        fields = ', '.join(valid_data.keys())
        
        # 创建命名参数占位符
        placeholders = ', '.join([f":{k}" for k in valid_data.keys()])
        
        # 构建SQL语句
        query = f"INSERT INTO dynamic_{table_name} ({fields}) VALUES ({placeholders})"
        
        # 使用命名参数执行SQL
        result = db.session.execute(text(query), valid_data)
        
        # 获取插入记录的ID
        if db.engine.name == 'sqlite':
            last_id_query = "SELECT last_insert_rowid() as id"
        else:  # mysql
            last_id_query = "SELECT LAST_INSERT_ID() as id"
            
        last_id = db.session.execute(text(last_id_query)).fetchone().id
        db.session.commit()
        
        # 获取插入的记录
        get_query = f"SELECT * FROM dynamic_{table_name} WHERE id = {last_id}"
        record = db.session.execute(text(get_query)).fetchone()
        
        # 转换为字典
        result = {}
        for column, value in record._mapping.items():
            result[column] = value
        
        return jsonify({
            'message': '记录创建成功',
            'record': result
        }), 201
    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"创建记录时发生错误: {str(e)}")
        traceback.print_exc()
        return jsonify({'message': f'错误: {str(e)}'}), 500

@dynamic_tables_bp.route('/<string:table_name>/<int:record_id>', methods=['PUT'])
def update_record(table_name, record_id):
    # 临时调试模式：忽略JWT验证
    auth_header = request.headers.get('Authorization')
    print(f"收到更新记录请求，表名: {table_name}，记录ID: {record_id}，授权头: {auth_header}")
    
    # 检查表格是否存在
    table_def = TableDefinition.query.filter_by(name=table_name).first()
    if not table_def:
        return jsonify({'message': '表格不存在'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'message': '未提供数据'}), 400
    
    try:
        check_query = f"SELECT id FROM dynamic_{table_name} WHERE id = {record_id}"
        record = db.session.execute(text(check_query)).fetchone()
        
        if not record:
            return jsonify({'message': '记录不存在'}), 404
        
        # 获取表结构以验证字段
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns(f"dynamic_{table_name}")
                  if col['name'] not in ['id', 'created_at', 'updated_at']]
        
        # 过滤无效字段
        valid_data = {k: v for k, v in data.items() if k in columns}
        
        if not valid_data:
            return jsonify({'message': '未提供有效字段'}), 400
        
        # 使用SQLAlchemy更安全的参数传递方式
        # 构建set子句，使用命名参数
        set_clause = ', '.join([f"{k} = :{k}" for k in valid_data.keys()])
        
        # 将record_id添加到参数字典中
        params = {**valid_data, 'record_id': record_id}
        
        # 构建更新SQL
        query = f"UPDATE dynamic_{table_name} SET {set_clause} WHERE id = :record_id"
        
        # 执行语句
        db.session.execute(text(query), params)
        db.session.commit()
        
        # 获取更新后的记录
        get_query = f"SELECT * FROM dynamic_{table_name} WHERE id = {record_id}"
        updated_record = db.session.execute(text(get_query)).fetchone()
        
        # 将结果转换为字典
        result = {}
        for column, value in updated_record._mapping.items():
            result[column] = value
        
        return jsonify({
            'message': '记录更新成功',
            'record': result
        }), 200
    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"更新记录时发生错误: {str(e)}")
        traceback.print_exc()
        return jsonify({'message': f'错误: {str(e)}'}), 500

@dynamic_tables_bp.route('/<string:table_name>/<int:record_id>', methods=['DELETE'])
def delete_record(table_name, record_id):
    # 临时调试模式：忽略JWT验证
    auth_header = request.headers.get('Authorization')
    print(f"收到删除记录请求，表名: {table_name}，记录ID: {record_id}，授权头: {auth_header}")
    
    # 检查表格是否存在
    table_def = TableDefinition.query.filter_by(name=table_name).first()
    if not table_def:
        return jsonify({'message': '表格不存在'}), 404
    
    try:
        check_query = f"SELECT id FROM dynamic_{table_name} WHERE id = {record_id}"
        record = db.session.execute(text(check_query)).fetchone()
        
        if not record:
            return jsonify({'message': '记录不存在'}), 404
        
        query = f"DELETE FROM dynamic_{table_name} WHERE id = {record_id}"
        db.session.execute(text(query))
        db.session.commit()
        
        return jsonify({
            'message': '记录删除成功'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'错误: {str(e)}'}), 500