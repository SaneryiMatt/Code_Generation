from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Roles(db.Model):
    """角色信息表"""
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(255), nullable=False, default='')
    description = db.Column(db.String(255))

    def __repr__(self):
        return f'<Role {self.role_name}>'