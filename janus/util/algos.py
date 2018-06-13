# gives the student rank for determining whether he or she gets an elective or not
def rank(ovrAvg, subAvg, tRec):
    return (float(ovrAvg) * .4 + float(subAvg) * .4 + float(tRec) * .2) * 100

# chooses the optimal class for each period that minimizes collateral damage (or minimizing the number of periods that lose a class)
def optC(classList, classPds, currentPd):
    # given 2D array
    c = [0 for i in range(len(classList))]
    for i in classPds:
        for f in i:
            if f in c:
                c[classList.index(f)] += 1
    return classList[c.index(min(c))]

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
                schedule[pd.index(i)] = i[0] # puts the class into the period
                r.append(i[0])
                if i[0] in classList:
                    classList.remove(i[0])
        # removes all classes that can only be in one period
        # print "r", r
        # print "classList", classList
        for i in pd:
            for f in r:
                if f in i:
                    i.remove(f)
        if len(classList) == 0:
            # print "algo pd", pd
            return
        optc = optC(classList, pd, currentPd)
        # print "optc", optc
        # print "schedule", schedule
        # remove optC from all lists
        for i in pd:
            # print i
            if optc in i:
                # print "i", i
                i.remove(optc)
        classList.remove(optc)
        schedule[currentPd] = optc
        return schedulize(classList, pd, schedule, currentPd + 1)

def schedule(classList, pds):
    schedule = ['' for i in range(10)]
    # print "pds", pds
    schedulize(classList, pds, schedule, 1)
    # print pds
    # t = reduce( (lambda x,y: x + y), pds)
    t = 0
    for p in pds:
        t += len(p)
    # s = filter( (lambda x: x != ''), schedule)
    s =  [i for i in schedule if i != '']
    s = len( s )
    print 't', t
    # print 's', s
    # print schedule
    # print "pds after", pds
    if t != 0: #schedule conflict
        return False
    else:
        return schedule
