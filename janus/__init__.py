import os,csv,json
#from util import algos
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
	classYr = db.Column(db.Integer())
	#classSections - will give you list of class sections that student is in. Need to go up one more in order to access class itself.
	#schedule - will give you list of class sections that student is in. Need to go up one more in order to access class itself.
	legitSchedule = db.Column(db.String(1000))
	fname = db.Column(db.String(20))
	lname = db.Column(db.String(20))
	pw = db.Column(db.String(20))
	APcount = db.Column(db.Integer)
	electiveCount = db.Column(db.Integer)
	coreClassCount = db.Column(db.Integer)
	#avg must be a json in the following format: {ovrAvg: ??, dept: [class1: avg, class2: avg]}
	avg = db.Column(db.String(1000))
	subAvgs = db.Column(db.String(1000))

	def __init__(self, osis, fname, lname, classYr = 1, legitSchedule = '', pow='', APcount = 0, electiveCount = 0, avg = ''):
		self.osis = osis
		self.fname = fname
		self.lname = lname
		self.pw = str(hash(pow))
		self.classYr = classYr
		self.legitSchedule = legitSchedule
		self.APcount = APcount
		self.electiveCount = electiveCount
		self.avg = avg
		self.subAvgs = ''

	def UpdateAPcount(self):
		if self.avg >= 95.0:
			self.APcount = 4
		elif self.avg >= 93.0:
			self.APcount = 3
		elif self.avg >= 88.0:
			self.APcount = 2
		else:
			self.APcount = 1

	def UpdateCoreCount(self):
		if self.classYr == 4:
			self.coreClassCount = 4
		else:
			self.coreClassCount = 7

	def UpdateElectiveCount(self):
		self.electiveCount = 10 - self.coreClassCount - self.APcount

	def UpdateClassCount(self):
		self.UpdateCoreCount()
		self.UpdateAPcount()
		self.UpdateElectiveCount()
		db.session.commit()

	def setAvg(self, newAvg):
		prev = self.avg
		self.avg = newAvg
		return prev

	#takes a dictionary in this format: {'courseCode': float(avg)}
	def setSubAvg(self, subD):
		prev = self.subAvgs
		self.subAvgs = json.dumps(subD)
		return json.loads(subD)

	#returns a dictionary in above stated format
	def getSubAvg(self):
		return json.loads(self.subAvgs)

	#get specific class avg
	def getSpecSubAvg(self, cl):
		n = self.getSubAvg()
		return n[cl]

	def setLegitSchedule(self, newLS):
		prev = self.legitSchedule
		self.legitSchedule = newLS
		return prev

	#applied_classes - classes applied to
	def apply_to_class(self,newClass):
		self.applied_classes.append(newClass)
		db.session.commit()

	@staticmethod
	def getStudent(os):
		return students.query.filter_by(osis=os).first()

class sections(db.Model):
	id = db.Column('sectionID',db.Integer,primary_key=True)
	section_id = db.Column(db.Integer())
	class_code = db.Column(db.String(10),db.ForeignKey("classes.class_code"))
	teacher = db.Column(db.String(20))
	period = db.Column(db.Integer())
	roster = db.relationship('students',secondary=studentclass,backref=db.backref('classSections'))
	#upperClass - Use this to access the umbrella class for the section.

	def __init__(self, section_id, code, teach):
		self.section_id = section_id
		self.class_code = code
		self.teacher = teach

	#Mutator/Appender for roster
  	def add_to_roster(self,osis):
  		self.roster.append(students.getStudent(osis))

