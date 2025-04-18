from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class RegisterInfo(db.Model):
    """注册信息表"""
    __tablename__ = 'register_info'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, comment='用户名')
    password = db.Column(db.String(100), nullable=False, comment='密码')
    email = db.Column(db.String(100), comment='邮箱')
    phone_number = db.Column(db.String(20), comment='手机号')
    register_time = db.Column(db.DateTime, comment='注册时间')
    status = db.Column(db.Boolean, comment='状态')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    def __repr__(self):
        return f'<RegisterInfo {self.username}>'