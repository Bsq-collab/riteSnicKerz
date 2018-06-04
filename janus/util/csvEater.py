import csv, sqlite3

f = "../data/school.sqlite3"
db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops
command= "CREATE TABLE (username TEXT, password TEXT)"
c.execute(command)
    
with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader: