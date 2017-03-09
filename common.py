import tweepy
import json

def API():
	with open("API_KEY.json", "r") as f:
		keys = json.load(f)

	consumer_key = keys['consumer_key']
	consumer_secret = keys['consumer_secret']

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	api = tweepy.API(auth)
	
	return api


def geoCode(loc, radius):
	geo = GEO_CODES[loc]

	if isinstance(radius, int) or isinstance(radius, float):
		radius = "%.2fkm" % radius
	else:
		if radius.endswith("km") or radius.endswith("mi"):
			pass
		else:
			radius = "%skm" % radius
	return geo + "," + radius

def search(api, q, geo, max_count):
	all_results = []
	since_id = 0
	print 'q="%s"' % q
	print 'geo="%s"' % geo

	while len(all_results) < max_count:
		results = api.search(q=q, geocode=geo, since_id=since_id, count = 100)
		if len(results) > 0:
			all_results.extend(results)
			print "Got another %d results" % len(results)
			since_id = results.max_id()
		else:
			print "No results: bail out"
			break

	return all_results
