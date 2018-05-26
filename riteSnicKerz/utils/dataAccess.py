def getStudent(od):
	gotee = students.query.filter_by(id=od).first()
	print gotee.fname
	return 0