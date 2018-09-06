import pandas as pd
import numpy as np
import copy
class psidraw:
    def __init__(self):
        print('psidraw class: use .load() to import raw data')

# read in psid variable name file
    def psidcw(self):
        vardata = pd.read_excel('psid.xlsx')
# split variable descriptions to allow for multiple identifying variables
        vardata['split_text'] = vardata['TEXT'].str.split('>')
        vardata['C0'] = vardata['TYPE']
        for cat in range(1, vardata['split_text'].str.len().max()):
            text = vardata['split_text'].str[cat]
            text = text.str.replace('\n\d\d', '')
            text = text.str.replace(':', '')
            vardata['C' + str(cat)] = text
        return vardata.fillna('missing')


    def initiate_dict(self):
        d = {}
# Read in family data
        for year in range(1999, self.lastyear + 2, 2):
            d[year] = pd.read_stata('familydata/fam' + str(year) + '.dta')
# read in wealth data
        for year in range(1999, 2009, 2):
            wealth = pd.read_stata('wealthdata/wlth' + str(year) + '.dta')
            d[year] = d[year].join(wealth)
        return d

    def initiate_concw(self):
        concw = pd.read_excel("ConsExpCrosswalk.xlsx")
        concw.columns = ['name', 'oldname'] + list(
            range(1999, self.lastyear + 1, 2))
        concw = copy.deepcopy(concw.loc[2:])
        return concw

    def load(self, lastyear = 2015):
        self.lastyear = lastyear
        self.psidcw = self.psidcw()
        self.rawfam = self.initiate_dict()
        self.rawind = pd.read_stata('IndividualData/individual.dta')
        self.rawchild = pd.read_stata('ChildHistoryData/childhistory.dta')
        self.concw = self.initiate_concw()
