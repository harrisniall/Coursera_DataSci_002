import sys
import string
import json

"""
"""

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

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
        tweet['stateUS'] = getState(tweet, states)
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

def getState(tweet,states):
    """
    Check the place object in the tweet:
    - Determine if it originates from the US
    - If yes, identify the state code and return it
    """
    state = ''
    place = tweet['place']
    if place and place['country_code'] == 'US':
        location = place['full_name']
        # Place will be something like "Houston, TX" ... 
        try: 
            state = location.split(',')[1].strip().upper()
            if state in states: return state
            else: return ''
        except: pass
    return state

def buildStateHappinessDict(tweets):
    """
    Returns a dict with US states and an average happiness score
    based on the content of the tweets
    """
    states_sentiment = {}
    states_count = {}
    for tweet in tweets:
        state = tweet['stateUS']
        score = tweet['score']
        if state:
            if state not in states_sentiment:
                states_sentiment[state] = float(score)
                states_count[state] = 1
            else: 
                states_sentiment[state] += score
                states_count[state] += 1
    for key in states_sentiment:
        states_sentiment[key] = states_sentiment[key]/states_count[key]
    return states_sentiment

def printTopN(dict, N):
    """
    Prints the Top N key-value pairs in a dict.
    Dict must consist of string keys and numeric values
    """
    sorted_list = sorted(dict, key=dict.get, reverse=True)[0:N]
    for key in sorted_list:
        print key


def main_test():
    sent_file = open('AFINN-111.txt')
    tweet_file = open('output.txt')
    scores = buildScoresDict(sent_file)
    tweets = buildTweetsDict(tweet_file,scores)
    states_sentiment = buildStateHappinessDict(tweets)
    return scores, tweets, states_sentiment

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    scores = buildScoresDict(sent_file)
    tweets = buildTweetsDict(tweet_file,scores)
    states_sentiment = buildStateHappinessDict(tweets)
    printTopN(states_sentiment, 1)

if __name__ == '__main__':
    main()
