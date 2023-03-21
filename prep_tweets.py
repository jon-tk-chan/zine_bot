#for data collection - tweepy API 
import tweepy
import twitter_credentials
import json

consumer_key = twitter_credentials.CONSUMER_KEY 
consumer_secret = twitter_credentials.CONSUMER_SECRET 
access_token = twitter_credentials.ACCESS_TOKEN
access_token_secret = twitter_credentials.ACCESS_SECRET

out_filename = 'tracery_str.txt'
#FUNCTIONS 
def get_urls(status_raw):
    """Return a dictionary containing all versions of the tweet photo URL
    
    Input: individual items returned by tweepy.Cursor(api.user_timeline) (tweepy.models.Status)
    
    Assume that all urls are in first item of status['entities']['media'] 
    (tweets are single images only)
    """
    status = status_raw._json
    status_dict = {
        "date": status['created_at'],
        "tweet_id": status['id'],
        "url": status['entities']['media'][0]['url'],
        "media_url": status['entities']['media'][0]['media_url'],
        "display_url": status['entities']['media'][0]['display_url'],
        "expanded_url": status['entities']['media'][0]['expanded_url']
    }

    return status_dict

def create_tracery_dict(tweets_list, return_full_dict=False):
    
    """Return a Tracery dict to copy into https://cheapbotsdonequick.com/
    
    input:
        list of tweet dicts that each contain a 'url' field 
    Assume that pages are ordered in tweet_list - written to all_pages_dict with page number as key
    
    Output:
        string containing tracery_dict in the following format: f"Writing Project: How to live with yourself (Page {page_num}//192: {tweet_dict['url']}"
    """
    i = 0
    all_pages_dict = {}
    
    for i, tweet in enumerate(tweets_list):
        page_num = i + 1
        tweet_dict = get_urls(tweet)
    #     print("DATE: ", tweet_dict['date'])
    #     print("URL: ", tweet_dict['url'])
    #     print("PAGE NUM: ", i)
        all_pages_dict[page_num] = tweet_dict

    print("PAGES PROCESSED", str(page_num))

    #create tracery format dict only containing t.co url ()
    tracery_dict = {
        "origin": []
    }
#     tweet_format = f"Writing Project: How to live with yourself (Page {page_num}//192: {tweet_dict['url']}"
    for page_num, tweet_dict in all_pages_dict.items():
        tweet_text = f"Writing Project: How to live with yourself (Page {page_num}/192): {tweet_dict['url']} "
        tracery_dict['origin'].append(tweet_text)
    
    #requires double quotes
    tracery_str = str(tracery_dict).replace("\'", "\"")

    if return_full_dict:
        return tracery_str, all_pages_dict
    else:
        return tracery_str
    

def main():
    #authenticate Twitter with credentials from twitter_credentials.py
    #EXAMPLE: https://docs.tweepy.org/en/stable/authentication.html

    auth = tweepy.OAuth2AppHandler(
        consumer_key, consumer_secret
    )
    api = tweepy.API(auth)
    #define user to collect tweets using api.search_tweets (within Cursor() module)
    #username (id) to collect: @normies_media
    #collect all pages: 192 or more individual pages/tweets

    count = 200 
    user_id="normies_media"
    tweets_list = []
    for status in tweepy.Cursor(api.user_timeline, id=user_id).items(count):
        tweets_list.append(status)
    tracery_str = create_tracery_dict(tweets_list)
    with open(out_filename, 'w') as file:
        file.write(tracery_str) 
    print("CREATED JSON: ", out_filename)

if __name__ == "__main__":
    main()