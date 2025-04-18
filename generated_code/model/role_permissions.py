from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class RolePermissions(db.Model):
    """角色与权限的关联表"""
    __tablename__ = 'role_permissions'

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.String(255), nullable=False, default='')
    permission_id = db.Column(db.String(255), nullable=False, default='')

    def __repr__(self):
        return f'<RolePermission {self.role_id}-{self.permission_id}>'