import csv
import urllib2
import html5lib
from numpy import genfromtxt


url = 'http://tvtropes.org/pmwiki/randomitem.php?p=1'

#WARNING you must run this script once with the following line commented out to have an inital mastertropelist.csv file. this line converts the csv file into a neat array
mastertropelist = genfromtxt('mastertropelist.csv', dtype='str', delimiter=',')

#total there are supposed to be 25866 trope entries.
for i in range(0,3000): #this checks 3000 links, but many times they will already be in the list so expect the real number to be lower
    #gotta handle redirects from repeatedly clicking a randomitem link
    opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
    request = opener.open(url)
    #make sure it's an actual trope
    if 'php/Main' in request.url:
        #strip everything but the trope name from the url
        trope = (request.url[43:].split('?'))[0]
        #and trope not in mastertropelist
        if trope not in mastertropelist:
            print trope
            with open('mastertropelist.csv', 'ab') as csvfile: #ab for appending, bitch
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow([trope])
                csvfile.close()
        else: continue
    else: continue

