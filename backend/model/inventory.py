from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Inventory(db.Model):
    """
    商品库存信息表
    """
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(255), nullable=False, default='', comment='SKU')
    quantity = db.Column(db.Integer, nullable=False, default=0, comment='库存数量')
    warehouse_location = db.Column(db.String(255), nullable=False, default='', comment='仓库位置')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    def __repr__(self):
        return f'<Inventory {self.sku}>'