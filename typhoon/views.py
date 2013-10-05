from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import Context
from settings import CONSUMER_TOKEN, CONSUMER_SECRET
import tweepy

"""
	def testing_settings_import(request):
		return HttpResponse(CONSUMER_TOKEN + ' ' + CONSUMER_SECRET)
"""

def verification(request):
	#verifier = request.args['oauth_verifier']

	auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
	request_token = request.session['request_token']
	auth.set_request_token(request_token[0], request_token[1])
	request.session.delete('request_token')

	try:
		verifier = request.GET.get('oauth_verifier')
		auth.get_access_token(verifier)
		return get_tweets_with_links(auth)
	except tweepy.TweepError:
		return HttpResponse('Error! Failed to get access token.')

def home(request):
	#CONSUMER_TOKEN = 'FnQiwG9m6Qk4ttwhe8dUxA'
	#CONSUMER_SECRET = 'BKMmlxWO0h35oXEb3gR7honrDcWXZGIcEQuEBp8sxv8'
	#CALLBACK_URL = 'http://127.0.0.1:8000/home/triple/'
	#session = dict()
	#db = dict()

	auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)

	try:
		redirect_url = auth.get_authorization_url()
		request.session['request_token'] = (auth.request_token.key, auth.request_token.secret)
	except tweepy.TweepError:
		return HttpResponse('Error! Failed to get request token.')

	return redirect(redirect_url)

def get_tweets_with_links(auth):
	api = tweepy.API(auth)

	n=0
	page_list = []

	for page in tweepy.Cursor(api.user_timeline, count=20).pages(10):
	    page_list.append(page)

	tweets_list = []

	for page in page_list:
	    for status in page:
	       tweets_list.append(status.text)

	links_list = []
	for elem in tweets_list:
	    if ('t.co' in elem):
	        links_list.append(elem)

	#print links_list
	#return HttpResponse(links_list)
	return render_to_response('typhoon_mockup.html', Context({'links_list': links_list}))

