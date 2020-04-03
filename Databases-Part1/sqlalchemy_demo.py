from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# set the configrations of the app to connect to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1@localhost:5432/ray2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# initiate a database object inside the app
db = SQLAlchemy(app)

# inherits from db.Model so that the class Person is get mapped to a person table
# if there is no table call person, it creats the table 
# if it exists it do nothing
# variables linked to database attributes must be a static variables to the classes 

class Student(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String())


    # very IMPORTANT 
    # variables is considered as an object variables not static variables 
    def change(self):
        self.name +=  "######"
    # this function overload the way the record is printed in python3 interrupter or on any thing
    def __repr__(self):
        return f'<Student ID: {self.id}, name: {self.name}>'


# INSERT using Sessions 
p1 =  Student(id=9,name='sers')
p2 =  Student(id=10,name='wegz')
print(".............")
print(p1,p2)

p1.change()
print(p1)
print(p2)

# INSERT 
# db.session.add(p1)
# db.session.add(p2)
# save changes to database
#db.session.commit()

@app.route('/')
def index():
    student = Student.query.all()[4]
    print(student)
    return 'hello ' + student.name + 'with id ' + str(student.id)


# required to create tables -of the inherited classes from db.Model- if it dosn't exist 
db.create_all()

if __name__ == "__main__":
    app.run()
