from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class PermissionManagement(db.Model):
    """权限管理表"""
    __tablename__ = 'permission_management'
    
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), nullable=False, comment='角色名称')
    permission_list = db.Column(db.Text, comment='权限列表')
    create_time = db.Column(db.DateTime, comment='创建时间')
    status = db.Column(db.Boolean, comment='状态')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    def __repr__(self):
        return f'<PermissionManagement {self.role_name}>'