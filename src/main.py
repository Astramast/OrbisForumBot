from discord.ext import commands
import discord
import asyncio
import json
import threading
from time import sleep
from sys import argv
from BotConfig import BotConfig
from RSSFeed import RSSFeed
from RSSFeedGetter import RSSFeedGetter

if len(argv) == 2 and argv[1] == "--help":
	print("Usage: python main.py <config file | --help>")
	exit(0)

try:
	configFile = argv[1]
except IndexError:
	configFile = "config.json"

with open(configFile) as f:
	config = json.load(f)

TIME_DELAY = int(config["timeDelay"])
if TIME_DELAY < 1:
	print("Time delay must be at least 1 (1s).")
	exit(1)

rssURL = config["rssURL"]
rssFeedGetter = RSSFeedGetter(rssURL)
rssFeed = RSSFeed(rssFeedGetter)
botConfig = BotConfig("botConfig.json")

def saveChannels():
	with open(botConfig.dataFilename, "w") as f:
		json.dump(botChannels, f)


global bot
bot = commands.Bot(command_prefix = botConfig.prefix, intents = botConfig.intents)
botChannels = dict()
try:
	with open(botConfig.dataFilename, "r") as f:
		botChannels = json.load(f)
except FileNotFoundError:
	saveChannels()

@bot.event
async def on_ready():
	async def RSSLoop():
		lastTopic = None
		while True:
			newTopic = input("Send Message : ")
			if newTopic != lastTopic:
				for channel in botChannels.values():
					await bot.get_channel(channel).send(newTopic)
					print(f"Sent to {channel}: {newTopic}")
				lastTopic = newTopic
			sleep(TIME_DELAY)
	mainThread = threading.Thread(target=asyncio.run, args=(RSSLoop(),))
	mainThread.start()
	print(f"Bot ready ! Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
	sleep(10)
	await ctx.send("Pong !")

@bot.command()
async def startfeed(ctx):
	botChannels[ctx.guild.id] = ctx.channel.id
	saveChannels()
	await ctx.send("Feed channel started ! RSS Updates will be sent here in " + ctx.channel.mention + " .")

@bot.command()
async def stopfeed(ctx):
	del botChannels[ctx.guild.id]
	saveChannels()
	await ctx.send("Feed channel stopped ! RSS Updates will no longer be sent here in " + ctx.channel.mention + " .")

bot.run(botConfig.DISCORD_TOKEN)

