from bs4 import BeautifulSoup
import csv
import re
import sys
import os
import urllib2
import html5lib
from numpy import genfromtxt
import time

tropelist = []
numoftropes = 0
start = time.time()

#compare the tropelist to the master tropelist and return a 1 dimensional binary array
def binarizer(tropelist):
    mastertropelist = genfromtxt('mastertropelist.csv', dtype='str', delimiter=',')
    tropearray = []
    for item in mastertropelist:
        if item in tropelist:
            tropearray += [1]
        else:
            tropearray += [0]
    return tropearray

#need the redirect handler to account for links on the tropeswiki page concerning other series or creators. the link on the page contains /Main/ but the link it redirects to has /Series/  /Creator/ etc
def get_redirected_url(url):
    opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
    request = opener.open(url)
    return request.url

#extracting the tropeName string from the url
def tropescraper(url):
    global tropelist
    global numoftropes
    try: #catch value errors that occur for <soup.findAll('a', {'class':'twikilink'})> items that don't contain a url
        #convert link to the redirect url
        link = str(get_redirected_url(url))
        if 'php/Main' in link:
            #truncate everything that is not the trope
            trope = (link[43:].split('?'))[0]
            #add it to the tropelist if trope not in tropelist cause many pages contain duplicates
            if trope not in tropelist:
                tropelist += [trope]
                print trope
                numoftropes+=1
    except ValueError: pass

def webcrawler(startingurl, imdbrating):
    #access page and initialize alternatetropeliststyle and declare global variables
    request = urllib2.Request(startingurl)
    url = urllib2.urlopen(request)
    soup = BeautifulSoup(url, 'html5lib')
    #need this alternate tropeliststyle to account for pages that don't use the newer clickable "folder" system. this uses new webpages instead
    alternatetropeliststyle = []
    global tropelist
    global numoftropes

    #find everything with this name and tag. includes all of the links in the folders at the bottom
    for item in soup.findAll('a', {'class':'twikilink'}):
        #check if one of the links found contains TropesAToD, etc, an indicator the alternate tropelist style was implemented
        if not re.search("Tropes.To.",item['href']):
            tropescraper(item['href'])
        else:
            alternatetropeliststyle += [item['href']]

    #if alternate tropeslist was used open each "TropesAToD" etc link and run tropescraper on it after making it into soup
    if alternatetropeliststyle:
        for listedurl in alternatetropeliststyle:
            request = urllib2.Request(listedurl)
            url = urllib2.urlopen(request)      
            soup = BeautifulSoup(url, 'html5lib')

            for item in soup.findAll('a', {'class':'twikilink'}):
                tropescraper(item['href'])

    print "Total number of tropes found: ", numoftropes

    #dynamically name and create tropelists for works
    filename = subject + ' tropelist.csv'
    path_to_script_dir = os.path.dirname(os.path.abspath("tlm.py"))  #create a new file no matter what
    newpath = path_to_script_dir + r'\\' + filename
    with open(newpath, 'wb') as f:
        writer = csv.writer(f)
        for trope in tropelist:
            writer.writerow([trope])
        f.close()

    #convert tropelist to array of 1's and 0's and put that array in an array that also contains the work title, rating (y-data), and total num of tropes found
    #put all this in a master array list to analyze with the classifier
    tropearray = binarizer(tropelist)
    with open('masterarraylist.csv', 'ab') as f:
        writer = csv.writer(f)
        writer.writerow([subject,tropearray,imdbrating,numoftropes])
        f.close()

#media = raw_input('"Anime", ComicStrip","Webcomic","ComicBook","Film","VideoGame","Series","Literature","WesternAnimation"')
#subject = raw_input("Enter work you want to analyze (all one word and case matters!): ")
#imdbrating = raw_input("Please provide a rating from 1-10 for this work: ")
media = 'WesternAnimation'
subject = 'AdventureTime'
imdbrating = 90 #use 1-100 scale
webcrawler("http://tvtropes.org/pmwiki/pmwiki.php/" + media +"/" + subject, imdbrating)

#automatically go through every work on tvtropes for a given medium, in this case WesternAnimation
# with open('WesternAnimation.csv', 'r') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         webcrawler(row,_________)  #NEED TO AUTOMATICALLY SCRAPE RATINGS/GENRE OR SOMETHING BASED ON THE CAPITALIZED ONE WORD TITLE!
#     f.close()

end = time.time()

print "Time elapsed:", end-start