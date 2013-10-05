`from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
import tweepy

def verification(request):
	#verifier = request.args['oauth_verifier']

	auth = tweepy.OAuthHandler(CONSUMER,TOKEN, CONSUMER_SECRET)
	token = session['request_token']
	del session['request_token']

	auth.set_request_token(token[0], token[1])

	try:
		auth.get_access_token(verifier)
	except tweepy.TweepError:
		return HttpResponse('Error! Failed to get access token.')
	return HttpResponse('Welcome to the fray.')

def home(request):
	CONSUMER_TOKEN = 'FnQiwG9m6Qk4ttwhe8dUxA'
	CONSUMER_SECRET = 'BKMmlxWO0h35oXEb3gR7honrDcWXZGIcEQuEBp8sxv8'
	#CALLBACK_URL = 'http://127.0.0.1:8000/home/triple/'
	#session = dict()
	#db = dict()

	auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)

	try:
		redirect_url = auth.get_authorization_url()
		#request.session['request_token'] = (auth.request_token.key, auth.request_token.secret)
	except tweepy.TweepError:
		return HttpResponse('Error! Failed to get request token.')

	return redirect(redirect_url)

def homeOLD(request):
	auth = tweepy.OAuthHandler('FnQiwG9m6Qk4ttwhe8dUxA', 'BKMmlxWO0h35oXEb3gR7honrDcWXZGIcEQuEBp8sxv8')

	try:
	    redirect_url = auth.get_authorization_url()
	except tweepy.TweepError:
	    return HttpResponse('Error! Failed to get request token.')

	print 'please visit:'
	print  redirect_url 
	print 'to authenticate. Please enter code below'

	verifier = raw_input('-->')

	try:
	    auth.get_access_token(verifier)
	except:
	    print 'Error! Failed to get access token.'

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

	print links_list