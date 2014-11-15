from bs4 import BeautifulSoup
import csv
import os
import urllib2
import html5lib

startingurl = 'http://tvtropes.org/pmwiki/pmwiki.php/Main/WesternAnimation'
listoflinks = []
medium = "WesternAnimation"

request = urllib2.Request(startingurl)
url = urllib2.urlopen(request)
soup = BeautifulSoup(url, 'html5lib')

for item in soup.findAll('a', {'class':'twikilink'}):
	link = item['href']
	if link not in listoflinks and ('php/'+medium) in link:
		print link
		listoflinks += [link]
	else: continue

filename = medium + '.csv'
path_to_script_dir = os.path.dirname(os.path.abspath("findallworks.py"))  #create a new file no matter what
newpath = path_to_script_dir + r'\\' + filename
with open(newpath, 'wb') as f:
    writer = csv.writer(f)
    for link in listoflinks:
        writer.writerow([link])
    f.close()