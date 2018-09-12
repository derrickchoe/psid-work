import pandas as pd
import numpy as np
import copy
# def categories(crosswalk, clist):
#     subset = copy.deepcopy(crosswalk)
#     for i in range(0, len(clist)):
#         lowercase = subset['C' + str(i)].str.lower()
#         cond = lowercase.str.startswith(clist[i])
#         subset = copy.deepcopy(subset[cond])
#     assert len(subset) > 0
#     return subset
#
# def cat_from_varname(crosswalk, varname):
#     subset = copy.deepcopy(crosswalk)
#     ylist = [x for x in crosswalk.columns if x.startswith('Y')]
#     df= crosswalk[ylist]
#     assert varname in df.values
#     subset = subset[df.values == varname]
#     return subset
#
# def availableyears(crosswalk, clist, minyear = 1968, maxyear = 2015):
#     ndf = categories(crosswalk, clist)
# #     all year columns
#     ylist = [x for x in ndf.columns if x.startswith('Y')]
# #     only year columns in range
#     rlist = [x for x in ylist if int(x[1:]) in range(minyear, maxyear + 1)]
#     for i in ndf.index:
#         print('ROW ' + str(i))
#         rdf = ndf[rlist]
#         notmissing = [x for x in rdf if rdf.loc[i, x] != 'missing']
#         print(ndf[notmissing].columns)
#
# def findseries(crosswalk, varname):
#     ylist = [x for x in crosswalk.columns if x.startswith('Y')]
#     df= crosswalk[ylist]
#     catlist = [x for x in crosswalk.columns if x.startswith('C')]
#     return crosswalk[df.values == varname][catlist]
#
# def subcategories(crosswalk, clist):
#     subset = categories(crosswalk, clist)
#     i = len(clist)
#     return subset['C' + str(i + 1)].unique()
