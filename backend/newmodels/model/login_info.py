from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class LoginInfo(db.Model):
    """登录信息表"""
    __tablename__ = 'login_info'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, comment='用户名')
    password = db.Column(db.String(100), nullable=False, comment='密码')
    login_time = db.Column(db.DateTime, comment='登录时间')
    login_ip = db.Column(db.String(50), comment='登录IP')
    status = db.Column(db.Boolean, comment='状态')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    def __repr__(self):
        return f'<LoginInfo {self.username}>'