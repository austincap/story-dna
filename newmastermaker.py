import csv
import urllib2
import html5lib
from bs4 import BeautifulSoup
from numpy import genfromtxt

mastertropelist = []
numoftropes = 0

#extracting the tropeName string from the url
def tropescraper(url):
    global mastertropelist
    global numoftropes
    try: #catch value errors that occur for <soup.findAll('a', {'class':'twikilink'})> items that don't contain a url
        #convert link to the redirect url
        link = str(get_redirected_url(url))
        if 'php/Main' in link:
            #truncate everything that is not the trope
            trope = (link[43:].split('?'))[0]
            #add it to the tropelist if trope not in tropelist cause many pages contain duplicates
            mastertropelist = genfromtxt('mastertropelist.csv', dtype='str', delimiter=',')
            if trope not in mastertropelist:
                mastertropelist += [trope]
                print trope
                numoftropes+=1
    except ValueError: pass


#need the redirect handler to account for links on the tropeswiki page concerning other series or creators. the link on the page contains /Main/ but the link it redirects to has /Series/  /Creator/ etc
def get_redirected_url(url):
    opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
    request = opener.open(url)
    return request.url



with open('linklist.csv', 'r') as linklist:
    reader = csv.reader(linklist, delimiter='\n')
    for row in reader:
        linkstr = row.pop()
        request = urllib2.Request(linkstr)
        url = urllib2.urlopen(request)
        soup = BeautifulSoup(url, 'html5lib')
        for item in soup.findAll('a', {'class':'twikilink'}):
            tropescraper(item['href'])
    linklist.close()

with open('newmasterlist.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for trope in mastertropelist:
        writer.writerow([trope])
    csvfile.close()

print numoftropes