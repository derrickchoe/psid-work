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
        concw = pd.read_excel("ConsExpCrosswalk_new.xlsx")
        concw.columns = ['name', 'oldname'] + list(
            range(1999, self.lastyear + 2, 2))
        concw = copy.deepcopy(concw.loc[2:])
        return concw

    def categories(self, clist):
        subset = copy.deepcopy(self.psidcw)
        for i in range(0, len(clist)):
            lowercase = subset['C' + str(i)].str.lower()
            cond = lowercase.str.startswith(clist[i])
            subset = copy.deepcopy(subset[cond])
        assert len(subset) > 0
        return subset

    def cat_from_varname(self, varname):
        subset = copy.deepcopy(self.psidcw)
        ylist = [x for x in self.psidcw.columns if x.startswith('Y')]
        df= self.psidcw[ylist]
        assert varname in df.values
        subset = subset[df.values == varname]
        return subset

    def availableyears(clist, minyear = 1968, maxyear = 2017):
        ndf = self.categories(clist)
    #     all year columns
        ylist = [x for x in ndf.columns if x.startswith('Y')]
    #     only year columns in range
        rlist = [x for x in ylist if int(x[1:]) in range(minyear, maxyear + 1)]
        for i in ndf.index:
            print('ROW ' + str(i))
            rdf = ndf[rlist]
            notmissing = [x for x in rdf if rdf.loc[i, x] != 'missing']
            print(ndf[notmissing].columns)

    def findseries(self, varname):
        ylist = [x for x in self.psidcw.columns if x.startswith('Y')]
        df= self.psidcw[ylist]
        catlist = [x for x in self.psidcw.columns if x.startswith('C')]
        return self.psidcw[df.values == varname][catlist]

    def subcategories(self, clist):
        subset = self.categories(clist)
        i = len(clist)
        return subset['C' + str(i + 1)].unique()

    def load(self, lastyear = 2017):
        self.lastyear = lastyear
        self.psidcw = self.psidcw()
        self.rawfam = self.initiate_dict()
        self.rawind = pd.read_stata('IndividualData/individual.dta')
        self.rawchild = pd.read_stata('ChildHistoryData/childhistory.dta')
        self.concw = self.initiate_concw()