class classes(db.Model):
	id = db.Column('classID',db.Integer,primary_key=True)
	sections = db.relationship("sections",backref="upperClass",lazy = True)
	max_students = db.Column(db.Integer())
	students_per_class = db.Column(db.Integer())
	class_code = db.Column(db.String(10))
	class_name = db.Column(db.String(20))
	description = db.Column(db.String(1000))
	dept = db.Column(db.String(500))
	applicant_pool = db.relationship("students",secondary=applicantclass,backref=db.backref('applied_classes'),lazy=True)
	preReqs = db.Column(db.String(1000))

	def __init__(self, code, name, dept = '', studnPC = 30, studn =100, descr='', preReqs = ''):
		self.students_per_class = studnPC
		self.max_students = studn
		self.class_code = code
		self.class_name = name
		self.dept = dept
		self.description = descr
		self.preReqs = preReqs

	@staticmethod
	def getClass(coode):
		return classes.query.filter_by(class_code = coode).first()

	def append_to_applicant_pool(self,newStudent):
		if newStudent not in self.applicant_pool:
			self.applicant_pool.append(newStudent)

	def set_applicant_pool(self,pool):
		self.applicant_pool = pool

	def get_applicant_pool(self):
		return self.applicant_pool

	def setDept(self, dep):
		prev = self.dept
		self.dept = dep
		return prev

	def setPreReqs(self, preR):
		prev = self.preReqs
		self.preReqs = preR
		return prev

	def getPreReqs(self):
		return self.preReqs

	#takes a list of class codes
	@staticmethod
	def schedulePds(cls):
		ret2D = []
		for i in range(10):
			ret2D.append([])
		for i in cls:
			a = getClass(i)
			for sec in a.sections:
				ret2D[sec.pd - 1].append(a)
		return ret2D


	@staticmethod
	def getAPs():
		cl = classes.query.all()
		# print "cl", cl
		r = {}
		for i in cl:
			print i.class_name
			if 'X' in i.class_code:
				r[i.class_code] = i.class_name
		return r

	@staticmethod
	# returns a list of all class objects
	def getAllClasses():
		return classes.query.all()

	@staticmethod
	def classList():
		x = getAllClasses()
		r = {}
		for i in x:
			r[i.class_code] = i.class_name
		return r

# def __init__(self, code, name, max_students, descr=''):
# need to fix csvEater to have relationship working
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
					newClass = classes(row[0], row[2])
					prevClass = row[0]
				else:
					sectionHolder[row[1]] = {"teacher":row[3],"room":'',"roster":[]}
		# newClass.sections = json.dumps(sectionHolder)
		db.session.add(newClass)
		db.session.commit()


class admins(db.Model):
	id = db.Column('adminID',db.Integer,primary_key=True)
	admin_id = db.Column(db.String(20))
	pw = db.Column(db.String(20))
	fName = db.Column(db.String(30))
	lName = db.Column(db.String(30))
	position = db.Column(db.String(30))
	an_program_change = db.Column(db.Boolean())
	def __init__(self,fName,lName,position,ballin,pw="admin"):
		self.fName = fName
		self.lName = lName
		self.pw = hash(pw)
		self.position = position
		self.can_program_change = ballin
		temp = fName[0]+lName
		self.admin_id = temp.upper()
		print("Admin %s has been created"%(lName))

	def changePW(self,newpass):
		self.pw = hash(newpass)

	def checkPW(self,password):
		return hash(password)==self.pw

# ===============================END OF NEW CLASS DEFINITIONS==============================================

# ============================START OF ROUTING=============================

@app.route("/debug")
def debug():

	# newClass = classes("MKS22X","CALC AB")
	#
	# db.session.add(newClass)
	#
	currentStudent = students.getStudent(session['username'])
	#
	# currentStudent.apply_to_class(newClass)
	#
	x = currentStudent.applied_classes
	# x = classes.schedulePds(currentStudent.applied_classes
	print "===========================================PRINT======================="
	print x
	# for i in x:
	# 	print i.class_code
	print "===========================================PRINT======================="
	# db.session.commit()
	return "Hello"

@app.route("/")
def home():
	if 'username' in session:
		return render_template("student/student_dash.html")
	else:
		return render_template("guess/login.html")

