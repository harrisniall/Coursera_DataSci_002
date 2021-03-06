import sys
import string
import re
import json

"""
"""

def buildTweetsDict(tweets_file):
    tweets = []
    for line in tweets_file:
        tweet = json.loads(line)
        if tweet['lang'] == 'en':
            tweet['clean_text'] = cleanTweetText(tweet)
        else: 
            tweet['clean_text'] = ''
        tweets.append(tweet)
    return tweets

def cleanTweetText(tweet):
    """
    Exclude hashtags, mentions and weblinks
    Remove punctuation
    Return a clean list of words in the tweet
    """
    twext = excludeTwitterTags(tweet)
    twext = stripPunctuation(twext)
    return twext

def excludeTwitterTags(tweet):
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
    exclude = set(string.punctuation)
    exclude.add('\n') # Let's try account for newline characters also
    clean_text = ''.join(ch for ch in text if ch not in exclude)
    return clean_text.encode('ascii','ignore')

def getFrequencies(tweets):
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


def main_test():
    tweet_file = open('output.txt')
    tweets = buildTweetsDict(tweet_file)
    word_freq = getFrequencies(tweets)
    return tweets, word_freq

def main():
    tweet_file = open(sys.argv[1])
    tweets = buildTweetsDict(tweet_file)
    word_freq = getFrequencies(tweets)
    for key in word_freq:
        print key, word_freq[key]

if __name__ == '__main__':
    main()
