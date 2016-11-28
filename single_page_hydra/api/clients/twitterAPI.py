'''
Handles all the requests to twitter.api
And Return a customized result
'''

import json
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
from single_page_hydra.api.keys import *


class TwitterAPI():

    def __init__(self):
        self.aouth = OAuth(Twitter_Access_Token,Twitter_Access_TokenSecret,Twitter_Consumer_Key,Twitter_Consumer_Secret)



        self.twitter_stream = TwitterStream(auth=self.aouth, domain='userstream.twitter.com')




    def search(self, query):


        iterator = self.twitter_stream.statuses.filter(track=query, language="en")


        tweet_count = 10
        list_tweets = []
        for tweet in iterator:
            tweet_count -= 1


            json_tweet = json.dumps(tweet, indent=4)   # Parse the request result in json and Save in a variable


            tweets = json.loads(json_tweet)
            if 'text' in tweets:
                tweet_text = tweets['text']
                tweet_user = tweets['user']['name']
                list_tweets.append({'Text': tweet_text, 'User': tweet_user})



            if tweet_count <= 0:

                break

        return \
            {
              'Twitter': list_tweets
            }





