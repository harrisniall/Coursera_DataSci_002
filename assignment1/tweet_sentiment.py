import sys
import string
import json

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def buildScoresDict(afinnfile):
    scores = {} # initialize an empty dictionary
    for line in afinnfile:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

    #print scores.items() # Print every (term, score) pair in the dictionary
    return scores

def scoreTweet(tweet, scores):
    """ 
    scoreTweet takes the dict of AFINN scores and applies a score to 
    each word in a tweet.
    
    The total score of all relevant words in the tweet is summed and output to sdout.
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
    print tweet_total_score

def cleanTweetText(tweet_text):
    exclude = set(string.punctuation)
    clean_tweet = ''.join(ch for ch in tweet_text if ch not in exclude)
    return clean_tweet

def parseTweets(tweet_file, scores):
    for line in tweet_file:
        tweet = json.loads(line)
        scoreTweet(tweet, scores)


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    scores = buildScoresDict(sent_file)
    parseTweets(tweet_file, scores)

if __name__ == '__main__':
    main()
