import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import matplotlib.pyplot as plt
from io import BytesIO
import base64
  
class TwitterClient(object):

    def __init__(self):

        # keys and tokens from the Twitter Dev Console
        consumer_key = '#####################'
        consumer_secret = '#######################'
        access_token = '#########################'
        access_token_secret = '#################################'
  
        # attempt authentication
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
  
    def clean_tweet(self, tweet):

        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\/\/\S+)", " ", tweet).split())
  
    def get_tweet_sentiment(self, tweet):
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
  
    def get_tweets(self, query, count = 10):
        
        # empty list to store parsed tweets
        tweets = []
  
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count)
  
            # parsing tweets one by one
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
  
            # return parsed tweets
            return tweets
  
        except tweepy.TweepError as e:
            print("Error : " + str(e))
  
def main():

    hashtagFile = open('HashtagToAnalyse.txt','r')
    hashtag = hashtagFile.read()
    hashtagFile.close()
    api = TwitterClient()
    tweets = api.get_tweets(query = hashtag, count = 100)

    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    print("Twitter says about #"+hashtag)
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    # percentage of neutral tweets
    print("Neutral tweets percentage: {} % \
        ".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets)))

    positvepercent = float(round(100*len(ptweets)/len(tweets),2))
    negativepercent = float(round(100*len(ntweets)/len(tweets),2))
    neutralpercent = float(round(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets),2))
    

    cars = ['Positive','Negative','Neutral']

    data = [positvepercent,negativepercent,neutralpercent]

    # Creating plot
    fig = plt.figure(figsize =(10, 7))
    #plt.pie(data, labels = data)
    plt.pie(data, autopct='%1.1f%%',  startangle=90)
    
    plt.legend(title="#"+hashtag,labels= cars, loc="best")
    
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

    html = 'Twitter Sentimental Analysis' + '<img src=\'data:image/png;base64,{}\'>'.format(encoded) + 'Created by Sivaraman'

    with open('index.html','w') as f:
        f.write(html)
    plt.show()

  
    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])
  
    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])
  

 

if __name__ == "__main__":
    main()
