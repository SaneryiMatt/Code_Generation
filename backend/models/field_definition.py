from . import db
from datetime import datetime

class FieldDefinition(db.Model):
    __tablename__ = 'field_definitions'
    
    id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Integer, db.ForeignKey('table_definitions.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    field_type = db.Column(db.String(50), nullable=False)  # text, number, date, boolean, etc.
    required = db.Column(db.Boolean, default=False)
    default_value = db.Column(db.String(255), nullable=True)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'table_id': self.table_id,
            'name': self.name,
            'display_name': self.display_name,
            'field_type': self.field_type,
            'required': self.required,
            'default_value': self.default_value,
            'order': self.order,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
    @staticmethod
    def get_sqlalchemy_type(field_type):
        """Convert field type to SQLAlchemy type"""
        type_mapping = {
            'text': db.String(255),
            'longtext': db.Text,
            'number': db.Float,
            'integer': db.Integer,
            'date': db.Date,
            'datetime': db.DateTime,
            'boolean': db.Boolean,
        }
        return type_mapping.get(field_type.lower(), db.String(255)) 