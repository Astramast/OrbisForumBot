from RSSFeed import RSSFeed
from RSSFeedGetter import RSSFeedGetter
from OrbisForumBot import OrbisForumBot
from BotConfig import BotConfig
from sys import argv
from datetime import datetime
import discord
import time
import json

if len(argv) < 2:
	print("Usage: python main.py <config file>")
	exit(1)

with open(argv[1]) as f:
	config = json.load(f)

TIME_DELAY = int(config["timeDelay"])
if TIME_DELAY < 1:
	print("Time delay must be at least 1 (1s).")
	exit(1)

from dotenv import load_dotenv
from os import getenv

rssURL = config["rssURL"]
rssFeedGetter = RSSFeedGetter(rssURL)
rssFeed = RSSFeed(rssFeedGetter)
botConfig = BotConfig(config["botConfigFile"])
bot = OrbisForumBot(botConfig)

load_dotenv()
DISCORD_TOKEN = getenv("DISCORD_TOKEN")
bot.run(DISCORD_TOKEN)
lastTopic = None
#while True:
#	rssFeed.refresh()
#	newTopic = rssFeed.getLastTopic()
#	if newTopic != lastTopic:
#		print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - New topic: {newTopic}")
#		lastTopic = newTopic
#		bot.feed(str(newTopic))
#	time.sleep(TIME_DELAY)

