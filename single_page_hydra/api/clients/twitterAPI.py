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



        self.twitter_search= Twitter(auth=self.aouth)




    def search(self, result):


        iterator = self.twitter_search.search.tweets(q=result, count=10, lang="en")



        list_tweets = []
        for tweet in iterator["statuses"]:


            json_tweet = json.dumps(tweet, indent=4)   # Parse the request result in json and Save in a variable


            tweets = json.loads(json_tweet)


            if 'text' in tweets:
                tweet_text = tweets['text']
                tweet_user = tweets['user']['name']
                list_tweets.append({'Text': tweet_text, 'User': tweet_user})



        return \
            {
              'Twitter': list_tweets
            }




