from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class WarehouseLocation(db.Model):
    """仓库位置信息表"""
    __tablename__ = 'warehouse_location'
    
    id = db.Column(db.Integer, primary_key=True)
    warehouse_code = db.Column(db.String(255), nullable=False, default='', comment='仓库编码')
    warehouse_name = db.Column(db.String(255), nullable=False, default='', comment='仓库名称')
    region = db.Column(db.String(255), nullable=False, default='', comment='所在地区')
    address = db.Column(db.Text, nullable=False, default='', comment='详细地址')
    contact_person = db.Column(db.String(100), nullable=False, default='', comment='联系人')
    contact_number = db.Column(db.String(50), nullable=False, default='', comment='联系方式')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    def __repr__(self):
        return f'<WarehouseLocation {self.warehouse_code}>'