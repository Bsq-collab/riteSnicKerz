import csv

fin = "../data/Class-List1.csv"
fout = "../data/Class-ListOut.csv"  
allcopy = []
with open(fout) as csvout:
    with open(fin) as csvin:
        reader = csv.reader(csvin)
        writer = csv.writer(csvout)
        for row in reader:
            allcopy.append(row)
            
print allcopy
