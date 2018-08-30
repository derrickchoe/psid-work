import pandas as pd
import numpy as np
import copy
from psid import psidraw, psidvars
from psid.functions import categories
class psiddata:
    def __init__(self, rawdata = None):
        if isinstance(rawdata, psidraw):
            self.rawfam = rawdata.rawfam
            self.rawind = rawdata.rawind
            self.rawchild = rawdata.rawchild
            self.psidcw = rawdata.psidcw
            self.concw = rawdata.concw
            self.lastyear = rawdata.lastyear
        else:
            print('include raw data object')

    def getfamyeardata(self, df, namedf, year):
    #     Get list of that year's variable names
        varlist = list(namedf['Y' + str(year)])
    #     Remove missing vars/vars already included
        varlist = [x for x in varlist if x != 'missing']
        for var in varlist:
            df[var] = self.rawfam[year][var]
        return df

    def getfamdata(self, datadict, namedf):
        # this function updates a dictionary with raw family data
        for year in range(1999, self.lastyear + 2, 2):
            datadict.setdefault(year, pd.DataFrame())
            datadict[year] = self.getfamyeardata(datadict[year], namedf, year)
        return datadict

    def getinddata(self, df, namedf):
    #     Get list of that year's variable names
        varlist = []
        for year in range(1999, self.lastyear + 1, 2):
            varlist = varlist + list(namedf['Y' + str(year)])
    #     Remove missing vars/vars already included
        varlist = [x for x in varlist if x != 'missing']
        for var in varlist:
            df[var] = self.rawind[var]
        return df

    def merge_ind_fam(self, inddf, famdict):
        indid_arg = [
            'individual', 'survey information',
            'interview information', 'id (interview)',
            'missing'
            ]
        famid_arg = [
            'family', 'survey information',
            'interview information', 'family interview number (id)',
            'missing'
            ]
        indid_list = categories(self.psidcw, indid_arg)
        famid_list = categories(self.psidcw, famid_arg)
        newdict = {}
        # generate keep variable to track observations
        keep = [0] * len(inddf)
        for year in range(1999, self.lastyear + 1, 2):
    # assign copy of family ID with family data name to individual data
            famname = famid_list['Y' + str(year)].values[0]
            indname = indid_list['Y' + str(year)].values[0]
            inddf[famname] = inddf[indname]
            inddf = inddf.merge(famdict[year], on = famname, how = 'left')
            # keep observations that have appeared in data at least once
            keep = np.where((inddf[famname] != 0) | (keep == 1), 1, 0)
            # generate person_id for merge with child data
        inddf['person_id'] = (self.rawind['ER30001'] * 1000 +
                              self.rawind['ER30002'])
        return inddf[keep == 1]

    # Crosswalk for pulling data and renaming
    def consdata(self, d = {}):
#         pull family raw consumption data
        for year in range(1999, self.lastyear + 1, 2):
            varlist = self.concw[year].dropna()
            for var in varlist:
                d[year][var] = self.rawfam[year][var]
        return d


    def merge_child(self, inddf):
        # create markers for whether someone is a parent
        # subset for those with children?
        child = copy.deepcopy(self.rawchild[self.rawchild['CAH9'] < 98])
        child['person_id'] = child['CAH3'] * 1000 + child['CAH4']
        # keep those with children
        child['max9'] = child.groupby('person_id')['CAH9'].transform(max)
        child = child.loc[(child['max9'] == child['CAH9']) |
                          (child['max9'].isnull())]
        child = child.drop_duplicates('person_id')
        child = child[['person_id', 'max9']]
        inddf = inddf.merge(child, on = 'person_id', how = 'left')
        # assign parent dummy variable
        inddf['isparent'] = np.where(inddf['max9'].notnull(), 1, 0)
        return inddf

    def outputdf(self, varobj, inclusive= False):
        famdict = {}
        famdict = self.getfamdata(famdict, varobj.fam_ndf)

        famdict = self.consdata(famdict)

        inddf = pd.DataFrame()
        inddf = self.getinddata(inddf, varobj.ind_ndf)

        combineddf = self.merge_ind_fam(inddf, famdict)
        combineddf = self.merge_child(combineddf)

        widedf = combineddf.rename(columns = varobj.renamedict)
        # if inclusive is false, only keep observations with data throughout
        # entire timeline
        if inclusive == False:
            widedf = widedf.dropna(thresh = len(widedf.columns) - 1)
        # shift from wide to long
        finaldf = pd.wide_to_long(widedf, varobj.reshapelist,
                                  i = 'person_id', j = 'year')
        finaldf = finaldf.reset_index()
        finaldf['year'] = finaldf['year'].astype(int)
        return finaldf
