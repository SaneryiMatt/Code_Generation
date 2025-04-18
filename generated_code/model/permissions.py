from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Permissions(db.Model):
    """权限信息表"""
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    permission_name = db.Column(db.String(255), nullable=False, default='')
    description = db.Column(db.String(255))

    def __repr__(self):
        return f'<Permission {self.permission_name}>'