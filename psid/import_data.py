import os
os.chdir("../")

endyear = 2017
end_str = str(endyear)

# Format Individual Data
# NEED TO SET TO SUBFOLDERS
path = "IndividualData/ind{}er/".format(end_str)
folderpath = os.getcwd() +"\IndividualData\ind{}er".format(end_str)
readpath = path + "IND{}ER.do".format(end_str)
writepath = path + "IND{}ERnew.do".format(end_str)
with open(readpath, "r") as file:
    fix = file.read()
    fix = fix.replace('[path]\\', '')
with open(writepath, "w") as file:
    file.write("cd " + folderpath)
    file.write(fix)
    file.write("\nsave ..\individual, replace;")

# Format Child History Data
path = "ChildHistoryData/cah85_{}/".format(end_str[-2:])
folderpath = os.getcwd() +"\ChildHistoryData\cah85_{}".format(end_str[-2:])
readpath = path + "CAH85_{}.do".format(end_str[-2:])
writepath = path + "CAH85_{}new.do".format(end_str[-2:])
with open(readpath, "r") as file:
    fix = file.read()
    fix = fix.replace('[path]\\', '')
with open(writepath, "w") as file:
    file.write("cd " + folderpath)
    file.write(fix)
    file.write("\nsave ..\childhistory, replace;")


# Format Family Data
for y in range(1999, endyear + 2, 2):
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
master.write("#delimit ; \n")
master.write("forval i = 1999(2)2015{; \n")
master.write("cd " +  "\"" + famfolder + "\FAM`i'er\"; \n" )
master.write("do \"FAM`i'ERnew.do\"; \n")
master.write("save \"../fam`i'.dta\", replace; \n\n")
master.write("};")
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
master.write("#delimit ; \n")
master.write("forval i = 1999(2)2007{; \n")
master.write("cd " +  "\"" + wealthfolder + "\wlth`i'\"; \n" )
master.write("do \"wlth`i'new.do\"; \n")
master.write("save \"../wlth`i'.dta\", replace; \n\n")
master.write("};")
master.close()

# master do file
with open("format_data.do", "w") as file:
    # family data
    file.write("clear \n")
    file.write("cd " + os.getcwd() + "\n")
    file.write("do FamilyData\\formatfam1.do" + "\n")
    # wealth data
    file.write("clear \n")
    file.write("cd " + os.getcwd() + "\n")
    file.write("do WealthData\\formatwealth1.do \n")
    # individual data
    file.write("cd " + os.getcwd() + "\n")
    file.write(
        "do IndividualData\ind{}er\IND{}ERnew.do"
        .format(end_str, end_str) + "\n")
    # child history data
    file.write("cd " + os.getcwd() + "\n")
    file.write(
        "do ChildHistoryData\cah85_{}\CAH85_{}new.do"
        .format(end_str[-2:], end_str[-2:]) + "\n")
    file.close()
