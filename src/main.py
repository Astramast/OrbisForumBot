from RSSFeed import RSSFeed
from RSSFeedGetter import RSSFeedGetter
from sys import argv
import time
import threading

if len(argv) < 2:
	print("Usage: python main.py <url>")
	exit(1)

#rssURL = sys.argv[1]
rssURL = "http://orbis-naturae.forumactif.com/rss" # TODO Remove
rssFeedGetter = RSSFeedGetter(rssURL)
rssFeed = RSSFeed(rssFeedGetter)
print("Last topic: " + str(rssFeed.getLastTopic()))

