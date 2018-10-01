#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import itertools
import re
import tweepy
import json
import jsonpickle
import pymongo
import collections
import operator
import pycountry
import pytz
import time
import datetime
import plotly
import pygal
import requests
from googletrans import Translator
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.tokenize import word_tokenize
from matplotlib import cm
import plotly.plotly as py
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

placesDict = {'London' : 'United Kingdom',
			  'Buenos Aires' : 'Argentina',
			  'Quito' : 'Ecuador',
			  'Athens' : 'Greece',
			  'Amsterdam' : 'The Netherlands',
			  'Pacific Time (US & Canada)' : 'United States',
			  'Jerusalem' : 'Israel',
			  'Mountain Time (US & Canada)' : 'United States',
			  'Caracas' : 'Venezuela',
			  'Eastern Time (US & Canada)' : 'United States',
			  'Baghdad' : 'Iraq',
			  'Karachi' : 'Pakistan',
			  'Greenland' : 'Denmark',
			  'Islamabad' : 'China',
			  'Mexico City' : 'Mexico',
			  'Arizona' : 'United States',
			  'Asia/Karachi' : 'Pakistan',
			  'Atlantic Time (Canada)' : 'Canada',
			  'Brussels' : 'Belgium',
			  'Brasilia' : 'Brazil',
			  'Kuwait' : 'Kuwait',
			  'Sydney' : 'Australia',
			  'Hong Kong' : 'Hong Kong',
			  'Abu Dhabi' : 'United Arab Emirates',
			  'Asia/Tbilisi' : 'Georgia',
			  'New Delhi' : 'India',
			  'Bern' : 'Switzerland',
			  'Baku' : 'Azerbaijan',
			  'Riyadh' : 'Saudi Arabia',
			  'Kyiv' : 'Ukraine',
			  'Asia/Dushanbe' : 'Tajikistan',
			  'Central Time (US & Canada)' : 'United States',
			  'Dublin' : 'Ireland',
			  'Hawaii' : 'United States',
			  'Europe/London' : 'United Kingdom',
			  'Nairobi' : 'Kenya',
			  'Chennai' : 'India',
			  'Rome' : 'Italy',
			  'Kolkata' : 'India',
			  'Alaska' : 'United States',
			  'Copenhagen' : 'The Netherlands',
			  'Mumbai' : 'India',
			  'Central America' : 'Venezuela',
			  'Ljubljana' : 'Slovenia',
			  'Asia/Riyadh' : 'Saudi Arabia',
			  'Europe/Amsterdam' : 'The Netherlands',
			  'Casablanca' : 'Morocco',
			  'Belgrade' : 'Serbia',
			  'Paris' : 'France',
			  'Brisbane' : 'Australia',
			  'Moscow' : 'Russia',
			  'Saskatchewan' : 'Canada',
			  'Yerevan' : 'Armenia',
			  'Midway Island' : 'United States',
			  'Urumqi' : 'China',
			  'International Date Line West' : 'New Zealand',
			  'Muscat' : 'Oman',
			  'Melbourne' : 'Australia',
			  'Auckland' : 'New Zealand',
			  'Australia/Sydney' : 'Australia',
			  'EST' : 'United States',
			  'Seoul' : 'South Korea',
			  'Santiago' : 'Chile',
			  'Tokyo' : 'Japan',
			  'Tehran' : 'Iran',
			  'Asia/Kolkata' : 'India',
			  'Berlin' : 'Germany',
			  'Tijuana' : 'Mexico',
			  'Asia/Calcutta' : 'India',
			  'Lima' : 'Peru',
			  'Vienna' : 'Austria',
			  'Prague' : 'Czech Republic',
			  'Perth' : 'Australia',
			  'Wellington' : 'New Zealand',
			  'CST' : 'United States',
			  'Madrid' : 'Spain',
			  'Beijing' : 'China',
			  'Cairo' : 'Egypt',
			  'West Central Africa' : 'Nigeria',
			  'America/Detroit' : 'Unites States',
			  'Bogota' : 'Columbia',
			  'Stockholm' : 'Sweden',
			  'Sarajevo' : 'Bosnia and Herzegovina',
			  'Harare' : 'Zimbabwe',
			  'Africa/Johannesburg' : 'South Africa',
			  'Asia/Dubai' : 'United Arab Emirates',
			  'Minsk' : 'Belarus',
			  'Bucharest' : 'Romania'}

