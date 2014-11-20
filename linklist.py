from bs4 import BeautifulSoup
import csv
import html5lib
import urllib2

linklist = []
numoflinks = 0

def linkscraper(url):
    global linklist
    global numoflinks
    try: #catch value errors that occur for <soup.findAll('a', {'class':'twikilink'})> items that don't contain a url
        #convert link to the redirect url
        link = str(get_redirected_url(url))
        if 'php/Main' in link:
            #truncate everything that is not the trope
            linklist += [link]
    except ValueError: pass

#need the redirect handler to account for links on the tropeswiki page concerning other series or creators. the link on the page contains /Main/ but the link it redirects to has /Series/  /Creator/ etc
def get_redirected_url(url):
    opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
    request = opener.open(url)
    return request.url


startingurl = 'http://tvtropes.org/pmwiki/pmwiki.php/Main/Tropes'
request = urllib2.Request(startingurl)
url = urllib2.urlopen(request)
soup = BeautifulSoup(url, 'html5lib')

for item in soup.findAll('a', {'class':'twikilink'}):
    linkscraper(item['href'])

    with open('linklist.csv', 'wb') as f:
        writer = csv.writer(f)
        for link in linklist:
            writer.writerow(link)
        f.close()