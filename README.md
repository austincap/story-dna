story-dna
============

Tropes are story-telling tools; ie the essence of what makes up a story. Every single story ever can be described as a combination of tropes just like how every single person ever can be described as a combination of DNA. Furthermore there seems to be a trend in data science to call this kind of stuff DNA so I'm going with it.

The idea is to produce for each work on tvtropes.org an array that describes what tropes it contains. Using this tropelist data set, a variety of analyses can be conducted on art.

1) Obtain a set of parameters that when provided with a tropelist data set can predict what the quality of a new, unrated work will be. This could help artists determine what tropes to use in order to be successful. 

2) Run a clustering algorithm on the same data to find patterns and similarities. Maybe help with quantitative genre definition.

3) One could even use their own personal ratings for every show to build a recommender system, based on the features/tropes of different works.

How it works: Provide some sort of rating (eg imdb) to go with each show's data. Run the trope data and rating data for each show through a machine learning algorithm. Right now I'm looking at stochastic gradient descent. While this requires the use of integers for ratings, I'm just gonna make every rating 1/100 or 1/1000 and call it a day. Yes, this means there would be 100s of labels to classify to and 10000s of features for that matter. 

============

mastertropelistmaker.py

Scrapes all of tvtropes.org for a list of every single trope. There are 25866. It's designed to let you scrape a little at a time, keyboard interrupting whenever you feel like. You could run this yourself but I'm also providing the mastertropelist.csv when I have it.

findallworks.py

Automatically produces a list of all links for a given medium. Ideally you'd run this before tlm.py but I still need a way to automatically scrape rating data.

tlm.py (trope list maker)

Right now this takes a single work's page along with some sort of rating, scrapes the tropes from the page, and appends a new row to the "masterarraylist" containing the work's title, the binary tropelist array, the rating label, and the total number of tropes found.

classifier.py

Takes all the "masterarraylist" data and runs it through a scikit classifier.

nottropes.csv

I noticed some tropes I was scraping are not really story-telling tools so much as concepts that didn't fit well in other places on the site; eg "Sequel" "TVTropesWillRuinYourLife"


