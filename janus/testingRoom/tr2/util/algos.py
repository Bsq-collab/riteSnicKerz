# gives the student rank for determining whether he or she gets an elective or not
def rank(ovrAvg, subAvg, tRec):
    return (float(ovrAvg) * .4 + float(subAvg) * .4 + float(tRec) * .2) * 100

# chooses the optimal class for each period that minimizes collateral damage (or minimizing the number of periods that lose a class)
def optC(classList, classPds, currentPd):
    # given 2D array
    c = [0 for i in range(len(classList))]
    for i in classPds:
        for f in i:
            c[classList.indexOf(f)] += 1
    return c[c.indexOf(min(c))]

def schedulize(classList, pd, schedule, currentPd):
    if currentPd == 10:
        return
    else:
        # pd = getPds(classList)
        # given list returned from getPds
        # check whether there are any periods of one
        r = [] # array of classes that can only be in one period
        for i in pd: # performs check for classes that can only be in one period
            if len(i) == 1:
                schedule[pd.indexOf(i)] = i[0] # puts the class into the period
                r.append(i[0])
        # removes all classes that can only be in one period
        for i in pd:
            for f in r:
                if f in i:
                    i.remove(f)
        # optC = optC(classList, pd, currentPd)
        # remove optC from all lists
        for i in pd:
            if optC in i:
                i.remove(optC)
        return schedulize(classList, pd, schedule, currentPd + 1)

def schedule(classList, pds):
    schedule = ['' for i in range(10)]
    schedulize(classList, pds, schedule, 1)
    t = reduce( (lambda x,y: len(x) + len(y)), pds)
    s = filter( (lambda x: x != ''), schedule)
    s = len( s )
    if t != len(schedule): #schedule conflict
        return False
    else:
        return schedule
