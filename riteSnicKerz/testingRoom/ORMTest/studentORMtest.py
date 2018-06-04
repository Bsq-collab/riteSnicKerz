import os
from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#association table
stclAsso = db.Table('subs',
	db.Column('user_id',db.Integer,db.ForeignKey('user.user_id')),
	db.Column('channel_id',db.Integer,db.ForeignKey('channel.channel_id'))
)

class students(db.Model):
	id = db.Column('useless_id',db.Integer,primary_key=True)
	osis = db.Column(db.Integer)


	def __init__(self, osis, fname, lname, pow=''):
		self.osis = osis
		self.fname = fname
		self.lname = lname
		self.pw = str(hash(pow))

class classes(db.Model):
	id = db.Column('classID',db.Integer,primary_key=True)
	course_code = db.Column(db.String(20))
	course_name = db.Column(db.String(20))
	sections = 	db.Column(db.String(1000))
	#Organization of sections data: {*section#*: {teacher:---, room:---, roster:[---]}, ...}
	max_students = db.Column(db.Integer())

	def __init__(self,code,name,studn,sekshuns={}):
		self.course_code = code
		self.course_name = name
		self.max_students = studn
		self.sections = str(sekshuns)

	def add_section(self,num,techer,rom,roost):
		temp = json.loads(self.sections)
		temp[str(num)] = {"teacher":techer,"room":rom,"roster":roost}
		print temp
		self.sections = json.dumps(temp)
