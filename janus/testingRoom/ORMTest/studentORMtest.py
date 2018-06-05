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
	db.Column('section',db.Integer,db.ForeignKey('sections')),
	db.Column('student_osis',db.Integer,db.ForeignKey('students.osis'))
)

class students(db.Model):
	id = db.Column('useless_id',db.Integer,primary_key=True)
	osis = db.Column(db.Integer())
	#classSections - will give you list of class sections that student is in. Need to go up one more in order to access class itself.

#Uhh.... new plan? make a classes db and sections db and then relate the two.

class sections(db.Model):
	id = db.Column('sectionID',db.Integer,primary_key=True)
	section_id = db.Column(db.Integer())
	roster = db.relationship('roster',secondary=studentclass,backref=db.backref('classSections'))


class classes(db.Model):
	id = db.Column('classID',db.Integer,primary_key=True)
	sections = db.relationship("sections",backref="class")
	max_students = db.Column(db.Integer())

