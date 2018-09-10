import os
os.chdir("../")

# Format Individual Data
# NEED TO SET TO SUBFOLDERS
path = "IndividualData/ind2015er/"
folderpath = os.getcwd() +"\IndividualData\ind2015er"
readpath = path + "IND2015ER.do"
writepath = path + "IND2015ERnew.do"
with open(readpath, "r") as file:
    fix = file.read()
    fix = fix.replace('[path]\\', '')
with open(writepath, "w") as file:
    file.write("cd " + folderpath)
    file.write(fix)
    file.write("\nsave ..\individual, replace;")

# Format Child History Data
path = "ChildHistoryData/CAH85_15/"
folderpath = os.getcwd() +"\ChildHistoryData\CAH85_15"
readpath = path + "CAH85_15.do"
writepath = path + "CAH85_15new.do"
with open(readpath, "r") as file:
    fix = file.read()
    fix = fix.replace('[path]\\', '')
with open(writepath, "w") as file:
    file.write("cd " + folderpath)
    file.write(fix)
    file.write("\nsave ..\childhistory, replace;")


# Format Family Data
for y in range(1999, 2017, 2):
    yr = str(y)
    path = "FamilyData/fam{}er".format(yr)
    readpath = path + "/FAM{}ER.do".format(yr)
    writepath = path + "/FAM{}ERnew.do".format(yr)
    with open(readpath ,"r") as file:
        fix = file.read()
        fix = fix.replace('[path]\\', '')
    with open(writepath ,"w") as file:
        file.write(fix)

master = open("FamilyData/formatfam1.do", "w")
famfolder = os.getcwd() +"\FamilyData"
master.write("cd " + "\"" + famfolder + "\"\n")
master.write("set maxvar 10000 \n")
master.write("forval i = 1999(2)2015{ \n")
master.write("cd " +  "\"" + famfolder + "\FAM`i'er\" \n" )
master.write("do \"FAM`i'ERnew.do\" \n")
master.write("save \"../fam`i'.dta\", replace \n")
master.write("}")
master.close()

# Format Wealth Data
for y in range(1999, 2009, 2):
    yr = str(y)
    path = "WealthData/wlth{}".format(yr)
    readpath = path + "/wlth{}.do".format(yr)
    writepath = path + "/wlth{}new.do".format(yr)
    with open(readpath ,"r") as file:
        fix = file.read()
        fix = fix.replace('[path]\\', '')
    with open(writepath ,"w") as file:
        file.write(fix)

master = open("WealthData/formatwealth1.do", "w")
wealthfolder = os.getcwd() +"\WealthData"
master.write("cd " + "\"" + wealthfolder + "\"\n")
master.write("set maxvar 10000 \n")
master.write("forval i = 1999(2)2015{ \n")
master.write("cd " +  "\"" + wealthfolder + "\wlth`i'\" \n" )
master.write("do \"wlth`i'new.do\" \n")
master.write("save \"../wlth`i'.dta\", replace \n")
master.write("}")
master.close()

# master do file
with open("format_data.do", "w") as file:
    file.write("cd " + os.getcwd() + "\n")
    # individual data
    file.write("do IndividualData\ind2015er\IND2015ERnew.do" + "\n")
    # child history data
    file.write("do ChildHistoryData\CAH85_15\CAH85_15new.do" + "\n")
    # family data
    file.write("do FamilyData\\formatfam1.do" + "\n")
    # wealth data
    file.write("do WealthData\\formatwealth1.do")
