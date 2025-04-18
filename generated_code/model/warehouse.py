from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Warehouse(db.Model):
    """仓库位置信息表"""
    __tablename__ = 'warehouse'
    
    id = db.Column(db.Integer, primary_key=True)
    warehouse_code = db.Column(db.String(255), nullable=False, default='', comment='仓库编码')
    warehouse_name = db.Column(db.String(255), nullable=False, default='', comment='仓库名称')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    def __repr__(self):
        return f'<Warehouse {self.warehouse_code}>'