def getItem(tabl, od):
	gotee = tabl.query.filter_by(id=od).first()
	print gotee.fname
	return 0