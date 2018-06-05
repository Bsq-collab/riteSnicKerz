import os
from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#classes.query.all()

#association table

studentclass = db.Table('ssa_table',
	db.Column('section',db.Integer,db.ForeignKey('sections.section_id')),
	db.Column('student_osis',db.Integer,db.ForeignKey('students.osis'))
)

class students(db.Model):
	id = db.Column('useless_id',db.Integer,primary_key=True)
	osis = db.Column(db.Integer())
	#classSections - will give you list of class sections that student is in. Need to go up one more in order to access class itself.


class sections(db.Model):
	id = db.Column('sectionID',db.Integer,primary_key=True)
	section_id = db.Column(db.Integer())
	class_code = db.Column(db.String(10),db.ForeignKey("classes.class_code"))
	roster = db.relationship('students',secondary=studentclass,backref=db.backref('classSections'))


class classes(db.Model):
	id = db.Column('classID',db.Integer,primary_key=True)
	sections = db.relationship("sections",backref="upperClass",lazy = True)
	max_students = db.Column(db.Integer())
	class_code = db.Column(db.String(10))

	def __init__(self,classCode):
		self.class_code = classCode

if __name__ == '__main__':
	db.create_all()
	sect1=sections(section_id=3)
	class1 = classes("MKS")
	class1.sections.append(sect1)
	student1=students(osis = 1111)
	student2=students(osis=10101)
	sect1.roster.append(student1)
	sect1.roster.append(student2)
	print "Sections "+str(class1.sections)
	print "Class code: "+str(class1.class_code)
	print "Class of sect1: "+str(sect1.upperClass.class_code)
	print "Roster of sect1 "+str(sect1.roster)
	print "ID of student 0 of sect1 "+str(sect1.roster[0].osis)
	print "Sections of student: " +str(student1.classSections)
	print "Class of Section of student " +str(student1.classSections[0].upperClass.class_code)
	#db.commit()
	app.run(debug = True, use_reloader=False)