# Twitter Authorization
CONS_KEY = 'UW2jEHLjIKZmKBHTGmz3OWRTz'
CONS_SECRET = 'bIiTEcCAUDCW9p2tQtsFRP9WKajFsfyVf4L4z2KgjalaIk4vd6'
ACC_KEY = ''
ACC_SECRET = ''

auth = tweepy.AppAuthHandler(CONS_KEY, CONS_SECRET)
# auth.set_access_token(ACC_KEY, ACC_SECRET)

api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

print api.rate_limit_status()['resources']['search']
print ''

#MongoDB Authorization
client = pymongo.MongoClient('18.216.51.154', 27017)
db = client.precogBase

# Air Pollution in Delhi/NCR Hashtags
smogInDelhi = db.smogInDelhiCollection
myRightToBreathe = db.myRightToBreatheCollection
delhiSmog = db.delhiSmogCollection
delhiPollution = db.delhiPollutionCollection
cropBurning = db.cropBurningCollection

# Mumbai Rains Hashtags
mumbaiRains = db.mumbaiRainsCollection
cycloneOckhi = db.cycloneOckhiCollection
mumbaiCyclone = db.mumbaiCycloneCollection
ockhiCyclone = db.ockhiCycloneCollection


#Plotly Authorization
plotly.tools.set_credentials_file(username='imsubkrishd', api_key='pK0piKHX4C7jKPUScsTL')

maxTweets = 2500

tknzr = TweetTokenizer()

def isFloat(n):
	try:
		answer = bool(re.match(r'^-?\d+(\.\d+)?$', n))
	except UnicodeEncodeError:
		pass

	return answer

def makeCountries():
	countries = {}
	for i in range(len(pycountry.countries)):
		countries[list(pycountry.countries)[i].name.lower()] = 0

	return countries

def searchForTweets(collection):
	count = 0
	for tweet in tweepy.Cursor(api.search, q = '#OckhiCyclone', count = 100, lang = 'en', include_entities = True).items(maxTweets):
		count += 1
		try:
			collection.insert(tweet._json)
			# print tweet._json['text']
		except:
			pass
		# f.write(jsonpickle.encode(tweet._json, unpicklable = False) + '\n')
		print count
		print ''

def originalVRetweet():
	retweetCount = 0
	originalCount = 0
	for tweet in mumbaiCyclone.find():
		try:
			if tweet['retweeted_status']:
				retweetCount += 1
				# print tweet['text']
				print "retweetCount: " + str(retweetCount)
				print ""
		except:
			originalCount += 1
			print "originalCount: " + str(originalCount)
			print ""

	print "New collection"

	for tweet in mumbaiRains.find():
		try:
			if tweet['retweeted_status']:
				retweetCount += 1
				# print tweet['text']
				print "retweetCount: " + str(retweetCount)
				print ""
		except:
			originalCount += 1
			print "originalCount: " + str(originalCount)
			print ""

	print "New collection"

	for tweet in ockhiCyclone.find():
		try:
			if tweet['retweeted_status']:
				retweetCount += 1
				# print tweet['text']
				print "retweetCount: " + str(retweetCount)
				print ""
		except:
			originalCount += 1
			print "originalCount: " + str(originalCount)
			print ""

	print "New collection"

	for tweet in cycloneOckhi.find():
		try:
			if tweet['retweeted_status']:
				retweetCount += 1
				# print tweet['text']
				print "retweetCount: " + str(retweetCount)
				print ""
		except:
			originalCount += 1
			print "originalCount: " + str(originalCount)
			print ""

	print "New collection"

	print "Total: " + str(retweetCount + originalCount)

	labels = ['Original Tweets', 'Retweeted Tweets']
	values = [originalCount, retweetCount]
	colors = ['#5DA5DA', 'F15854',]

	trace = go.Pie(labels=labels, values=values,
	               hoverinfo='label+percent', textinfo='value', 
	               textfont=dict(size=20),
	               marker=dict(colors=colors, 
	                           line=dict(color='#000000', width=2)))

	py.plot([trace], filename='styled_pie_chart')

