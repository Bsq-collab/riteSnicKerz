import os,csv,json, random
from util import algos
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
	avg = db.Column(db.Float(100))
	subAvgs = db.Column(db.String(1000))

	def __init__(self, osis, fname, lname, classYr = 1, legitSchedule = '', pow='', APcount = 0, electiveCount = 0, avg = 90):
		self.osis = osis
		self.fname = fname
		self.lname = lname
		self.pw = str(hash(pow))
		self.classYr = classYr
		self.legitSchedule = legitSchedule
		self.APcount = APcount
		self.electiveCount = electiveCount
		self.avg = avg
		self.subAvgs = 'MPS22: 90'

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

	def appendSchedule(self, cla):
		self.schedule.append(cla)

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
	roster = db.relationship('students',secondary=studentclass,backref=db.backref('schedule'))
	class_type = db.Column(db.String(10))
	#upperClass - Use this to access the umbrella class for the section.

	def __init__(self, section_id, teach, pd):
		self.section_id = section_id
		#self.class_code = code
		self.teacher = teach
		self.period = pd

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
	class_type = db.Column(db.String(20))


	def __init__(self, code, name,class_type="normal", dept = '', studnPC = 30, studn =100, preReqs = ''):
		self.students_per_class = studnPC
		self.max_students = studn
		self.class_code = code
		self.class_name = name
		self.dept = dept
		#self.description = descr
		self.preReqs = preReqs
		self.class_type = class_type

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

	def getSection(self,num):
		for i in self.sections:
			if i.period == num:
				return i
		print "AAAAAAAAAAAAAAHHH - get Section"
		return None

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
			a = classes.getClass(i)
			print "printing sections"
			# print a.sections
			for sec in a.sections:
				# print "printing sec"
				# print sec.period
				ret2D[sec.period - 1].append(a.class_code)
		return ret2D


	@staticmethod
	def getAPs():
		cl = classes.query.all()
		# print "cl", cl
		r = {}
		for i in cl:
			# print i.class_name
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
def csvEater():
	with open("data/NewClassList.csv") as csvfile:
		reader = csv.reader(csvfile)
		prevClass = ''
		sectionHolder = sections(0,'',0)
		newClass = classes('','',1)
		for row in reader:
			if row[0] == 'Course Code':
				pass
			else:
				if prevClass != row[0]:
					db.session.add(newClass)
					newClass = classes(row[0], row[2], row[5])
					sectionHolder = sections(row[1],row[3],row[6])
					newClass.sections.append(sectionHolder)
					prevClass = row[0]
				else:
					sectionHolder = sections(row[1],row[3],row[6])
					newClass.sections.append(sectionHolder)
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
	def __init__(self,fName,lName,position, admin_id, ballin, pw="admin"):
		self.fName = fName
		self.lName = lName
		self.pw = hash(pw)
		self.position = position
		self.can_program_change = ballin
		self.admin_id = admin_id
		# temp = fName[0]+lName
		# self.admin_id = temp.upper()
		print("Admin %s has been created"%(lName))

	@staticmethod
	def getAdmin(iid):
		return admins.query.filter_by(admin_id=iid).first()

	def changePW(self,newpass):
		self.pw = hash(newpass)

	def checkPW(self,password):
		return hash(password)==self.pw


# ===============================END OF NEW CLASS DEFINITIONS==============================================

# ============================START OF ROUTING=============================

@app.route("/debug")
def debug():
	currentStudent = students.getStudent(1111)
	x = currentStudent.applied_classes
	bc = currentStudent.applied_classes
	print "============================================================"
	print bc
	print "============================================================"
	ac = [i.class_code for i in bc]
	print "==============================applied classes=============================="
	print ac
	print "=================================================================="
	cc = classes.schedulePds(ac)
	print "================================pds schedule============================"
	print cc
	print "=================================================================="
	s = algos.schedule(ac, cc)
	print "================================schedule============================"
	print s
	print "=================================================================="
	# print x
	# for i in x:
	# 	print i.class_code
	# # for i in x:
	# # 	print i.class_code
	print "===========================================PRINT======================="
	# db.session.commit()
	return "Hello"

