from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Students(db.Model):
	id = db.Column('student_id',db.Integer,primary_key=True)
	osis = db.Column(db.Integer)
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


if __name__ == '__main__':
	db.create_all()
	newstudent = Students(207268863,'Brian','Leung')
	db.session.add(newstudent)
	#db.session.commit()
	app.run(debug = True)
