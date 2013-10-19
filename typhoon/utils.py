from goose import Goose 
import tweepy
import re

g = Goose()
ARTICLE_LENGTH = 150

def is_news(url):
    """A function that returns TRUE if the given URL is a news article
    and FALSE if it is not
    """
    article = g.extract(url=url)
    if len(article.cleaned_text.split()) < ARTICLE_LENGTH:
        return False
    return True

def get_links(tweets):
    """Returns a list of t.co links from a list of given tweets"""
    api = tweepy.API(auth)
    page_list = []
    tweets_list = []
    links_list = []
    regex = re.compile(" http://t.co/.*")

    for page in tweepy.Cursor(api.home_timeline, count=20).pages(10):
        page_list.append(page)
    for page in page_list:
        for status in page:
           tweets_list.append(status.text)
    for elem in tweets_list:
        if ('t.co' in elem):
            links_list.append(elem)
    for tweet in tweets_list:
        print tweet