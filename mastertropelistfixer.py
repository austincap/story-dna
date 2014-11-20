import csv

def uniquifyer(seq, idfun=None): 
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       # in old Python versions:
       # if seen.has_key(marker)
       # but in new ones:
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result

seq=[]
with open('mastertropelist.csv','r') as f:
	spamreader = csv.reader(f, delimiter='\n')
	for row in spamreader:
		seq+=row
with open('mastertropelistalpha.csv','r') as f:
  spamreader = csv.reader(f, delimiter='\n')
  for row in spamreader:
    seq+=row

print len(seq)

print len(uniquifyer(seq, idfun=None))

fixedlist = uniquifyer(seq, idfun=None)

with open('fixedmastertropelist.csv', 'ab') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for item in fixedlist:
    	writer.writerow([item])
    csvfile.close()