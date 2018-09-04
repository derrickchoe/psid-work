# psid-work
The psid-work repository is designed to facilitate use of the Panel Survey of Income Dynamics. It can be used to pull, rename, and reshape publically-available PSID data.

## Downloading and formatting the raw data
This repo is currently designed to handle PSID data from 1999 onwards. All necessary data files come from the <a href = "https://simba.isr.umich.edu/Zips/ZipMain.aspx" >"packaged data"</a> section of the PSID download center. 
1. Start by expanding the "Family Files" section and download the zipped files for years 1999-2015. From 1999-2007, the supplemental wealth data are only available in separate files; simply expand the 1999, 2001, etc. year tabs to download them. 
2. Download the individual-level data. This comes as a single extract titled "Cross-year Individual: 1968-2015."
3. Download the PSID consumption data, titled "Consumption Expenditure Data: 1999-2013."

Once the data are all download, extract the family folders into the "FamilyData" folder of this repo, and the wealth data into the "WealthData" folder of this repo. "FamilyData" should thus contain several folders labelled "fam1999er," "fam2003er," etc. Similarly, "WealthData" will contain "wlth2003," "wlth2007," etc. 

The next step is to run the "import_data.py" script in the "psid" folder. 
