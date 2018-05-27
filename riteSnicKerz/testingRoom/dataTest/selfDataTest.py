from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class students(db.Model):
	id = db.Column('student_id',db.Integer,primary_key=True)
	osis = db.Column(db.Integer)
	fname = db.Column(db.String(20))
	lname = db.Column(db.String(20))
	email = db.Column(db.String(30))
	SCHEDULE = db.Column(db.String(200))
	O_average = db.Column(db.Float)
	S_average = db.Column(db.String(100))
	pw = db.Column(db.String(20))

	def __init__(self, osis, fname, lname):
		self.osis = osis
		self.fname = fname
		self.lname = lname

	def getStudent(self,od):
		return self.query.filter_by(osis=od).first()

	#PW FXNS
	def checkPW(self,unhash):
		return self.pw == String(hash(unhash)) 
	def modPW(self,unhash):
		self.pw = String(hash(unhash))

class teachers(db.Model):
 	id = db.Column('student_id',db.Integer,primary_key=True)
	teacherID = db.Column(db.Integer)

	def __init__(self,ood):
		self.teacherID = ood 

def StoL(listring):
	return json.loads(listring)

if __name__ == '__main__':
	db.create_all()
	
	newstudent = students(1234,'Brian','Leung')
	db.session.add(newstudent)
		
	newteacher = teachers(202020)
	db.session.add(newteacher)
	
	newstudent = newstudent.getStudent(1234)
	print newstudent
	
	print "DONE"
	
	db.session.commit()
	app.run(debug = True, use_reloader=False)
