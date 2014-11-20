import csv
import urllib2
import html5lib
from numpy import genfromtxt


url = 'http://tvtropes.org/pmwiki/randomitem.php?p=1'

#WARNING you must run this script once with the following line commented out to have an inital mastertropelist.csv file. this line converts the csv file into a neat array
#mastertropelist = genfromtxt('mastertropelist.csv', dtype='str', delimiter=',')

#I noticed there is one issue with my method for scraping tropes: if the trope was added to the master list in the current batch, repeats will not be discovered as the master trope list is only generated once

#total there is supposed to be 25866 trope entries.
for i in range(0,100000):
    #gotta handle redirects from repeatedly clicking a randomitem link
    opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
    request = opener.open(url)
    #make sure it's an actual trope
    if 'php/Main' in request.url:
        #strip everything but the trope name from the url
        trope = (request.url[43:].split('?'))[0]
        #and trope not in mastertropelist
        mastertropelist = genfromtxt('mastertropelist.csv', dtype='str', delimiter=',')
        if trope not in mastertropelist:
            print trope
            with open('mastertropelist.csv', 'ab') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow([trope])
                csvfile.close()
        else: continue
    else: continue


#print my_data