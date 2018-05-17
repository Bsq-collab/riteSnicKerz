#!usr/bin/python

from flask import Flask, session, render_template, request, redirect, url_for, flash

app = Flask(__name__)

@app.route("/")
def landing:
	pass

@app.route("/registration")
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


if __name__ == "__main__":
    app.debug = True
    app.run()