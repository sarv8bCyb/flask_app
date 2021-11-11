import os
from flask import Flask,redirect,url_for,request
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy

current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

class Student(db.Model):
    __tablename__ = "student"
    student_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    roll_number = db.Column(db.String,unique=True,nullable=False)
    first_name = db.Column(db.String,nullable=False)
    last_name = db.Column(db.String)
    

class Course(db.Model):
    __tablename__ = "course"
    course_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    course_code = db.Column(db.String,unique=True,nullable=False)
    course_name = db.Column(db.String,nullable=False)
    course_description = db.Column(db.String)

class Enrollments(db.Model):
    __tablename__ = "enrollments"
    enrollment_id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    estudent_id = db.Column(db.Integer , db.ForeignKey("student.student_id"),nullable=False)
    ecourse_id = db.Column(db.Integer , db.ForeignKey("course.course_id"),nullable=False)

@app.route("/",methods=["GET","POST"])
def students():
    # students  =Student.query.all()
    students =db.session.query(Student).all()
    
    return render_template("index.html",students = students)

@app.route("/student/create",methods=["GET","POST"])
def add_student():
    if request.method == 'POST':
      roll_number = request.form['roll']
      first_name = request.form['f_name']
      last_name = request.form['l_name']
      courses = request.form.getlist('courses')

      exists = db.session.query(Student.roll_number).filter(Student.roll_number==roll_number).first() is not None
      if exists:
          return render_template("student_exists.html")
      else:
          new_student = Student(roll_number=roll_number,first_name=first_name,last_name=last_name)
      
          db.session.add(new_student)
          db.session.commit()
          stud=db.session.query(Student).filter(Student.roll_number==roll_number).first()
          estudent_id=stud.student_id
          dict={}
          dict['course_1']='MAD I'
          dict['course_2']='DBMS'
          dict['course_3']='PDSA'
          dict['course_4']='BDM'
          
          
          for course in courses:
            c = db.session.query(Course).filter(Course.course_name==dict[course]).first()
            ecourse_id=c.course_id
            enrollment = Enrollments(estudent_id=estudent_id,ecourse_id=ecourse_id)
            db.session.add(enrollment)
            db.session.commit()
            
          

            
          return redirect(url_for('students'))
    else:
        return render_template("student_form.html")
    

@app.route("/student/<student_id>/update",methods=["GET","POST"])
def update_student(student_id):
    if request.method=="POST":
        roll_number = request.form['roll']
        first_name = request.form['f_name']
        last_name = request.form['l_name']
        courses = request.form.getlist('courses')

        new_student = Student.query.filter_by(roll_number=roll_number).first()
        
        new_student.first_name= first_name
        new_student.last_name = last_name

    
        db.session.add(new_student)
        db.session.commit()
        estudent_id=db.session.query(Student).filter(Student.roll_number==roll_number).first().student_id
        dict={}
        dict['course_1']='MAD I'
        dict['course_2']='DBMS'
        dict['course_3']='PDSA'
        dict['course_4']='BDM'
            
        for course in courses:
            c = db.session.query(Course).filter(Course.course_name==dict[course]).first()
            ecourse_id=c.course_id
            enrollment = Enrollments(estudent_id=estudent_id,ecourse_id=ecourse_id)
            db.session.add(enrollment)
            db.session.commit()

            
        return redirect(url_for('students'))
    else:
        id = student_id
        student = db.session.query(Student).filter(Student.student_id==id).first()
        return render_template("update_form.html",student=student)

@app.route("/student/<student_id>/delete",methods=["GET","POST"])
def delete_student(student_id):
    if request.method=="POST":
        pass
    else:
        id = student_id
        stud = db.session.query(Student).filter(Student.student_id==id).first()
        delete_q = Enrollments.__table__.delete().where(Enrollments.estudent_id == id)
        db.session.execute(delete_q)
        db.session.delete(stud)
        db.session.commit()
        return redirect(url_for('students'))

@app.route("/student/<student_id>",methods=["GET","POST"])
def student_info(student_id):
    id = student_id
    stud = db.session.query(Student).filter(Student.student_id==id).first()
    enrollments = Enrollments.query.filter(Enrollments.estudent_id==id).all()
    courses=[]
    for enrollment in enrollments:
        course = Course.query.filter(Course.course_id==enrollment.ecourse_id).first()
        courses.append(course)

    
    return render_template("student_detail.html",stud=stud,enrollments=enrollments,courses=courses)




if __name__=='__main__':
    #Run the flask app
    app.run(
        host='0.0.0.0',
        debug=True,
        port=8080
    )

