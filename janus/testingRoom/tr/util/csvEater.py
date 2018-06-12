import csv


def csvEater():
	with open("NewClassList.csv") as csvfile:
		reader = csv.reader(csvfile)
		prevClass = ''
		for row in reader:
			if row[0] == 'Course Code':
				pass
			else:
				if prevClass != row[0]:
					db.session.add(newClass)
					newClass = classes(row[0], row[2])
					prevClass = row[0]
				else:
					sectionHolder[row[1]] = {"teacher":row[3],"room":'',"roster":[]}
		db.session.add(newClass)
		db.session.commit()

