import os,csv, json
from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = os.urandom(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#NEW ============================FLASK-SQLALCHEMY NEW CLASS DEFINTIONS======================================= NEW
#This is the association table, just dont touch it
studentclass = db.Table('ssa_table',
	db.Column('section',db.Integer,db.ForeignKey('sections.section_id')),
	db.Column('student_osis',db.Integer,db.ForeignKey('students.osis'))
)
applicantclass = db.Table('aca_table',
	db.Column('osis',db.Integer,db.ForeignKey('students.osis')),
	db.Column('applied_class',db.Integer,db.ForeignKey('classes.class_code'))
)
'''
Class: MKS22-
	Applicant_Pool:
	[
	0: blah
	1: Mr brown
	2: bloo
	]
	students_per_class: 31

	Section1: 
		Period: 3
		Teacher: Dr Ku
		Students:
		  Brian - -- 
		  Terry - - 
		  Yuyang - --
  
'''
class students(db.Model):
	id = db.Column('useless_id',db.Integer,primary_key=True)
	osis = db.Column(db.Integer())
	
	#schedule - will give you list of class sections that student is in. Need to go up one more in order to access class itself.
	legitSchedule = db.Column(db.String(1000))
	def make_legit_schedule(self):
		pass

	#applied_classes - classes applied to
	def apply_to_class(self,newClass):
		self.applied_classes.append(newClass)

	fname = db.Column(db.String(20))
	lname = db.Column(db.String(20))
	pw = db.Column(db.String(20))
	APcount = db.Column(db.Integer)
	electiveCount = db.Column(db.Integer)
	#avg must be a json in the following format: {ovrAvg: ??, dept: [class1: avg, class2: avg]}
	avg = db.Column(db.String(1000))
  
	#graduation requirements
	#Pre_Reqs

	@staticmethod
	def findStudent(os):
		return students.query.filter_by(osis=os).first()
	
	#List of next year classes?
	def __init__(self, osis, fname, lname, pow='', APcount = 0, electiveCount = 0, avg = ''):
		self.osis = osis
		self.fname = fname
		self.lname = lname
		self.pw = str(hash(pow))
		self.APcount = APcount
		self.electiveCount = electiveCount
		self.avg = avg


class sections(db.Model):
	id = db.Column('sectionID',db.Integer,primary_key=True)
	section_id = db.Column(db.Integer())
	class_code = db.Column(db.String(10),db.ForeignKey("classes.class_code"))
	teacher = db.Column(db.String(20))
	period = db.Column(db.Integer())
	roster = db.relationship('students',secondary=studentclass,backref=db.backref('schedule'))
	#upperClass - Use this to access the umbrella class for the section.

	#Mutator/Appender for roster
  	def add_to_roster(self,osis):
  		self.roster.append(students.findStudent(osis))


	def __init__(self, section_id, code, teach):
		self.section_id = section_id
		self.class_code = code
		self.teacher = teach

class classes(db.Model):
	id = db.Column('classID',db.Integer,primary_key=True)

	sections = db.relationship("sections",backref="upperClass",lazy = True)

	students_per_class = db.Column(db.Integer())
	max_students = db.Column(db.Integer())
	class_code = db.Column(db.String(10))
	class_name = db.Column(db.String(20))
	description = db.Column(db.String(1000))

	@staticmethod
	def findClass(coode):
		return classes.query.filter_by(class_code = coode).first()

	#Applicant Pool
	applicant_pool = db.relationship("students",secondary=applicantclass,backref=db.backref('applied_classes'),lazy=True)
	
	def append_to_applicant_pool(self,newStudent):
		self.applicant_pool.append(students.findStudent(newStudent))

	def set_applicant_pool(self,pool):
		self.applicant_pool = pool 

	def get_applicant_pool(self):
		return self.applicant_pool

	
	#Appender/Adder for Applicant Pool
	#Mutator/Sorter for Applicant Pool
	#Need to get max number of students acceptable

	def __init__(self, studn, code, name, descr=''):
		self.students_per_class = studn
		self.class_code = code
		self.class_name = name
		self.description = descr
		'''
		if (self.students_per_class is not None):
			self.max_students = self.students_per_class*len(sections)	
		'''

	def get_sections(self):
		return self.sections


	
#NEW ===============================END OF NEW CLASS DEFINITIONS============================================== NEW

db.create_all()
exclass = classes(31,"MKS22X","AP Calc AB")
print classes.findClass("MKS22X")
#exstud = students(1111,'21','savage')
#print "1 Student applied to "+str(exstud.applied_classes)
#exstud.apply_to_class(exclass)
#exclass.applicant_pool.append(exstud)
#print "2 Student applied to "+str(exstud.applied_classes)

#db.session.add(exstud)
#db.session.add(exclass)
db.session.commit()