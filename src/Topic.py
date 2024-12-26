class Topic():
	def __init__(self, rssEntry):
		self.title = rssEntry[0]
		self.link = rssEntry[1]
		self.author = rssEntry[2]
	
	def __str__(self):
		return f"Nouveau post de **{self.author}** : {self.title} :\n{self.link}"
	
	def __eq__(self, other):
		if other == None:
			return False
		return (self.title == other.title and self.link == other.link and self.author == other.author)

