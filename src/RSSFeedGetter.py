import feedparser

class RSSFeedGetter():
	def __init__(self, url):
		self.url = url
	
	def getFeed(self):
		return feedparser.parse(self.url)

