import pandas as pd
import numpy as np
import copy
def categories(crosswalk, clist):
    subset = copy.deepcopy(crosswalk)
    for i in range(0, len(clist)):
        lowercase = subset['C' + str(i)].str.lower()
        cond = lowercase.str.startswith(clist[i])
        subset = copy.deepcopy(subset[cond])
    return subset

def availableyears(crosswalk, clist, minyear = 1968, maxyear = 2015):
    ndf = categories(crosswalk, clist)
#     all year columns
    ylist = [x for x in ndf.columns if x.startswith('Y')]
#     only year columns in range
    rlist = [x for x in ylist if int(x[1:]) in range(minyear, maxyear + 1)]
    for i in ndf.index:
        print('ROW ' + str(i))
        rdf = ndf[rlist]
        notmissing = [x for x in rdf if rdf.loc[i, x] != 'missing']
        print(ndf[notmissing].columns)

def findseries(crosswalk, varname):
    ylist = [x for x in crosswalk.columns if x.startswith('Y')]
    df= crosswalk[ylist]
    catlist = [x for x in crosswalk.columns if x.startswith('C')]
    return crosswalk[df.values == 'ER60163'][catlist]

def subcategories(crosswalk, clist):
    subset = categories(crosswalk, clist)
    i = len(clist)
    return subset['C' + str(i + 1)].unique()

def edit_dofiles():
#     This function removes the [path]\ string from .do files to facilitate running a master .do file
    for y in range(1999, 2017, 2):
        path = "FamilyData/famxxxxer/FAMxxxxER.do".replace("xxxx", str(y))
        writepath = "FamilyData/famxxxxer/FAMxxxxERnew.do".replace("xxxx", str(y))
        with open(path ,"r") as file:
            fix = file.read()
            fix = fix.replace('[path]\\', '')
        with open(writepath ,"w") as file:
            file.write(fix)
    for y in range(1999, 2009, 2):
        path = "WealthData/wlthxxxx/wlthxxxx.do".replace("xxxx", str(y))
        writepath = "WealthData/wlthxxxx/wlthxxxxnew.do".replace("xxxx", str(y))
        with open(path ,"r") as file:
            fix = file.read()
            fix = fix.replace('[path]\\', '')
        with open(writepath ,"w") as file:
            file.write(fix)
