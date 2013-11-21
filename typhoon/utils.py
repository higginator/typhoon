from goose import Goose 
import tweepy
import re
from django.shortcuts import render_to_response
from django.template import Context
from django.http import HttpResponse
import urllib
from summary import extract

g = Goose()
ARTICLE_LENGTH = 150

def is_news(url):
    """A function that returns TRUE if the given URL is a news article
    and FALSE if it is not
    """
    if url == None:
        return False
    try:
        article = g.extract(url=url)
        if len(article.cleaned_text.split()) < ARTICLE_LENGTH:
            return False
        return True
    except:
        return False

def is_news_and_data(url):
    """A function that returns a list of the form
        [True, title, meta_description]
        or
        [False]
    """
    result = []
    if url == None:
        return False
    try:
        article = g.extract(url=url)
        if len(article.cleaned_text.split()) < ARTICLE_LENGTH:
            result.append(False)
        else:
            title = article.title
            meta_description = article.meta_description
            result.extend([True, title, meta_description])
    except:
        result.append(False)
    return result

"""is_news function without using goose, broken
def is_news2(url):
    if url == None:
        return False
    result = extract(urllib.urlopen(url).read())
    if len(result['body'].split()) < ARTICLE_LENGTH:
        return False
    return True
"""
def get_links(auth):
    """Returns a list of t.co links from a list of given tweets"""
    api = tweepy.API(auth)
    page_list = []
    tweets_list = []
    links_list = []
    news_list = []
    regex = re.compile('http://t.co/.[a-zA-Z0-9]*')

    for page in tweepy.Cursor(api.home_timeline, count=20).pages(1):
        page_list.append(page)
    for page in page_list:
        for status in page:
           # root = etree.XML(status.text)
            #tweet = etree.tostring(root, encoding=unicode)
            tweet = status.text.encode('utf-8','ignore')
            tweets_list.append(tweet)
            #tweets_list.append(xml)
            #tweets_list.append(status.text.decode('unicode_escape').encode('ascii','ignore'))
    for tweet in tweets_list:
        links = regex.findall(tweet)
        links_list.extend(links)
    print 'The length of the links list is: ' + str(len(links_list))
    for link in links_list:
        news_and_data = is_news_and_data(link)
        if True in news_and_data:
            news_and_data.append(link)
            print news_and_data
            #[True, title, meta_description, link]
            news_list.append(news_and_data[1:])
            print str(link) + ' is a news item'
    print 'The length of the news list is: ' + str(len(news_list))


    return news_list