from twython import Twython
import re
import itertools
import string
import random
import unicodedata
import sys

# generates binary sequences, not used in the program.

def binseq(k):
    return [''.join(x) for x in itertools.product('01', repeat=k)]

def getcomb3(x,n):
	substrate = [0] * x
	# produces a *unique* sample of n numbers ranging from 1 to x. Really handy. 
	# we use this sample as positions to which we "sprinkle" n 1 bits on the substrate. 
	sel = random.sample(xrange(1,x),n)
	for s in sel:
		substrate[s]=1
        return substrate

random.seed(123)
# input 	
twitter = Twython( '<paste yours here>','<paste yours here>','<paste yours here>','<paste yours here>')

search_results = twitter.search(q='play', lang='en', until='2014-03-01',rpp=200, encoding='utf-8')
pool = []

# post-processing

for tweet in search_results['statuses']:
  print(tweet['created_at'], tweet['text'])

  t = re.sub(r"(?:\@|\#|https?\://)\S+", "", tweet['text']) # removes URLs, RTs, mentions
  tnort = t.replace("RT","")
  s = tnort.split(" ")  
  for word in s:
    if word.isalpha():
      pool.append(word)



pool_set = set(pool) # this will make the list have only uniques
pool_uniqt = list(pool_set) # changing it back to list
pool_uniq = []
for pool_word in pool_uniqt:
  pool_uniq.append(unicodedata.normalize('NFKD', pool_word).encode('ascii','ignore'))

stegomap = {}
stegomap_keys = list(string.ascii_lowercase) + list(string.ascii_uppercase) + list(string.digits) #the payload




# Pick words according to the bitmap
selection = getcomb3(len(pool_uniq),62)


#
stegomap_values = []
counter = -1


for idx,s in enumerate(selection):
	if s == 1: 
		stegomap_values.append(pool_uniq[idx])
	else:
		pass



#
# random.shuffle(a), opou a h stegomap_values, me seed to kleidi, kai meta directly map me dict(zip) kai komple

random.shuffle(stegomap_values)
stegomap_dec = dict(zip(stegomap_values, stegomap_keys)) # reversed, this will pair all possible payload characters with the pool words, using a key
print stegomap_dec

tweet_words = []
tweet = raw_input("Input:")

for word in tweet.split():
	tweet_words.append(word)
	if word in stegomap_dec:
		print stegomap_dec[word]
