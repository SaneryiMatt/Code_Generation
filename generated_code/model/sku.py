from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Sku(db.Model):
    """商品SKU信息表"""
    __tablename__ = 'sku'
    
    id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String(255), nullable=False, default='', comment='商品编码')
    product_name = db.Column(db.String(255), nullable=False, default='', comment='商品名称')
    specifications = db.Column(db.String(255), nullable=False, default='', comment='规格')
    unit = db.Column(db.String(50), nullable=False, default='', comment='单位')
    status = db.Column(db.String(50), nullable=False, default='', comment='状态')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    def __repr__(self):
        return f'<Sku {self.product_code}>'