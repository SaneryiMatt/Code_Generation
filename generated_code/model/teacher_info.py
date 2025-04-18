from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class TeacherInfo(db.Model):
    """教师信息表"""
    __tablename__ = 'teacher_info'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, comment='姓名')
    teacher_id = db.Column(db.String(50), nullable=False, unique=True, comment='工号')
    gender = db.Column(db.String(10), comment='性别')
    title = db.Column(db.String(50), comment='职称')
    courses_taught = db.Column(db.String(200), comment='教授课程')
    contact = db.Column(db.String(100), comment='联系方式')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    def __repr__(self):
        return f'<Teacher {self.name}>'