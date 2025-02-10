from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(10), nullable=False)

class AttendanceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    device = db.Column(db.String(50), nullable=False)