import tweepy

from djangoProject.webinar.models import Webinar

api_key = 't435S90vfqri9RP50COGAsq87'
api_key_secret = '5zfesq8GnWSsHE10NmD7ycMzXabl8RquPM9khoHcWbMtknzgV7'
access_token = '1354386310715367425-98KoiNnNjbnUz6fGWZ6l14XrJ9pxbH'
access_token_secret = 'DbW2sbAmnlWoiL9s9L64TNXD34IkEB13606p1Q2ijOTxZ'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAOFSMQEAAAAATHSJofaiFmjULC%2Fn2qG3U3Yhnw8%3DViXBtEq2mRaSkbCGzFdoEWoj9Bz3cyWqsoPnCdnZAJZHfYm08Q'
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def main():

    content = get_tweet_content('Test webinar', '09:00 am', 'Https://www.seminar-live.com', ['Literature', 'History'])
    tweet(content)

def get_user():
    return api.get_user('seminarlivecom')


def count_followers(user):
    return user.followers_count



def get_tweet_content(title: str, time_str: str, url: str, hash_tag: [str]) -> str:
    content_text = "{title} starts in one hour at {time_str}. {url} ".format(title=title, time_str=time_str, url=url)
    for tag in hash_tag:
        content_text += '#' + tag + ' '
    return content_text

# return all tweets
def get_my_tweets():
    return api.user_timeline()

def remove_all_my_tweets():
    for tweet in get_my_tweets():
        remove_tweet(tweet.id)

def tweet(content: str, in_reply_to: str = None):
    return api.update_status(status=content, in_reply_to_status_id=in_reply_to)

def remove_tweet(tweet_id: int):
    print("DELETING", tweet_id)
    return api.destroy_status(id=tweet_id)
if __name__ == "__main__":
    main()