@app.route("/")
def home():
	if 'username' in session and session['pwr'] == 'student':
		st = students.getStudent(session['username'])
		return render_template("student/student_dash.html", schedule = json.dumps(st.schedule))
	elif 'username' in session and session['pwr'] == 'admin':
		return render_template("admin/admin_dash.html")
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
		session['pwr'] = 'student'
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
	l = courseChoice(ma)
	c.electiveCount = c.electiveCount - l
	db.session.commit()
	redirect(url_for("home"))

@app.route("/apChoice", methods=["POST"])
def apChoice():
	c = students.getStudent(session['username'])
	ma = c.APcount
	l = courseChoice(ma)
	c.APcount = c.APcount - l
	db.session.commit()
	return redirect(url_for("home"))

def courseChoice(maxx):
	if maxx <= 0:
		return 0
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
		# student.apply_to_class(c)
		# print c.get_applicant_pool()
	return len(a)


# ============================ADMIN ROUTES =============================
@app.route("/admin")
def admin_dash():
	return render_template("admin/admin_dash.html")

@app.route("/student_selections")
def student_selections():
	return render_template("admin/student_selections.html")

@app.route("/authAdmin", methods=["GET","POST"])
def authAdmin():
	print request.form
	usr = request.form.get("usr")
	pwd = request.form.get("pwd")
	st = admins.getAdmin(usr)
	if str(usr) == str(st.admin_id) and str(hash(pwd)) == str(st.pw): # if inputed osis & pwd is same as in db
		print "success"
		session['username'] = usr
		session['pwr'] = 'admin'
		return redirect(url_for("home"))
	else:
		print "failed login"
		return redirect(url_for("home"))

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
@app.route("/schedule")
def schedule():
	allClasses = classes.getAllClasses()
	for cl in allClasses:
		q = {}
		# print "================applicant pool============================================"
		# print cl.applicant_pool
		# print "============================================================"
		a = []
		if len(cl.applicant_pool) != 0:
			print "cl", cl.applicant_pool
			for st in cl.applicant_pool:
				q[algos.rank(st.avg, 90, 0 )] = st
			r = q.keys()
			r.sort(reverse=True) #sort applicant pool
			# print r
			for i in r:
				a.append(q[i]) #creates a list of student objects sorted
			cl.set_applicant_pool(a)
		db.session.commit()
		# # done ranking students
		appPool = cl.get_applicant_pool()
		s = []
		for i in range( min(cl.max_students, len(cl.applicant_pool)) ):
			currentStudent = appPool[i]
			bc = currentStudent.applied_classes
			ac = [i.class_code for i in bc]
			cc = classes.schedulePds(ac)
			print "============================================================"
			print bc
			print "============================================================"
			print "==============================applied classes=============================="
			print ac
			print "=================================================================="
			print "================================pds schedule============================"
			print cc
			print "=================================================================="
			print "================================schedule============================"
			s = algos.schedule(ac, cc)
			print "=================================================================="

		if (s != False):
			counter = 0
			for clcode in s:
				if clcode=='' or clcode==[]:
					counter+=1
					pass
				else:
					c = classes.getClass(clcode)
					sec = c.getSection(counter+1)
					print counter+1
					counter+=1
					currentStudent.appendSchedule(sec)

				# print "curreijaowdi", currentStudent.schedule
				# currentStudent.legitSchedule = json.dumps(s)
		else:
			print "schedule conflict"
			# print s
	db.session.commit()
	#print students.getStudent(1111).schedule
	return "IT WORKED"

# @app.route("/logout")
# def logout():
#     session.pop("username")
#   return render_template("login.html")

# ============================END OF ROUTING=============================

if __name__ == "__main__":
	db.create_all()
	if (len(classes.getAllClasses()) == 0):
		print "Creating classes"
		csvEater()
	else:
		print "Classes already exist"
	newstudent = students(1111,'21','savage',pow="issa", APcount = 3)
	if (students.getStudent(1111) is not None):
		print "Student already exists. Not creating."
	else:
		db.session.add(newstudent)
		print "Student %s created"%(newstudent.fname)
	# bloop = classes.getClass("FMS62")
	# print bloop.sections
	db.session.commit()
	print "Done."
	app.run(debug = True, use_reloader= False)
