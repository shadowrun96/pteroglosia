#!/usr/bin/python
#
#
# pteroglosia prototype
# (c) George Fountis 2014, Goldsmiths.
#
# extract.py
from twython import Twython
from twython import Twython
import re
import itertools
import string
import random
import unicodedata
import datetime
import sys
import ConfigParser

def getKdist(x,n):
    substrate = [0] * x
    # produces a *unique* sample of n numbers ranging from 1 to x. Really handy. 
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
stego_tweet = sys.argv[1] #stego-tweet
print "Pteroglosia (*)>"
print "            / )"
print "           /\""
print "Prototype, George Fountis (c) 2014, Goldsmiths."

print "Configuration loaded"
random.seed(PASSPHRASE)
print "PRNG seeded with PASSPHRASE"
# input
twitter = Twython( CONSUMER_KEY, CONSUMER_SEC, ACCESS_TOKEN,ACCESS_LEVEL)
# calculate 2 calendar days before current date
twodaysbefore = str(datetime.date.today()-datetime.timedelta(2))
search_results = twitter.search(q=POOLKEY, lang=’en’, until=twodaysbefore,rpp=200, count=200, encoding=’utf-8

# pre-processing
for tweet in search_results[’statuses’]:
    words_in_tweet = tweet[’text’].split(" ");
    for word in words_in_tweet:
        if word.isalpha():
            unique_pool.append(unicodedata.normalize(’NFKD’, word.lower()).encode(’ascii’,’ignore’));

tmp_unique_pool_set = set(unique_pool)
unique_pool = list(tmp_unique_pool_set)
f = open(’stop.txt’, ’r’)
stopwords = []
stopwords = f.read()
for word in unique_pool:
    if word in stopwords:
        #print word, "is a stopword, deleting from pool.."
        while unique_pool.count(word) > 0:
            unique_pool.remove(word)

# data extraction
selection = getKdist(len(unique_pool),62)
for idx,s in enumerate(selection):
    if s == 1:
        stegomap_values.append(unique_pool[idx])
    else:
        pass

str(unique_pool)
print "Unique Pool (",len(unique_pool), "):"
random.shuffle(stegomap_values)
stegomap = dict(zip(stegomap_values, stegomap_keys))
print unique_pool
print "\n"
print "Stegomap (",len(stegomap),"):"
print stegomap

stego_tweet_words = stego_tweet.split(" ")
payload = ""
for word in stego_tweet_words:
    if stegomap.get(word):
        payload = payload + stegomap.get(word)
print "\n"
print "Payload extracted: http://goo.gl/"+payload

