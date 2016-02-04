import requests
import lxml.html as lh
import os.path
import urllib
import zipfile
import glob
import operator

# Here we can find the data
gdelt_base_url = 'http://data.gdeltproject.org/gkg/'

#http://data.gdeltproject.org/gkg/index.html
'''
For each resulting CSV file (probably only one)
Create and open an output file
For each line of the input file
Read into a string
Split string by tab delimiter
Check for the desired values in the appropriate list indexes
If they are not there, continue the loop
If the are there, write the line to the output file
Increment a current-file counter
Close the input and output files
Delete the input file

'''

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

### Let's start with Mexico
fips_country_code = 'MEX'

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

    '''    
    # parse each of the csv files in the working directory, 
    print 'parsing,',
    for infile_name in glob.glob(local_path+'tmp/*'):
        outfile_name = local_path+'country/'+fips_country_code+'%04i.tsv'%outfilecounter
        
        # open the infile and outfile
        with open(infile_name, mode='r') as infile, open(outfile_name, mode='w') as outfile:
            for line in infile:
                # extract lines with our interest country code
                if fips_country_code in operator.itemgetter(51, 37, 44)(line.split('\t')):    
                    outfile.write(line)
            outfilecounter +=1
            
        # delete the temporary file
        os.remove(infile_name)
    '''
    infilecounter +=1
    print 'done'