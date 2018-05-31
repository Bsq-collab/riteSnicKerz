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
	pw = db.Column(db.String(20))

	def __init__(self, osis, fname, lname):
		self.osis = osis
		self.fname = fname
		self.lname = lname

	def getStudent(self,od):
		return self.query.filter_by(osis=od).first()

	#PW FXNS
	def checkPW(self,unhash):
		return self.pw == str(hash(unhash)) 
	def modPW(self,unhash):
		self.pw = str(hash(unhash))

class classes(db.Model):
	id = db.Column('classID',db.Integer,primary_key=True)
	course_code = db.Column(db.String(20))
	course_name = db.Column(db.String(20))
	sections = 	db.Column(db.String(1000))
	#Organization of sections data: {*section#*: {teacher:---, room:---, roster:[---]}, ...}
	max_students = db.Column(db.Integer())

	def __init__(self,code,name,studn):
		self.course_code = code
		self.course_name = name
		self.max_students = studn
		self.sections = '{}'

	def add_section(self,num,techer,rom,roost):
		temp = json.loads(self.sections)
		temp[str(num)] = {"teacher":techer,"room":rom,"roster":roost}
		print temp
		self.sections = json.dumps(temp)

	def add_student(self,sect,osiss):
		temp = json.loads(self.sections)
		temp[str(sect)]["roster"].append(osiss)
		self.sections = json.dumps(temp)
		'''
	def edit_section(self,num,techer='',rom='',roost=''):
		temp = json.loads(self.sections)
		print temp[str(num)]
'''
'''
class teachers(db.Model):
 	id = db.Column('student_id',db.Integer,primary_key=True)
	teacherID = db.Column(db.Integer)

	def __init__(self,ood):
		self.teacherID = ood 
'''
def StoL(listring):
	return json.loads(listring)

if __name__ == '__main__':
	db.create_all()
	
	newstudent = students(1234,'Brian','Leung')
	if (newstudent.getStudent(1234) is not None):
		print newstudent
		print "Student already exists"
	else:
		db.session.add(newstudent)	
		db.session.commit()
	newcourse = classes('MKS22-',"Calculus AB",31)
	newcourse.add_section(1,"Dr. Ku",1114,["Yuyang","Terry","Lil Pump"])
	newcourse.add_student(1,"Thanos")
	db.session.add(newcourse)
	db.session.commit()
	print "DONE"	
	
	app.run(debug = True, use_reloader=False)
