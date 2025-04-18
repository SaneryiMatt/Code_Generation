from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Inventory(db.Model):
    """库存数量信息表"""
    __tablename__ = 'inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    sku_code = db.Column(db.String(255), nullable=False, default='', comment='SKU编码')
    current_stock = db.Column(db.Float, nullable=False, default=0, comment='当前库存')
    safety_stock = db.Column(db.Float, nullable=False, default=0, comment='安全库存')
    locked_stock = db.Column(db.Integer, nullable=False, default=0, comment='锁定库存')
    available_stock = db.Column(db.Integer, nullable=False, default=0, comment='可用库存')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    def __repr__(self):
        return f'<Inventory {self.sku_code}>'