def typeOfTweet(): # Separate Media into Images and Videos
	textCount = 0
	imageCount = 0
	textAndImageCount = 0
	collections = [smogInDelhi, delhiSmog, delhiPollution, myRightToBreathe, cropBurning]
	for collection in collections:
		for tweet in collection.find():
			if tweet['text'] == None:
				imageCount += 1
				# print "imageCount: " + str(imageCount)
				# print ""
			elif len(tweet['entities']) == 4:
				textCount += 1
				# print "textCount: " + str(textCount)
				# print ""
			else:
				textAndImageCount += 1
				# print "textAndImageCount: " + str(textAndImageCount)
				# print ""

	print "imageCount: " + str(imageCount)
	print "textCount: " + str(textCount)
	print "textAndImageCount: " + str(textAndImageCount)

	labels = ['Only Media', 'Only Text', 'Text and Media']
	values = [imageCount, textCount, textAndImageCount]
	colors = ['#5DA5DA', '#F15854', '#DECF3F']

	trace = go.Pie(labels=labels, values=values,
	               hoverinfo='label+percent', textinfo='value', 
	               textfont=dict(size=20),
	               marker=dict(colors=colors, 
	                           line=dict(color='#000000', width=2)))

	py.plot([trace], filename='styled_pie_chart')

countries2 = makeCountries()
def countryTweets():
	countries3 = {}
	collections = [delhiSmog, delhiPollution, smogInDelhi, myRightToBreathe, cropBurning]
	collections1 = [mumbaiCyclone, mumbaiRains, cycloneOckhi, ockhiCyclone]
	twitCountry = []

	for collection in collections1:
		for tweet in collection.find():
			twitCountry.extend(word_tokenize(tweet['user']['location'].lower()))

	for collection in collections1:
		for tweet in collection.find():
			if tweet['place'] != None:
				if tweet['place']['country'].lower() in makeCountries():
					countries2[tweet['place']['country'].lower()] += 1
			elif tweet['user']['time_zone'] != None:
				if tweet['user']['time_zone'] in placesDict:
					if placesDict[tweet['user']['time_zone']].lower() in makeCountries():
						countries2[placesDict[tweet['user']['time_zone']].lower()] += 1

	for k, v in countries2.items():
		if v == 0:
			del countries2[k]

	for key in sorted(countries2, key = countries2.__getitem__):
		print "%s: %s" % (key, countries2[key])
	print ''

	for key, value in countries2.iteritems():

		country = pycountry.countries.get(name=key.title())
		alpha2 = country.alpha_2.lower()
		print alpha2
		countries3[alpha2] = value


	print countries3

	worldmap_chart = pygal.maps.world.World()
	worldmap_chart.title = 'Location of Tweets by Country'
	worldmap_chart.add('For Mumbai Rains', countries3)
	worldmap_chart.render_to_file("locationMap2.svg")

