import gpt_2_simple as gpt2
import tweepy
import os
import re
from random import seed
from random import randint
import time
from tweepy import OAuthHandler
import preprocessor as p

# Calls the twitter api to send out a tweet
def send_tweet(tweet, api):
	api.update_status(tweet)

# Generates a page of tweets and outputs it to output/botTweets.txt
def generateTweets():
    sess = gpt2.start_tf_sess()
    checkpoint_dir = ".\\Calvinbot\\checkpoint"
    gpt2.load_gpt2(sess, checkpoint_dir = checkpoint_dir)

    text = gpt2.generate(sess, 
                checkpoint_dir = checkpoint_dir,
                temperature=0.8,
                top_k=20,
                top_p=0.9,
                return_as_list=True
    )[0]

    out_file = open('./output/botTweets.txt', 'w', encoding='utf-8')
    out_file.write(text)
    out_file.close()

    if text != "":
        return True
    else:
        return False

# Compares with the training data to make sure it generates unique tweets
def compareWithOriginal(tweet_database):
    orig_tweet = []
    # stores all the original tweets used to train in orig_tweet list
    with open('./twitterScrubber/cleanData/new_FakeKenty_tweets_clean_train.txt', 'r', encoding='utf-8') as fp:
        tweet = fp.readline()
        while tweet:
            # Looks for actual tweets
            if tweet.strip() != "==========":
                orig_tweet.append(tweet)
            
            tweet = fp.readline()

    # compare with tweets generated from gpt-2 and take out duplicates
    num = 0
    dup = 0
    newlist = []
    for tweet in tweet_database:
        dup_found = False
        for o in orig_tweet:
            if tweet == o:
                dup += 1
                dup_found = True
        if dup_found == False:
            newlist.append(tweet)
        num += 1
        print('...Looped through {}/{} tweets and found {} duplicates'.format(num, len(tweet_database), dup))

    return newlist

# Cleans the generated tweets. Mainly looks for the n-word and gets rid of delimiters
# Outputs valid tweets to output file
# Returns a list of all valid tweets
def cleanGeneratedTweet():
    tweet_database = []
    with open('./output/botTweets.txt', 'r', encoding='utf-8') as fp:
        tweet = fp.readline()
        while tweet:
            # Looks for real tweets and puts them into a list
            if tweet.strip() != "==========":
                # Replaces N-word with bro and pushes it to the back of the list
                tweet = re.sub('(n|i){1,32}((g{2,32}|q){1,32}|[gq]{2,32})[e3r]{1,32}', 'bro', tweet)
                tweet_database.append(tweet)
            tweet = fp.readline()
            if len(tweet_database) % 10 == 0:
                print("...Generated {} tweets".format(len(tweet_database)))


    # Removing duplicate values
    print("Removing duplicate tweets...")
    tweet_database = list(set(tweet_database))

    out_file = open('./output/botTweets_clean.txt', 'w', encoding='utf-8')
    for tweet in tweet_database:
        out_file.write(tweet.strip() + '\n==========\n')
    out_file.close()

    return tweet_database

# Chooses a random tweet in our database to tweet out and returns the tweet
def chooseRandomTweet(tweet_database):
    # seed with current time in milliseconds
    seed(int(round(time.time() * 1000)))

    # Generate random number within the index
    tweet = tweet_database[randint(0, len(tweet_database))]

    return tweet

def authenticate():
    # API authentification
    consumer_key = os.environ['CALVIN_CONSUMER_KEY']
    consumer_secret = os.environ['CALVIN_CONSUMER_SECRET']

    access_token = os.environ['CALVIN_ACCESS_KEY']
    access_secret = os.environ['CALVIN_ACCESS_SECRET']

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)
    
    return api


def generateAndSendTweet(api):
    if generateTweets() == True:
        tweet_database = cleanGeneratedTweet()
        if len(tweet_database) != 0:
            tweet = chooseRandomTweet(tweet_database)
            if tweet != "":
                p.set_options(p.OPT.URL)
                tweet = p.clean(tweet)
                print(tweet)
                send_tweet(tweet, api)
            else:
                print("ERROR: Tweet not populated.")
        else:
            print("ERROR: Tweet Database not populated.")
    else:
        print("ERROR: Tweets did not generate correctly.")


api = authenticate()
generateAndSendTweet(api)