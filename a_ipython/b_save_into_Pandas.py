# Martin Gascon, IDS

import glob
import pandas as pd
import csv
import sys



maxInt = sys.maxsize
decrement = True

while decrement:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.
    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt/10)
        decrement = True


# Get the GDELT field names from a helper file
# colnames = pd.read_excel('CSV.header.fieldids.xlsx', sheetname='Sheet1', 
#                         index_col='Column ID', parse_cols=1)['Field Name']

local_path = '/Users/martin/Desktop/GDELT_Data/'

# Build DataFrames from each of the intermediary files
files = glob.glob(local_path+'tmp/'+'*')

DFlist = []
print files

fields = ['DATE', 'NUMARTS', 'COUNTTYPE', 'GEO_TYPE', 'GEO_FULLNAME','GEO_COUNTRYCODE', 'GEO_LAT','GEO_LONG']

for active_file in files:
    #print active_file
    with open(active_file) as f:
        reader = csv.reader(f, delimiter="\t")
        for i in reader:
            if i[2]=='KILL' and (i[8]=='MX' or i[8]=='Mexico'):
                print i[6],i[7],i[8], i[9]

                #DFlist.append(pd.read_csv(active_file, sep='\t', usecols=fields, dtype=str))

#print DFlist
    #                          names=colnames, index_col=['GLOBALEVENTID']))


    #df = pd.read_csv('data.csv', skipinitialspace=True, usecols=fields)
# See the keys
#print df.keys()
# See content in 'star_name'
#print df.star_name

'''
# Merge the file-based dataframes and save a pickle
DF = pd.concat(DFlist)
DF.to_pickle(local_path+'backup'+fips_country_code+'.pickle')    
    
# once everythin is safely stored away, remove the temporary files
for active_file in files:
    os.remove(active_file)

# Here we can find the data
gdelt_base_url = 'http://data.gdeltproject.org/gkg/'

#http://data.gdeltproject.org/gkg/index.html

# Get the list of all the links on the gdelt file page
page = requests.get(gdelt_base_url+'index.html')
doc = lh.fromstring(page.content)
link_list = doc.xpath("//*/ul/li/a/@href")


# separate out those links that begin with four digits 
file_list = [x for x in link_list if str.isdigit(x[0:4]) and 'counts' in x]
print(file_list)

## We reset the infilecounter and outfilecounter external to the main algorithm cell 
# so that if the algorithm encounters an error, and quits, we can pick up where we left off.
infilecounter = 0
outfilecounter = 0

## All the zip files
local_path = '/Users/martin/Desktop/GDELT_Data/'

for compressed_file in file_list[infilecounter:]:
    print compressed_file,
    
    # if we dont have the compressed file stored locally, go get it. Keep trying if necessary.
    while not os.path.isfile(local_path+compressed_file): 
        print 'downloading,',
        urllib.urlretrieve(url=gdelt_base_url+compressed_file, 
                           filename=local_path+compressed_file)
        
    # extract the contents of the compressed file to a temporary directory    
    print 'extracting,',
    z = zipfile.ZipFile(file=local_path+compressed_file, mode='r')    
    z.extractall(path=local_path+'tmp/')

    infilecounter +=1
    print 'done'


'''