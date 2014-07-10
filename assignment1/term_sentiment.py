import sys
import string
import json

"""
I want to output the sentiment of a given term, 
based on the content of all my stored tweets. 

- Input will be a word or list of words?
- For that word, cycle through each tweet
  - Determine the presence of that word in the tweet
  - If present, compute the sentiment score for the tweet and add to an array
  - Positive sentiment score is sum(scores > 0)
  - Negative sentiment score is sum(abs(scores < 0))
  - Overall sentiment is Positive Sentiment / Negative Sentiment
- Finally, print the output to sdout
"""

def lines(fp):
    print str(len(fp.readlines()))

def buildScoresDict(afinnfile):
    scores = {} # initialize an empty dictionary
    for line in afinnfile:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

    #print scores.items() # Print every (term, score) pair in the dictionary
    return scores

def buildTweetsDict(tweets_file, scores):
    tweets = []
    for line in tweets_file:
        tweet = json.loads(line)
        score = scoreTweet(tweet, scores)
        tweet['score'] = score
        tweet['clean_text'] = cleanTweetText(tweet['text'])
        tweets.append(tweet)
    return tweets

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
    return tweet_total_score

def cleanTweetText(tweet_text):
    exclude = set(string.punctuation)
    clean_tweet = ''.join(ch for ch in tweet_text if ch not in exclude)
    return clean_tweet

def buildNewWordsDict(tweets,scores):
    new_words = {}
    for tweet in tweets:
        try: twext = tweet['clean_text']
        except: pass
        if twext:
            for word in twext.split(' '):
                if word.lower() not in scores:
                    new_words[word.lower()] = [0,0,0]
    return new_words

def processNewWord(word,tweets):
    """
    For each word in the dict, cycle through the tweets and check if the word is present.
    If it's present, increment the first entry (count).
    Also increment either the second (positive sentiment) or third (negative sentiment) 
    scores, depending on the sentiment of the tweet
    """
    word_info = [0,0]
    word = word.lower()
    # Cycle through the tweets
    for tweet in tweets:
        if word in tweet['clean_text']:
            score = tweet['score']
            word_info[0] += 1
            word_info[1] += score
    # Score the sentiment of the word
    word_count = word_info[0]
    word_score = word_info[1]
    try: word_sentiment = float(word_score)/word_count
    except: word_sentiment = 0
    # Output the result
    print word.encode('utf-8'), word_sentiment


def main_test():
    sent_file = open('AFINN-111.txt')
    tweet_file = open('output.txt')
    scores = buildScoresDict(sent_file)
    tweets = buildTweetsDict(tweet_file,scores)
    new_words = buildNewWordsDict(tweets,scores)
    return scores, tweets, new_words

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    scores = buildScoresDict(sent_file)
    tweets = buildTweetsDict(tweet_file,scores)
    new_words = buildNewWordsDict(tweets,scores)
    for word in new_words: 
        processNewWord(word,tweets)

if __name__ == '__main__':
    main()