def locationOfTweets2():
	collections = [delhiSmog, delhiPollution, smogInDelhi, myRightToBreathe, cropBurning]
	collections1 = [mumbaiRains, mumbaiCyclone, cycloneOckhi, ockhiCyclone]
	locationDict = {}
	count1 = 0
	count2 = 0
	count3 = 0
	for collection in collections1:
		print collection
		for tweet in collection.find():
			count2 += 1
			if tweet['place'] == None:
				count1 += 1
			else:
				# print tweet['place']['full_name']
				# if "New Delhi" in tweet['place']['full_name']:
				# 	tweet['place']['full_name'] = "New Delhi, India"
				# else:
				# 	tweet['place']['full_name'] = "Everything Else"

				if "Mumbai" in tweet['place']['full_name']:
					tweet['place']['full_name'] = "Mumbai, India"
				else:
					tweet['place']['full_name'] = "Everything Else"

				if tweet['place']['full_name'] not in locationDict:
					locationDict[tweet['place']['full_name']] = 1
				else:
					locationDict[tweet['place']['full_name']] += 1

				count3 += 1
				# print count2
				# print "Total locations: " + str(count3)
				# print ""

	for key in sorted(locationDict, key = locationDict.__getitem__):
		print "%s: %s" % (key, locationDict[key])
	print ''

	labels = locationDict.keys()
	values = locationDict.values()
	colors = ['#5DA5DA', '#F15854']

	trace = go.Pie(labels=labels, values=values,
	               hoverinfo='label+percent', textinfo='value', 
	               textfont=dict(size=20),
	               marker=dict(colors=colors, 
	                           line=dict(color='#000000', width=2)))

	py.plot([trace], filename='styled_pie_chart')

def distributionOfOriginal(collection):
	retweetCount = 0
	originalCount = 0
	tweetDict = {}
	for tweet in collection.find():
		try:
			if tweet['retweeted_status']:
				retweetCount += 1
				# print tweet['text']
				# print "retweetCount: " + str(retweetCount)
				# print ""
		except:
			originalCount += 1
			print "Fav Count: " + str(tweet['favorite_count'])
			print "originalCount: " + str(originalCount)
			print ""
			if tweet['id'] not in tweetDict and tweet['favorite_count'] != 0:
				tweetDict[tweet['id_str']] = tweet['favorite_count']

	for key in sorted(tweetDict, key = tweetDict.__getitem__):
		print "%s: %s" % (key, tweetDict[key])
	print ''


	trace0 = go.Bar(
	    x=tweetDict.keys(),
		y=tweetDict.values(),
		marker=dict(
			color='rgb(158,202,225)',
			line=dict(
				color='rgb(8,48,107)',
				width=1.5,
			)
		),
		opacity=0.6
	)

	data = [trace0]
	layout = go.Layout(
		title='Original Tweet Favorite Count Distribution',
	)

	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename='text-hover-bar')

def wordsFromTweets():
	tweetListFiltered = set()
	for tweet in smogInDelhi.find():
		tweetList = tknzr.tokenize(tweet['text'].lower().encode('utf-8'))
		for word in tweetList:
			if word.startswith("#"):
				try:
					tweetListFiltered.add(str(word))
				except:
					pass

	for tweet in delhiPollution.find():
		tweetList = tknzr.tokenize(tweet['text'].lower().encode('utf-8'))
		for word in tweetList:
			if word.startswith("#"):
				try:
					tweetListFiltered.add(str(word))
				except:
					pass

	for tweet in delhiSmog.find():
		tweetList = tknzr.tokenize(tweet['text'].lower().encode('utf-8'))
		for word in tweetList:
			if word.startswith("#"):
				try:
					tweetListFiltered.add(str(word))
				except:
					pass

	for tweet in cropBurning.find():
		tweetList = tknzr.tokenize(tweet['text'].lower().encode('utf-8'))
		for word in tweetList:
			if word.startswith("#"):
				try:
					tweetListFiltered.add(str(word))
				except:
					pass

	for tweet in myRightToBreathe.find():
		tweetList = tknzr.tokenize(tweet['text'].lower().encode('utf-8'))
		for word in tweetList:
			if word.startswith("#"):
				try:
					tweetListFiltered.add(str(word))
				except:
					pass

	for tweet in mumbaiRains.find():
		tweetList = tknzr.tokenize(tweet['text'].lower().encode('utf-8'))
		for word in tweetList:
			if word.startswith("#"):
				try:
					tweetListFiltered.add(str(word))
				except:
					pass

	for tweet in mumbaiCyclone.find():
		tweetList = tknzr.tokenize(tweet['text'].lower().encode('utf-8'))
		for word in tweetList:
			if word.startswith("#"):
				try:
					tweetListFiltered.add(str(word))
				except:
					pass

	for tweet in cycloneOckhi.find():
		tweetList = tknzr.tokenize(tweet['text'].lower().encode('utf-8'))
		for word in tweetList:
			if word.startswith("#"):
				try:
					tweetListFiltered.add(str(word))
				except:
					pass

	for tweet in ockhiCyclone.find():
		tweetList = tknzr.tokenize(tweet['text'].lower().encode('utf-8'))
		for word in tweetList:
			if word.startswith("#"):
				try:
					tweetListFiltered.add(str(word))
				except:
					pass
				


	print len(tweetListFiltered)

