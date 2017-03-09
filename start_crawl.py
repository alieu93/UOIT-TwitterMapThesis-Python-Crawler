import common
import sys
import json
import time

def get_since_id(archive_file):
	max_id = 0
	try:
		with open(archive_file, "r") as f:
			for line in f.xreadlines():
				data = json.loads(line)
				if data.get('id', 0) > max_id:
					max_id = data.get('id')
	except Exception, e
		pass

	return max_id


def save_tweet(archive_file, tweet):
	with open(archive_file, "a") as f:
		print >>f, json.dumps(tweet._json)

def start_crawl(param, delay, archive_file, city):
	api = common.API()
	
	print "** STARTING CRAWL:", param

	while True:
		results = api.search(**param)
		print "[%s] Collected %d tweets, at %s " % (city, len(results), 
				time.strftime('%a %d %b %Y %H: %M %S'))

		if len(results > 0):
			param['since_id'] = max(x.id for x in results)

			for x in results:
				sys.stdout.write(".")
				save_tweet(archive_file, x)

		print 

		if delay:
			time.sleep(delay)

def main(city):
	with open("TARGET.json", "r") as f:
		TARGET = json.load(f)
	
	archive_file = "%s.tweets" % city
	geo = TARGET[city]["geo"]
	delay = TARGET[city]["delay"]
	rpp = TARGET[city]['rpp']
	since_id = get_since_id(archive_file)
	params = dict(geocode=geo, count=rpp, since_id=since_id)

	if since_id:
		print "** Resuming since last time from %s" % since_id
	else:
		print "** Starting now..."
	
	start_crawl(params, delay, archive_file, city)


if __name__ == '__main__':
	if not sys.argv[1:]:
		print >>sys.stderr, "USAGE: <TORONTO | OSHAWA>"
	else:
		city = sys.argv[1]
		main(city)

