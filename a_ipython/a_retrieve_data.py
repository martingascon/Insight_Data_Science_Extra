# Martin Gascon, IDS

'''
This script download GDELT files into local directory
and extracts Relevant GDELT Rows to Intermediate Files

# Procedure 
1. Check and see if the files are available locally 
so we don't have to to continually ping the gdelt server.
2. Unzip the compressed raw GDELT file into the tmp directory

'''
import requests
import lxml.html as lh
import os.path
import urllib
import zipfile
import glob
import operator
from os import listdir
from os.path import isfile, join

# Here we can find the data
gdelt_base_url = 'http://data.gdeltproject.org/gkg/'
#http://data.gdeltproject.org/gkg/index.html

# Get the list of all the links on the gdelt file page
page = requests.get(gdelt_base_url+'index.html')
doc = lh.fromstring(page.content)
link_list = doc.xpath("//*/ul/li/a/@href")
#print link_list

## All the zip files
local_path = '/Users/martin/Desktop/GDELT_Data/'



onlyfiles = [f for f in listdir(local_path) if isfile(join(local_path, f))]
#print onlyfiles

# separate out those links that begin with four digits 
file_list = [x for x in link_list if str.isdigit(x[0:4]) and 'counts' in x and x not in onlyfiles]
print(file_list)

## We reset the infilecounter and outfilecounter external to the main algorithm cell 
# so that if the algorithm encounters an error, and quits, we can pick up where we left off.
infilecounter = 0
outfilecounter = 0

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




