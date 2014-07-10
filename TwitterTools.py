import sys
import string
import json

"""
TwitterTools.py
---------------
Some functions I used to do Assignment 1 in Coursera's Introduction to Data Science course. 

"""


def buildScoresDict(afinnfile):
    """
    Returns a dict with words and their corresponding sentiment score.
    """
    scores = {} # initialize an empty dictionary
    for line in afinnfile:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.
    #print scores.items() # Print every (term, score) pair in the dictionary
    return scores

def scoreTweet(tweet, scores):
    """ 
    Takes the dict of AFINN scores and applies a score to each word in a tweet. 
    The total score of all relevant words in the tweet is summed returned as an integer.
    """
    try:
        lang = tweet['lang']
        twext = tweet['text']
    except: 
        lang = 'Not english'
        twext = ''
    # Initialise some data
    tweet_total_score = 0
    # Prepare the tweet
    clean_tweet = cleanTweetText(twext).split(' ')
    for word in clean_tweet: 
        try: word_score = scores[word]
        except: word_score = 0 
        # Add the word's score to the overall tweet score
        tweet_total_score += word_score
    # Print some output
    # print clean_tweet
    return tweet_total_score


def cleanTweetText(tweet):
    """
    Exclude hashtags, mentions and weblinks. Remove punctuation and return the cleaned text.
    """
    twext = excludeTwitterTags(tweet)
    twext = stripPunctuation(twext)
    return twext

def excludeTwitterTags(tweet):
	"""
	For a given tweet, strip out hashtags, mentions and urls for the tweet text.
	"""
	twext = tweet['text'].lower()
	if tweet['entities']['hashtags']:
		for hashtag in tweet['entities']['hashtags']:
			twext = twext.replace(hashtag['text'].lower(),"")
			if tweet['entities']['user_mentions']:
				for user_mention in tweet['entities']['user_mentions']:
					twext = twext.replace(user_mention['screen_name'].lower(),"")
			if tweet['entities']['urls']:
				for url in tweet['entities']['urls']:
					twext = twext.replace(url['url'].lower(),"")
	return twext

def stripPunctuation(text):
	""" 
	Remove punctuation from a string.
	"""
	exclude = set(string.punctuation)
    clean_text = ''.join(ch for ch in text if ch not in exclude)
    clean_text = clean_text.replace('\n',' ') # Let's account for newline characters also 
    return clean_text.encode('ascii','ignore')

def getFrequencies(tweets):
    """
    Returns a dict with words and their relative frequencies. 
    
    Input is a list of tweets with the 'clean_text' attribute already determined.
    Output is a dict with every distinct word in the set of tweets along with its' relative frequency.
    """
    total_words = 0
    word_freq = {}
    for tweet in tweets:
        twext = tweet['clean_text']
        for word in twext.split(' '):
            word = word.strip()
            if word:
                total_words += 1
                if word not in word_freq:
                    word_freq[word] = float(1)
                else:
                    word_freq[word] += 1
    for key in word_freq:
        word_freq[key] = word_freq[key]/total_words
    return word_freq

def printTopN(dict, N):
    """
    Prints the Top N key-value pairs in a dict.
    Dict must consist of string keys and numeric values
    """
    sorted_list = sorted(dict, key=dict.get, reverse=True)[0:N]
    for key in sorted_list:
        print key

def buildHashtagsDict(tweets):
    """ 
    Returns a dictionary with all hashtags in a given set of tweets, along with a count of each hashtag.
    """
    hashtags = {}
    for tweet in tweets:
        if tweet['entities']['hashtags']:
            for hashtag in tweet['entities']['hashtags']:
                tag = hashtag['text'].lower().strip()
                if tag not in hashtags:
                    hashtags[tag] = 1
                else:
                    hashtags[tag] += 1
    return hashtags

