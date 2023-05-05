#!/usr/bin/python
#
# pteroglosia prototype
# (c) George Fountis 2014, Goldsmiths.
#
# embed.py
from twython import Twython
import re
import itertools
import string
import random
import unicodedata
import datetime
import sys
import ConfigParser
keyword_arg = sys.argv[1] # payload

def getKdist(x,n):
    substrate = [0] * x
# produces a *unique* sample of n numbers ranging from 1 to #x. Really handy.
# we use this sample as positions to which we "sprinkle" n 1 bits on the substrate.
    sel = random.sample(xrange(1,x),n)
    for s in sel:
        substrate[s]=1
return substrate
Config = ConfigParser.ConfigParser()
Config.read("pteroglosia_keys.private")
global CONSUMER_KEY
global CONSUMER_SEC
global ACCESS_TOKEN
global ACCESS_LEVEL
global PASSPHRASE
global POOLKEY

CONSUMER_KEY = Config.get(’Twitter’,’CONSUMER_KEY’)
CONSUMER_SEC = Config.get(’Twitter’,’CONSUMER_SEC’)
ACCESS_TOKEN = Config.get(’Twitter’, ’ACCESS_TOKEN’)
ACCESS_LEVEL = Config.get(’Twitter’,’ACCESS_LEVEL’)
PASSPHRASE = Config.get(’pteroglosia’,’PASSPHRASE’)
POOLKEY = Config.get(’pteroglosia’,’POOLKEY’)

unique_pool = []
stegomap = {}
stegomap_keys = list(string.ascii_lowercase) + list(string.ascii_uppercase) + list(string.digits) # URL-space
stegomap_values = []
stego_object = []
keyword_arg = sys.argv[1]

print "Pteroglosia (*)>"
print "            / )"
print "            /\""
print "Prototype, George Fountis (c) 2014, Goldsmiths."
print "Configuration loaded"
random.seed(PASSPHRASE)
print "PRNG seeded with PASSPHRASE"

# input
twitter = Twython( CONSUMER_KEY, CONSUMER_SEC, ACCESS_TOKEN,
ACCESS_LEVEL)
# calculate 2 calendar days before current date
twodaysbefore = str(datetime.date.today()-datetime.timedelta(2))
search_results = twitter.search(q=POOLKEY, lang=’en’,
until=twodaysbefore,rpp=200, count=200, encoding=’utf-8’)

# pre-processing
for tweet in search_results[’statuses’]:
    words_in_tweet = tweet[’text’].split(" ");
    for word in words_in_tweet:
        if word.isalpha():
            unique_pool.append(unicodedata.normalize(’NFKD’,word.lower()).encode(’ascii’,’ignore’));

tmp_unique_pool_set = set(unique_pool)
unique_pool = list(tmp_unique_pool_set)
f = open(’stop.txt’, ’r’)
stopwords = []
stopwords = f.read()
for word in unique_pool:
    if word in stopwords:
        while unique_pool.count(word) > 0:
            unique_pool.remove(word)

# data embedding
selection = getKdist(len(unique_pool),62)
for idx,s in enumerate(selection):
    if s == 1:
        stegomap_values.append(unique_pool[idx])
    else:
        pass

str(unique_pool)
print "Unique Pool (",len(unique_pool), "):"
print unique_pool
random.shuffle(stegomap_values)
stegomap = dict(zip(stegomap_keys, stegomap_values))
print "\n"
print "Stegomap (",len(stegomap),"):"
print stegomap
print "\n"
print ("Stego object for http://goo.gl/"+keyword_arg+":"),

for s in keyword_arg:
    stego_object.append(stegomap.get(s))
print stego_object

# annotation
valid = False
stego_tweet_words = []
stegocounter = 0
stego_tweet = raw_input(’Enter your input:’)
stego_tweet_words = stego_tweet.split(" ")
error = 0
for word in stego_tweet_words:
    if word not in stego_object and word in stegomap_values:
        error = 1
        err_word = word

if error:
    print "ERROR: You used the word ’",err_word,"’ which is not part of the stego_object but is present in the stegomap. Please try again!"

else:
    print "OK: stego_object seems to be embedded correctly. However make sure that the order of the words is preserved."

