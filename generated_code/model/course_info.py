from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class CourseInfo(db.Model):
    """课程信息表"""
    __tablename__ = 'course_info'
    
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False, comment='课程名称')
    course_id = db.Column(db.String(50), nullable=False, unique=True, comment='课程编号')
    instructor = db.Column(db.String(100), comment='授课教师')
    credit = db.Column(db.Float, default=0, comment='学分')
    class_time = db.Column(db.String(100), comment='上课时间')
    classroom = db.Column(db.String(100), comment='上课地点')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    def __repr__(self):
        return f'<Course {self.course_name}>'