def top10Handles(topic):
	if topic == "Delhi Pollution":
		hashtagDict = {}
		for tweet in smogInDelhi.find():
			tweetList = tknzr.tokenize(tweet['text'].lower().encode('utf-8'))
			for word in tweetList:
				if word.startswith("#"):
					if word not in hashtagDict:
						hashtagDict[word] = 1
					else:
						hashtagDict[word] += 1

		for tweet in myRightToBreathe.find():
			tweetList = tknzr.tokenize(tweet['text'].lower().encode('utf-8'))
			for word in tweetList:
				if word.startswith("#"):
					if word not in hashtagDict:
						hashtagDict[word] = 1
					else:
						hashtagDict[word] += 1

		for tweet in delhiPollution.find():
			tweetList = tknzr.tokenize(tweet['text'].lower().encode('utf-8'))
			for word in tweetList:
				if word.startswith("#"):
					if word not in hashtagDict:
						hashtagDict[word] = 1
					else:
						hashtagDict[word] += 1

		for tweet in cropBurning.find():
			tweetList = tknzr.tokenize(tweet['text'].lower().encode('utf-8'))
			for word in tweetList:
				if word.startswith("#"):
					if word not in hashtagDict:
						hashtagDict[word] = 1
					else:
						hashtagDict[word] += 1

		for tweet in delhiSmog.find():
			tweetList = tknzr.tokenize(tweet['text'].lower().encode('utf-8'))
			for word in tweetList:
				if word.startswith("#"):
					if word not in hashtagDict:
						hashtagDict[word] = 1
					else:
						hashtagDict[word] += 1

		hashtagDictNew = dict(sorted(hashtagDict.iteritems(), key = operator.itemgetter(1), reverse=True)[:11])

		hashtagDictNew.pop('#', None)


	elif topic == "Mumbai Rains":
		hashtagDict = {}
		for tweet in mumbaiRains.find():
			tweetList = tknzr.tokenize(tweet['text'].lower().encode('utf-8'))
			for word in tweetList:
				if word.startswith("#"):
					if word not in hashtagDict:
						hashtagDict[word] = 1
					else:
						hashtagDict[word] += 1

		for tweet in mumbaiCyclone.find():
			tweetList = tknzr.tokenize(tweet['text'].lower().encode('utf-8'))
			for word in tweetList:
				if word.startswith("#"):
					if word not in hashtagDict:
						hashtagDict[word] = 1
					else:
						hashtagDict[word] += 1

		for tweet in ockhiCyclone.find():
			tweetList = tknzr.tokenize(tweet['text'].lower().encode('utf-8'))
			for word in tweetList:
				if word.startswith("#"):
					if word not in hashtagDict:
						hashtagDict[word] = 1
					else:
						hashtagDict[word] += 1

		for tweet in cycloneOckhi.find():
			tweetList = tknzr.tokenize(tweet['text'].lower().encode('utf-8'))
			for word in tweetList:
				if word.startswith("#"):
					if word not in hashtagDict:
						hashtagDict[word] = 1
					else:
						hashtagDict[word] += 1

		hashtagDictNew = dict(sorted(hashtagDict.iteritems(), key = operator.itemgetter(1), reverse=True)[:11])

		hashtagDictNew.pop('#', None)


	for key in sorted(hashtagDictNew, key = hashtagDictNew.__getitem__):
		print "%s: %s" % (key, hashtagDictNew[key])
	print ''

	trace0 = go.Bar(
	    x=hashtagDictNew.keys(),
		y=hashtagDictNew.values(),
		marker=dict(
			color='rgb(158,202,225)',
			line=dict(
				color='rgb(8,48,107)',
				width=1.5,
			)
		),
		opacity=0.6
	)

	data = [trace0]
	layout = go.Layout(
		title='Top 10 Handles',
	)

	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename='top10Handles')

