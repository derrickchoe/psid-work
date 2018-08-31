import os
os.chdir("../")

# Format Family Data
for y in range(1999, 2017, 2):
    path = "FamilyData/famxxxxer/FAMxxxxER.do".replace("xxxx", str(y))
    writepath = "FamilyData/famxxxxer/FAMxxxxERnew.do".replace("xxxx", str(y))
    with open(path ,"r") as file:
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
    path = "WealthData/wlthxxxx/wlthxxxx.do".replace("xxxx", str(y))
    writepath = "WealthData/wlthxxxx/wlthxxxxnew.do".replace("xxxx", str(y))
    with open(path ,"r") as file:
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
