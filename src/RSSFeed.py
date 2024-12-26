from Topic import Topic

class RSSFeed():
	def __init__(self, rssFeedGetter):
		self.feedGetter = rssFeedGetter
		self.feed = self.feedGetter.getFeed()
	
	def getLastTopicTitle(self):
		return self.feed.entries[0].title
	
	def getLastTopicLink(self):
		return self.feed.entries[0].link
	
	def getLastTopicAuthor(self):
		return self.feed.entries[0].author
	
	def getLastTopic(self):
		title = self.getLastTopicTitle()
		link = self.getLastTopicLink()
		author = self.getLastTopicAuthor()
		return Topic((title, link, author))
	
	def refresh(self):
		self.feed = self.feedGetter.getFeed()

