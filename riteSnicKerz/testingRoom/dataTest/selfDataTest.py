from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class students(db.Model):
	id = db.Column('student_id',db.Integer,primary_key=True)
	osis = db.Column(db.Integer,unique=True)
	fname = db.Column(db.String(20))
	lname = db.Column(db.String(20))
	'''
	email = db.Column(db.String(30))
	SCHEDULE = db.Column(db.String(1000))
	O_average = db.Column(db.Float)
	S_average = db.Column(db.String(200))
	'''
	def __init__(self, osis, fname, lname):
		self.osis = osis
		self.fname = fname
		self.lname = lname

class teachers(db.Model):
 	id = db.Column('student_id',db.Integer,primary_key=True)
	teacherID = db.Column(db.Integer,unique=True)

	def __init__(self,ood):
		self.teacherID = ood 

if __name__ == '__main__':
	app.run(debug = True)
	db.create_all()
	newstudent = students(207268863,'Brian','Leung')
	db.session.add(newstudent)
	newstudent = students(31415,"J","DW")
	db.session.add(newstudent)
	newteacher = teachers(202020)
	db.session.add(newteacher)
	db.session.commit()
