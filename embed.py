from twython import Twython
import re
import itertools
import string
import random
import unicodedata
import datetime
import sys
import ConfigParser
# generates binary sequences, not used.


keyword_arg = sys.argv[1]
def binseq(k):
    return [''.join(x) for x in itertools.product('01', repeat=k)]

def getKdist(x,n):
	substrate = [0] * x
	# produces a *unique* sample of n numbers ranging from 1 to x. Really handy. 
	# we use this sample as positions to which we "sprinkle" n 1 bits on the substrate. 
	sel = random.sample(xrange(1,x),n)
	for s in sel:
		substrate[s]=1
        return substrate


def loadConf():
	Config = ConfigParser.ConfigParser()
	Config.read("pteroglosia_keys.private")
		
	global CONSUMER_KEY
	global CONSUMER_SEC
	global ACCESS_TOKEN
	global ACCESS_LEVEL
	global PTERO_RNDKEY
	global PTERO_POOLKEY

	CONSUMER_KEY = Config.get('Twitter','CONSUMER_KEY')
	CONSUMER_SEC = Config.get('Twitter','CONSUMER_SEC')
	ACCESS_TOKEN = Config.get('Twitter', 'ACCESS_TOKEN')
	ACCESS_LEVEL = Config.get('Twitter','ACCESS_LEVEL')
	PTERO_RNDKEY = Config.get('pteroglosia','PASSPHRASE')
	PTERO_POOLKEY = Config.get('pteroglosia','POOLKEY')

	
def pool_cleanup(pool):
	for tweet in pool:
  		print(tweet['created_at'], tweet['text'])
  		t = re.sub(r"(?:\@|\#|https?\://)\S+", "", tweet['text']) # removes URLs, RTs, mentions
		if 'RT' in t:
			pass
		else:
			tweets.append(tweet['text'])
		
  		for s in tweets:
			
			s = t.split(" ")
  			for word in s:
    				if word.isalpha():
      					pool.append(word.lower())
	# remove stop words
	# test for english words
	# if not english then prompt for exemption, if exception, saved
	# option to turn it off
	f = open('stop.txt', 'r')
	print "from cleanup()"
	stopwords = []
	stopwords = f.read()

	for word in pool:
		if word in stopwords:
			print word, "is a stopword, deleting from pool.."
			while pool.count(word) > 0:
   				 pool.remove(word)

loadConf()
print "Configuration loaded"
#random.seed(PTERO_RNDKEY)
# input 	
twitter = Twython( CONSUMER_KEY, CONSUMER_SEC, ACCESS_TOKEN, ACCESS_LEVEL)

# calculate 2 calendar days before current date


twodaysbefore = str(datetime.date.today()-datetime.timedelta(2))
#print twodaysbefore
#twodaysbefore="2014-04-20"
tweets = []
for i in range(1,5):

	print "pooling tweets..."
	search_results = twitter.search(q=PTERO_POOLKEY, lang='en', until=twodaysbefore,rpp=200, encoding='utf-8', count=100)
	tweets.extend(search_results)


pool = []
unique_sorted_set = sorted(set(tweets))
# post-processing

pool_cleanup(unique_sorted_set)

# convert the pool into a se and back to a list, so we keep the unique ones.
pool_set = set(pool) # this will make the list have only uniques
pool_uniqt = list(pool_set) # changing it back to list
pool_uniq = []
for pool_word in pool_uniqt:
  pool_uniq.append(unicodedata.normalize('NFKD', pool_word).encode('ascii','ignore'))

print "************* UNIQUE POOL **************"
print pool_uniq
stegomap = {}
stegomap_keys = list(string.ascii_lowercase) + list(string.ascii_uppercase) + list(string.digits) #the payload




# Pick the words with the flag bits 'true'
selection = getKdist(len(pool_uniq),62)


#
print "*********** SELECTION ***************"
print selection
stegomap_values = []
counter = -1


for idx,s in enumerate(selection):
	if s == 1: 
		stegomap_values.append(pool_uniq[idx])
	else:
		pass

#while (counter < len(selection)):
#	counter = counter + 1 
#	if selection[counter] == 1:
#		print counter,"Puting", pool_uniq[counter], "in ", counter
#		print stegomap_values
#		stegomap_values.append(pool_uniq[counter])



print "********** STEGOMAP VALUES ***************"
print stegomap_values

#
# random.shuffle(a), opou a h stegomap_values, me seed to kleidi, kai meta directly map me dict(zip) kai komple
print "********** STEGOMAP VALUES SHUFFLED *******"

random.shuffle(stegomap_values)
print stegomap_values

stegomap = dict(zip(stegomap_keys, stegomap_values)) # this will pair all possible payload characters with the pool words, using a key
print "*********** STEGOMAP **************"
print stegomap
print len(stegomap)
#http://goo.gl/mvJs9F
print ("Stego object for http://goo.gl/mvJs9F:")
stegobj =  [stegomap['m'], stegomap['v'], stegomap['J'], stegomap['s'],stegomap['9'], stegomap['F']]
print stegobj
#print("length of word pool is ",len(pool))
# #annotation
#
#
# need to check if all the stego object is embedded
valid=False


while (valid != True):

	tweet = raw_input('Enter your input:')


	tweet_words = []

	for word in tweet.split():
		tweet_words.append(word)

# this searches whether the words in the tweet except the stego ones belong to the pool
	stegocounter = 0

# validation section

	for word in tweet_words:
		if word in stegomap_values:
			print word, "word in stegomap found"
			stegocounter = stegocounter + 1
		if word in pool_uniq and word not in stegomap_values:
			print word, "word found in pool! abort!"
			break	

		if stegocounter == 6: valid=True
		
		if stegocounter < 6:
        		print "WARNING: Less than 6 stego-objects have been used! Please try again"
			break

print tweet_words
