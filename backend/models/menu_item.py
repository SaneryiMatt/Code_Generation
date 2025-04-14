from . import db
from datetime import datetime

class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=True)
    table_id = db.Column(db.Integer, db.ForeignKey('table_definitions.id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(50), nullable=True)
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 添加children关系
    children = db.relationship('MenuItem', 
                              backref=db.backref('parent', remote_side=[id]),
                              cascade='all, delete-orphan')
    
    def to_dict(self, include_children=True):
        result = {
            'id': self.id,
            'parent_id': self.parent_id,
            'table_id': self.table_id,
            'name': self.name,
            'display_name': self.display_name,
            'path': self.path,
            'icon': self.icon,
            'order': self.order,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_children and self.children:
            result['children'] = [child.to_dict() for child in self.children]
            
        return result 