def favAndRetCounter():
	favoriteCount1 = 0
	retweetCount1 = 0
	favoriteCount2 = 0
	retweetCount2 = 0
	collections1 = [delhiSmog, smogInDelhi, myRightToBreathe, cropBurning, delhiPollution]
	collections2 = [mumbaiRains, mumbaiCyclone, cycloneOckhi, ockhiCyclone]

	for collection in collections1:
		for tweet in collection.find():
			retweetCount1 += tweet['retweet_count']
			favoriteCount1 += tweet['favorite_count']

	for collection in collections2:
		for tweet in collection.find():
			retweetCount2 += tweet['retweet_count']
			favoriteCount2 += tweet['favorite_count']

	print "Delhi Fav: " + str(favoriteCount1)
	print "Delhi Ret: " + str(retweetCount1)
	print "Mumbai Fav: " + str(favoriteCount2)
	print "Mumbai Ret: " + str(retweetCount2)

def network():
	i = 1
	users = {}
	links = {}
	for tweet in rain.find():
		if(tweet['user']['id'] not in users):
			users[tweet['user']['id']] = i
			i = i + 1
		for x in tweet['entities']['user_mentions']:
			if(x['id'] not in users):
				users[x['id']] = i
				i = i + 1
				links[users[tweet['user']['id']]] = users[x['id']]
	with open('userNodesRain.csv','w') as f:
		w = csv.writer(f)
		for key, value in users.items():
			w.writerow([key,value])
	with open('userEdgesRain.csv','w') as f:
		w = csv.writer(f)
		for key, value in links.items():
			w.writerow([key,value])

