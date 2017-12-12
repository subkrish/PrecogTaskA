import pymongo
import os
from flask import Flask, render_template, flash, request, url_for, redirect, session

app = Flask(__name__)

#MongoDB Authorization
client = pymongo.MongoClient('localhost', 27017)
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


@app.route('/')
def home():
	# return  "This is from Flask!!!"
	return render_template("index.html")

@app.route('/home')
def homeAnalysis():
	return render_template("index2.html")

@app.route('/network')
def network():
	return render_template("network.html")

@app.route('/location')
def location():
	return render_template("location.html")

@app.route('/location/DelhiPollution')
def locationDelhi():
	return render_template("locationDelhi.html")

@app.route('/location/MumbaiRains')
def locationMumbai():
	return render_template("locationMumbai.html")

@app.route('/locationactivity')
def locationactivity():
	return render_template("locationanalysis.html")

@app.route('/locationactivity/DelhiPollution')
def locationactivityDelhi():
	return render_template("locationanalysisDelhi.html")

@app.route('/locationactivity/MumbaiRains')
def locationactivityMumbai():
	return render_template("locationanalysisMumbai.html")	

@app.route('/top10hashtags')
def top10hashtags():
	return render_template("top10hashtags.html")

@app.route('/top10hashtags/DelhiPollution')
def top10hashtagsDelhi():
	return render_template("top10hashtagsDelhi.html")

@app.route('/top10hashtags/MumbaiRains')
def top10hashtagsMumbai():
	return render_template("top10hashtagsMumbai.html")

@app.route('/originalvretweet')
def originalvretweet():
	return render_template("originalvretweet.html")

@app.route('/originalvretweet/DelhiPollution')
def originalvretweetDelhi():
	return render_template("originalvretweetDelhi.html")

@app.route('/originalvretweet/MumbaiRains')
def originalvretweetMumbai():
	return render_template("originalvretweetMumbai.html")

@app.route('/typeoftweet')
def typeoftweet():
	return render_template("typeoftweet.html")

@app.route('/typeoftweet/DelhiPollution')
def typeoftweetDelhi():
	return render_template("typeoftweetDelhi.html")

@app.route('/typeoftweet/MumbaiRains')
def typeoftweetMumbai():
	return render_template("typeoftweetMumbai.html")


if __name__ == "__main__":
	app.run()