from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not all(key in data for key in ['username', 'email', 'password']):
        return jsonify({'message': '必填项缺失！'}), 400
    
    # 检查用户名或邮箱是否已存在
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': '用户名已存在！'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': '邮箱已注册！'}), 400
    
    # 创建新用户
    try:
        user = User(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        db.session.add(user)
        db.session.commit()
        
        # 生成访问令牌
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': '用户注册成功！',
            'user': user.to_dict(),
            'access_token': access_token
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'服务器错误: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print(f"收到登录请求: {data}")
        
        if not data or not all(key in data for key in ['username', 'password']):
            return jsonify({'message': '请输入用户名和密码'}), 400
        
        # 开发调试模式：如果使用admin/admin123登录，总是成功
        if data['username'] == 'admin' and data['password'] == 'admin123':
            # 查找admin用户，如果不存在就创建一个
            admin_user = User.query.filter_by(username='admin').first()
            if not admin_user:
                admin_user = User(
                    username='admin',
                    email='admin@example.com',
                    password='admin123'
                )
                db.session.add(admin_user)
                db.session.commit()
            
            # 生成访问令牌
            access_token = create_access_token(identity=admin_user.id)
            
            response_data = {
                'message': '管理员登录成功',
                'user': admin_user.to_dict(),
                'access_token': access_token
            }
            print(f"登录成功: {admin_user.username}")
            return jsonify(response_data), 200
        
        # 正常用户验证逻辑
        user = User.query.filter_by(username=data['username']).first()
        
        if not user:
            return jsonify({'message': '用户名不存在'}), 401
        
        # 检查密码
        if not user.check_password(data['password']):
            return jsonify({'message': '密码不正确'}), 401
        
        # 生成访问令牌
        access_token = create_access_token(identity=user.id)
        
        response_data = {
            'message': '登录成功',
            'user': user.to_dict(),
            'access_token': access_token
        }
        print(f"登录成功: {user.username}")
        return jsonify(response_data), 200
    except Exception as e:
        db.session.rollback()
        error_message = f"登录处理过程中发生异常: {str(e)}"
        print(error_message)
        import traceback
        traceback.print_exc()
        return jsonify({'message': '登录失败，请稍后再试'}), 500

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    # 尝试从请求头中获取 Authorization 头部
    auth_header = request.headers.get('Authorization')
    
    # 如果没有 Authorization 头部，返回错误
    if not auth_header:
        return jsonify({'message': '缺少授权头'}), 401
    
    # 解析令牌
    try:
        # 分割 "Bearer token" 格式，获取实际的令牌
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({'message': '授权格式无效'}), 401
        
        token = parts[1]
        # 解码令牌获取用户 ID
        from flask_jwt_extended import decode_token
        decoded = decode_token(token)
        user_id = decoded['sub']
        
        # 查找用户
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': '用户不存在'}), 404
        
        # 返回用户信息
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        print(f"JWT解析错误: {str(e)}")
        # 开发环境下使用模拟用户
        if current_app.config.get('DEBUG', False):
            # 使用ID为1的管理员用户
            admin_user = User.query.filter_by(username='admin').first()
            if admin_user:
                return jsonify({'user': admin_user.to_dict()}), 200
        
        return jsonify({'message': '令牌验证失败'}), 401