def timeOfTweets():
	# collections = [delhiSmog, delhiPollution, smogInDelhi, myRightToBreathe, cropBurning]
	# collections1 = [mumbaiRains, mumbaiCyclone, cycloneOckhi, ockhiCyclone]
	# dateDiction = {}
	# for tweet in smogInDelhi.find():
	# 	d = datetime.datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
	# 	newDate = d.date()
	# 	# newDate2 = mdates.strpdate2num(newDate)
	# 	if newDate not in dateDiction:
	# 		dateDiction[newDate] = 1
	# 	else:
	# 		dateDiction[newDate] += 1

	# for tweet in delhiSmog.find():
	# 	d = datetime.datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
	# 	newDate = d.date()
	# 	# newDate2 = mdates.strpdate2num(newDate)
	# 	if newDate not in dateDiction:
	# 		dateDiction[newDate] = 1
	# 	else:
	# 		dateDiction[newDate] += 1

	# for tweet in delhiPollution.find():
	# 	d = datetime.datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
	# 	newDate = d.date()
	# 	# newDate2 = mdates.strpdate2num(newDate)
	# 	if newDate not in dateDiction:
	# 		dateDiction[newDate] = 1
	# 	else:
	# 		dateDiction[newDate] += 1

	# for tweet in myRightToBreathe.find():
	# 	d = datetime.datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
	# 	newDate = d.date()
	# 	# newDate2 = mdates.strpdate2num(newDate)
	# 	if newDate not in dateDiction:
	# 		dateDiction[newDate] = 1
	# 	else:
	# 		dateDiction[newDate] += 1

	# for tweet in cropBurning.find():
	# 	d = datetime.datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
	# 	newDate = d.date()
	# 	# newDate2 = mdates.strpdate2num(newDate)
	# 	if newDate not in dateDiction:
	# 		dateDiction[newDate] = 1
	# 	else:
	# 		dateDiction[newDate] += 1

	# print dateDiction
	# print ''

	# # newDateDiction = collections.OrderedDict(sorted(dateDiction.items()))
	# newDateDiction = collections.OrderedDict(sorted(dateDiction.items()))
	# # newDateDiction = dict(sorted(dateDiction.iteritems(), key = operator.itemgetter(1), reverse=True)[:])

	# # print newDateDiction

	# # for key in sorted(dateDiction, key = dateDiction.__getitem__):
	# #     print "%s: %s" % (key, dateDiction[key])
	# # print ''

	# fig = plt.figure(figsize = (6*3.13,3.1*3.13))
	# plt.plot_date(x = newDateDiction.keys(), y = newDateDiction.values(), fmt="r-")
	# plt.title("Time-Series")
	# plt.ylabel("Tweets")
	# plt.grid(True)
	# plt.show()

# {datetime.date(2017, 12, 8): 1377, datetime.date(2017, 12, 3): 139, datetime.date(2017, 12, 9): 1172, datetime.date(2017, 12, 4): 551, datetime.date(2017, 12, 5): 5310, datetime.date(2017, 12, 6): 1814, datetime.date(2017, 12, 7): 2161}
	police1 = go.Scatter(
					x=[datetime.date(2017, 12, 3), datetime.date(2017, 12, 4), datetime.date(2017, 12, 5), datetime.date(2017, 12, 6), datetime.date(2017, 12, 7), datetime.date(2017, 12, 8), datetime.date(2017, 12, 9)],
					y=[139, 551, 5310, 1814, 2161, 1377, 1172],
					name = "Mumbai Rains",
					line = dict(color = '#ff0000'))

	data = [police1]

	fig = dict(data = data)

	py.plot(fig, filename = "MumbaiRains Time-Series")



if __name__ == "__main__":
	# top10Handles("Delhi Pollution")
	# top10Handles("Mumbai Rains")
	# wordsFromTweets()
	# distributionOfOriginal(delhiSmog)
	# countryTweets()
	# locationOfTweets2()
	# typeOfTweet()
	# originalVRetweet()
	# favAndRetCounter()
	# country = pycountry.countries.get(name='india'.title())
	# print country.alpha_2.lower()
	timeOfTweets()











# #SmogInDelhi - 2053 tweets
# #MyRightToBreathe - 519 tweets
# #DelhiSmog - 5000 tweets
# #DelhiPollution - 1930 tweets
# #CropBurning - 12 tweets

# Total Tweets - 9628 tweets


# #MumbaiRains - 5000 tweets
# #CycloneOckhi - 5000 tweets
# #MumbaiCyclone - 24 tweets
# #OckhiCyclone - 2500 tweets

# Total Tweets - 12524 tweets

## Total Tweets - 22038 tweets






# AIzaSyDaSFqcrQSduebsIoAzYQpfaUb5Al41KZ0

# AIzaSyD7hnJz_D2wykA9DHbionFyPjqWbOA-NVc

# AIzaSyBIcMYuMddLO4vRVbDQoR2Sx_aOMavt8G4

# AIzaSyCELYB-LGMPWLNahxccwG9oCR9xmLTxF3M
