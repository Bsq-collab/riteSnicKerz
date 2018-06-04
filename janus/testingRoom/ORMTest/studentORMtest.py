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

#Uhh.... new plan? make a classes db and sections db and then relate the two.
class sections(db.Model):
	id = db.Column('sectionID',db.Integer,primary_key=True)


class classes(db.Model):
	id = db.Column('classID',db.Integer,primary_key=True)
	sections = 	db.Column(db.String(1000))
	#Organization of sections data: {*section#*: {teacher:---, room:---, roster:[---]}, ...}
	max_students = db.Column(db.Integer())

