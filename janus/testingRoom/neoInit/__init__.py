import os,csv, json
from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = os.urandom(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/school.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#NEW ============================FLASK-SQLALCHEMY NEW CLASS DEFINTIONS======================================= NEW
#This is the association table, just dont touch it
studentclass = db.Table('ssa_table',
	db.Column('section',db.Integer,db.ForeignKey('sections.section_id')),
	db.Column('student_osis',db.Integer,db.ForeignKey('students.osis'))
)
'''
Class: MKS22-
	Applicant_Pool:
  	[
    0: blah
    1: Mr brown
    2: bloo
    ]
  Max_Students: 31

  Section1: 
  	Period: 3
    Teacher:
  	Students:
    	Brian - -- 
      Terry - - 
      Yuyang - --
  
  Section2:
  	
  	Period: 5
    Teacher:
    Students: 
    	Brian - -- -
  
  Section3:
  	Period: 9
'''
class students(db.Model):
	id = db.Column('useless_id',db.Integer,primary_key=True)
	osis = db.Column(db.Integer())
	#schedule - will give you list of class sections that student is in. Need to go up one more in order to access class itself.
	legitSchedule = db.Column(db.String(1000))
  
	fname = db.Column(db.String(20))
	lname = db.Column(db.String(20))
	pw = db.Column(db.String(20))
	APcount = db.Column(db.Integer)
	electiveCount = db.Column(db.Integer)
	#avg must be a json in the following format: {ovrAvg: ??, dept: [class1: avg, class2: avg]}
	avg = db.Column(db.String(1000))
  
  #graduation requirements
  #Pre_Reqs
  
  #MVP_CLASS_SELECTIONS = classes relationship [AP ENG, AP CALC, BLah, Blah, Blahdw]
  #CONFIRMED CLASS LIST = classes relationship [MKS22X,REGENTS PHYSICS] - Be sure to get periods from classList
  
  
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
  
	def __init__(self, section_id, code, teach):
		self.section_id = section_id
		self.class_code = code
		self.teacher = teach

class classes(db.Model):
	id = db.Column('classID',db.Integer,primary_key=True)
	sections = db.relationship("sections",backref="upperClass",lazy = True)
	
  max_students = db.Column(db.Integer())
	class_code = db.Column(db.String(10))
	class_name = db.Column(db.String(20))
	description = db.Column(db.String(1000))
  
  applicant_pool = db.relationship("applicant_pool")
  #Applicant Pool
  #Appender/Adder for Applicant Pool
  #Mutator/Sorter for Applicant Pool
  #Need to get max number of students acceptable
	
  #Then scheduling. oooooooo
  #ALGO THINGY
  
	def __init__(self, studn, code, name, descr=''):
		self.max_students = studn
		self.class_code = code
		self.class_name = name
		self.description = descr
    
  def get_sections():
    
#NEW ===============================END OF NEW CLASS DEFINITIONS============================================== NEW


#
# ============================START OF SQLALCHEMY STUDENT CLASS DEFINITION=============================

	# def getStudent(self,od):
	#   return self.query.filter_by(osis=od).first()

	# #PW FXNS
	# def getPW(self, os):
	#   return self.query.filter_bystr(self.pw)
	#
	# def modPW(self,unhash):
	#   self.pw = str(hash(unhash))

# ============================ACCESSOR & MUTATORS FOR STUDENT CLASS=============================
def getStudent(osis):
	st = students.query.filter_by(osis=osis).first()
	# print st.fname
	return st

# def getAPcount(osis):
#   st = getStudent(osis)
#   return st.APcount

def setElectiveCount(osis, electiveCount):
	st.getStudent(osis)
	prev = st.electiveCount
	st.electiveCount = electiveCount
	db.commit()
	return prev

def setAPcount(osis, newAPcount):
	st = getStudent(osis)
	prev = st.APcount
	st.APcount = newAPcount
	db.commit()
	return prev
# ============================END OF ACCESSOR & MUTATORS FOR STUDENT CLASS=============================
# ============================END OF SQLALCHEMY STUDENT CLASS DEFINITION=============================

# UNFINISHED
# ============================START OF SQLALCHEMY COURSE CLASS DEFINITION=============================

# ============================END OF SQLALCHEMY COURSE CLASS DEFINITION=============================
def getClass(courseCode):
	return classes.query.filter_by(course_code=courseCode).first()

# returns a list of all class objects
def getAllClasses():
	return classes.query.all()

def classList():
	x = getAllClasses()
	r = {}
	for i in x:
		r[i.course_code] = i.course_name
	return r

def csvEater():
	with open("data/Class-List1.csv") as csvfile:
		reader = csv.reader(csvfile)
		prevClass = ''
		sectionHolder = {}
		newClass = classes('','',1)
		for row in reader:
			if row[0] == 'Course Code':
				pass
			else:
				if prevClass != row[0]:
					# newClass.sections = json.dumps(sectionHolder)
					db.session.add(newClass)
					sectionHolder = {}
					newClass = classes(row[0],row[2],31)
					prevClass = row[0]
				else:
					sectionHolder[row[1]] = {"teacher":row[3],"room":'',"roster":[]}
		newClass.sections = json.dumps(sectionHolder)
		db.session.add(newClass)
		db.session.commit()
# ============================START OF HELPER FUNCTIONS=============================
# ============================END OF HELPER FUNCTIONS=============================

# ============================START OF ROUTING=============================
@app.route("/")
def home():
	if 'username' in session:
		return render_template("student_dash.html")
	else:
		return render_template("home.html")

@app.route("/auth", methods=["GET","POST"])
def auth():
	print request.form
	osis = request.form.get("osis")
	pwd = request.form.get("pwd")
	st = getStudent(osis)
	if str(osis) == str(st.osis) and str(hash(pwd)) == str(st.pw): # if inputed osis & pwd is same as in db
		print "success"
		session['username'] = osis
		return render_template("student_dash.html")
	else:
		print "failed login"
		flash("Login failed") #does not yet flash
		return redirect(url_for("home"))

@app.route("/student")
def student_dash():
	cla = classList()
	return render_template("student_dash.html", classes = cla)

	#
	# @app.route("/about")
	#
	# # <int:student_id>
	# #the student dashboard
	# @app.route("/<int:student_id>")
	# @app.route("/<int:student_id>/pchange")
	# @app.route("/<int:student_id>/cselect")
	# @app.route("/<int:student_id>/transcript")
	# @app.route("/<int:student_id>/reportcard")
	# @app.route("/<int:student_id>/accountsettings")
	# @app.route("/<int:student_id>/pw")
	#
	# #the admin dashboard
	# @app.route("/<int:admin_id>/")
	# #How much detail is needed for studentView?
	# @app.route("/<int:admin_id>/studentView")
	# @app.route("/<int:admin_id>/courseView")
	# @app.route("/<int:admin_id>/adminsettings")
	# @app.route("/<int:admin_id>/adminpw")
	# @app.route("/<int:admin_id>/admindata")
	# @app.route("/<int:admin_id>/admininbox")
	#

@app.route("/select_courses")
def choose_courses():
	cla = classList()
	return render_template("course_selection.html", classes = cla)

# @app.route("/logout")
# def logout():
#     session.pop("username")
#   return render_template("home.html")


@app.route("/transcript")
def show_grades():
	return render_template("transcript.html")


@app.route("/all_courses")
def show_courses():
	return render_template("courses.html")

@app.route("/student_settings")
def student_settings():
	return render_template("student_settings.html")

@app.route("/elecChoice", methods=["POST"])
def elecChoice():
	print request.form.keys()
	a = {}
	for key in request.form.keys():
		st = request.form.get(key)
		st = st.split(":")
		a[ st[0] ] = st[1]
	print a
	return a

@app.route("/admin")
def admin_dash():
	return render_template("admin_dash.html")

@app.route("/student_selections")
def student_selections():
	return render_template("student_selections.html")

@app.route("/admin_settings")
def admin_settings():
	return render_template("admin_settings.html")

@app.route("/admin_all_courses")
def show_admin_courses():
	return render_template("admin_all_courses.html")
# ============================END OF ROUTING=============================

if __name__ == "__main__":
	db.create_all()

	newstudent = students(1111,'21','savage',pow="issa")
	if (getStudent(1111) is not None):
		print "Student already exists. Not creating."
	else:
		db.session.add(newstudent)
		print "Student %s created"%(newstudent.fname)
		db.session.commit()

	print "Done."
	# csvEater()
	app.run(debug = True, use_reloader= True)
