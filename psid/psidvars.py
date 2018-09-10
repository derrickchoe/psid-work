# Find a way to clean up handling of CONCW-- currently defined in both psidvars and psiddata classes
# maybe include vardata and categories in this class?
import pandas as pd
import numpy as np
import copy
from psid import psidraw
from psid.functions import categories, cat_from_varname
class psidvars:
    def __init__(self, rawdata = None):
        if isinstance(rawdata, psidraw):
            self.reshapelist = []
            self.renamedict = {}
            self.fam_ndf = pd.DataFrame()
            self.ind_ndf = pd.DataFrame()
            self.lastyear  = rawdata.lastyear
            self.psidcw = rawdata.psidcw
            self.concw = rawdata.concw
        else:
            print('include raw data object')

    def rename(self, namedf, namelist):
        # reshapelist is a list of names for wide to long function
        for name in [x for x in namelist if x not in self.reshapelist]:
            self.reshapelist.append(name)
        # append psid index dataframes for individual and family data
        self.fam_ndf = self.fam_ndf.append(
            namedf[namedf['TYPE'] == 'FAMILY PUBLIC'])
        self.ind_ndf = self.ind_ndf.append(
            namedf[namedf['TYPE'] == 'INDIVIDUAL'])
        assert(len(namedf) == len(namelist))
        # create dictionary with desired and raw data names + years
        rdict = {}
        for year in range(1999, self.lastyear + 1, 2):
            col_name = 'Y' + str(year)
            oglist = list(namedf[col_name])
            for i in range(0, len(oglist)):
                rdict[oglist[i]] = namelist[i] + str(year)
        return rdict

# creates a renaming dictionary for a namedf of PSID data
    def update_rename(self, namelist, clist):
        namedf = categories(self.psidcw, clist)
        newdict = self.rename(namedf, namelist)
        self.renamedict.update(newdict)

    def update_rename_varname(self, name, varname):
        namedf = cat_from_varname(self.psidcw, varname)
        vlist = [name]
        newdict = self.rename(namedf, vlist)
        self.renamedict.update(newdict)

    def cons_renamedict(self):
        # adds consumption variables from psid crosswalk (available online)
        # to renamedict and reshapelist
        for index, row in self.concw.iterrows():
            for y in range(1999, self.lastyear + 1, 2):
                ogname = row[y]
                newname = row['name'].strip()
                self.renamedict[ogname] = newname + str(y)
                if newname not in self.reshapelist:
                    self.reshapelist.append(newname)
