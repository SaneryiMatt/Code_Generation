from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class StudentInfo(db.Model):
    """学生信息表"""
    __tablename__ = 'student_info'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, comment='姓名')
    student_id = db.Column(db.String(50), nullable=False, unique=True, comment='学号')
    gender = db.Column(db.String(10), comment='性别')
    age = db.Column(db.Integer, default=0, comment='年龄')
    class_name = db.Column(db.String(50), comment='班级')
    contact = db.Column(db.String(100), comment='联系方式')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    def __repr__(self):
        return f'<Student {self.name}>'