@app.route("/auth", methods=["GET","POST"])
def auth():
	print request.form
	osis = request.form.get("osis")
	pwd = request.form.get("pwd")
	st = students.getStudent(osis)
	if str(osis) == str(st.osis) and str(hash(pwd)) == str(st.pw): # if inputed osis & pwd is same as in db
		print "success"
		session['username'] = osis
		st.UpdateClassCount()
		return redirect(url_for("home"))
	else:
		print "failed login"
		return redirect(url_for("home"))

@app.route("/transcript")
def show_grades():
	return render_template("student/transcript.html")

@app.route("/all_courses")
def show_courses():
	return render_template("student/courses.html")

@app.route("/student_settings")
def student_settings():
	return render_template("student/student_settings.html")

@app.route("/select_electives")
def select_electives():
	cla = classes.classList()
	return render_template("student/elective_selection.html", classes = cla)

@app.route("/select_aps")
def select_aps():
	aps = classes.getAPs()
	return render_template("student/ap_selection.html", APs = aps)

@app.route("/elecChoice", methods=["POST"])
def elecChoice():
	c = students.getStudent(session['username'])
	ma = c.electiveCount
	courseChoice(ma)
	redirect(url_for("home"))

@app.route("/apChoice", methods=["POST"])
def apChoice():
	c = students.getStudent(session['username'])
	ma = c.APcount
	courseChoice(ma)
	return redirect(url_for("home"))

def courseChoice(maxx):
		a = []
		for key in request.form.keys():
			st = request.form.get(key)
			if st != "N/A":
				st = st.split(":")
				if st[0] not in a:
					a.append(st[0])
		a = a[:maxx]
		# print a
		student = students.getStudent(session['username'])
		for i in range(len(a)):
			c = classes.getClass(a[i])
			c.append_to_applicant_pool(student)
			db.session.commit()
			# student.apply_to_class(c)
			print c.get_applicant_pool()


# ============================ADMIN ROUTES =============================
@app.route("/admin")
def admin_dash():
	return render_template("admin/admin_dash.html")

@app.route("/student_selections")
def student_selections():
	return render_template("admin/student_selections.html")

@app.route("/admin_settings")
def admin_settings():
	return render_template("admin/admin_settings.html")

@app.route("/admin_all_courses")
def show_admin_courses():
	a = classes.getAllClasses()
	clas = []
	for cl in a:
		clas.append( {"code": cl.class_code, "name": cl.class_name, "description": cl.description})
	return render_template("admin/admin_all_courses.html", classs = clas)

# goes through all classes and ranks and schedules all students
# @app.route("/schedule")
# def schedule():
# 	allClasses = classes.getAllClasses()
# 	for cl in allClasses:
# 		q = {}
# 		for st in cl.applicant_pool:
# 			q[rank(st.ovrAvg, st.getSpecSubAvg(cl.preReqs), 0 )] = st
# 			r = q.keys()
# 			r = r.sort(reverse=True) #sort applicant pool
# 			a = []
# 			for i in r:
# 				a.append(r[i]) #creates a list of student objects sorted
# 			cl.set_applicant_pool(a)
# 		# done ranking students
# 		appPool = cl.get_applicant_pool()
# 		for i in range(cl.max_students):
# 			currentStudent = appPool[i]
# 			s = algos.schedule(currentStudent.applied_classes, classes.schedulePds(currentStudent.applied_classes))
# 			print "============================================================"
# 			print s
# 			print "============================================================"
# 	return "hi"
#
# @app.route("/logout")
# def logout():
#     session.pop("username")
#   return render_template("login.html")

# ============================END OF ROUTING=============================

if __name__ == "__main__":
	db.create_all()
	csvEater()
	newstudent = students(1111,'21','savage',pow="issa", APcount = 3)
	if (students.getStudent(1111) is not None):
		print "Student already exists. Not creating."
	else:
		db.session.add(newstudent)
		print "Student %s created"%(newstudent.fname)
	db.session.commit()
	print "Done."
	app.run(debug = True, use_reloader= False)
