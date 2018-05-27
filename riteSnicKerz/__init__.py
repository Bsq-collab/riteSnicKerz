#!usr/bin/python

from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/school.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class students(db.Model):
	id = db.Column('useless_id',db.Integer,primary_key=True)
	osis = db.Column(db.Integer)
	fname = db.Column(db.String(20))
	lname = db.Column(db.String(20))
	pw = db.Column(db.String(20))

	def __init__(self, osis, fname, lname, pow=''):
		self.osis = osis
		self.fname = fname
		self.lname = lname
		self.pw = str(hash(pow))

	def getStudent(self,od):
		return self.query.filter_by(osis=od).first()

	#PW FXNS
	def checkPW(self,unhash):
		return self.pw == str(hash(unhash)) 
	def modPW(self,unhash):
		self.pw = str(hash(unhash))



@app.route("/")
def home():
	return render_template("home.html")
	username = session["username"]

@app.route("/student")
def student_dash():
	return render_template("student_dash.html")

	'''
	@app.route("/about")

	# <int:student_id>
	#the student dashboard
	@app.route("/<int:student_id>")
	@app.route("/<int:student_id>/pchange")
	@app.route("/<int:student_id>/cselect")
	@app.route("/<int:student_id>/transcript")
	@app.route("/<int:student_id>/reportcard")
	@app.route("/<int:student_id>/accountsettings")
	@app.route("/<int:student_id>/pw")

	#the admin dashboard
	@app.route("/<int:admin_id>/")
	#How much detail is needed for studentView?
	@app.route("/<int:admin_id>/studentView")
	@app.route("/<int:admin_id>/courseView")
	@app.route("/<int:admin_id>/adminsettings")
	@app.route("/<int:admin_id>/adminpw")
	@app.route("/<int:admin_id>/admindata")
	@app.route("/<int:admin_id>/admininbox")
	'''

@app.route("/select_courses")
def choose_courses():
        return render_template("course_selection.html")

if __name__ == "__main__":
	db.create_all()	

	newstudent = students(1111,'21','savage',"issa")
	if (newstudent.getStudent(1111) is not None):
		print "Student already exists. Not creating."
	else:
		db.session.add(newstudent)	
		print "Student %s created"%(newstudent.fname)
		db.session.commit()

	print "Done."	

	app.run(debug = True, use_reloader=False)
