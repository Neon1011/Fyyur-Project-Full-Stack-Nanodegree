from flask import Flask , render_template, request , redirect, jsonify 
from flask_sqlalchemy import SQLAlchemy, Model 
from sqlalchemy import Column , ForeignKey, Integer, String, Boolean
import sys
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1@localhost:5432/ray2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# table of relation
Study = db.Table("study",db.Column("student_id",Integer,ForeignKey("student.id"),primary_key=True),
                        db.Column("course_id",Integer,ForeignKey("course.id"),primary_key=True))
#db.create_all()

# define the relationship in any of the 2 classes it dosn't matter
# backref is the name of the current Class Table that the other one will have
# easy acess through Studnt.courses and Course.students
# deal with it as a normal python list
class Student(db.Model):
    id = Column(Integer,primary_key = True)
    name = Column(String(),nullable = False)
    courses = db.relationship("Course",backref="students",secondary=Study)
    def __repr__(self):
        return '(' + str(self.id) +',' + self.name + ')'

class Course(db.Model):
    id = Column(Integer,primary_key = True)
    name = Column(String(),nullable = False)
    def __repr__(self):
        return '(' + str(self.id) +',' + self.name +')'

s =  Student.query.get(1)
s2 =  Student.query.get(2)

c1 = Course.query.get(1)
c2 = Course.query.get(2)
c3 = Course.query.get(3)

# s.courses.append(c1)
# s.courses.append(c2)
# print(s.courses)
# print(s2.courses)
# print(c1.students)
# print(c2.students)
# print(c3.students)

# when you use db.session.add() to add Parent or child , the other is added automatically
# c4 = Course(id = 5, name = 'Game Development')
# s3 = Student(id=33,name='mohaned')
# c4.students.append(s3)
# db.session.add(c4)



db.session.commit()