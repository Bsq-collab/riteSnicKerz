import os,csv, json
from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = os.urandom(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/school.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ============================START OF SQLALCHEMY STUDENT CLASS DEFINITION=============================
class students(db.Model):
	id = db.Column('useless_id',db.Integer,primary_key=True)
	osis = db.Column(db.Integer)
	fname = db.Column(db.String(20))
	lname = db.Column(db.String(20))
	pw = db.Column(db.String(20))
	APcount = db.Column(db.Integer)
	electiveCount = db.Column(db.Integer)
	avg = db.Column(db.String(200))
	#avg must be a json in the following format: {ovrAvg: ??, dept: [class1: avg, class2: avg]}
	def __init__(self, osis, fname, lname, APcount = 0, electiveCount = 0, pow='', avg = ''):
		self.osis = osis
		self.fname = fname
		self.lname = lname
		self.APcount = APcount
		self.electiveCount = electiveCount
		self.pw = str(hash(pow))
		self.avg = avg

	# def getStudent(self,od):
	# 	return self.query.filter_by(osis=od).first()

	# #PW FXNS
	# def getPW(self, os):
	# 	return self.query.filter_bystr(self.pw)
	#
	# def modPW(self,unhash):
	# 	self.pw = str(hash(unhash))

# ============================ACCESSOR & MUTATORS FOR STUDENT CLASS=============================
def getStudent(osis):
	st = students.query.filter_by(osis=osis).first()
	# print st.fname
	return st

# def getAPcount(osis):
# 	st = getStudent(osis)
# 	return st.APcount

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


# ============================END OF SQLALCHEMY COURSE CLASS DEFINITION=============================
def getClass(courseCode):
	return classes.query.filter_by(course_code=courseCode).first()

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
					newClass.sections = json.dumps(sectionHolder)
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
	return render_template("student_dash.html")

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
    return render_template("course_selection.html")

# @app.route("/logout")
# def logout():
#     session.pop("username")
# 	return render_template("home.html")


@app.route("/transcript")
def show_grades():
    return render_template("transcript.html")


@app.route("/all_courses")
def show_courses():
    return render_template("courses.html")

@app.route("/student_settings")
def student_settings():
    return render_template("student_settings.html")

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
	csvEater()
	app.run(debug = True, use_reloader=False)
