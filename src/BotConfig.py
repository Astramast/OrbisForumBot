from dotenv import load_dotenv
from os import getenv
import json
import discord

class BotConfig():
	def __init__(self, jsonFile):
		with open(jsonFile) as f:
			self.jsonConfig = json.load(f)
		load_dotenv()
		self.DISCORD_TOKEN = getenv("DISCORD_TOKEN")
		self.prefix = self.jsonConfig["prefix"]
		self.dataFilename = self.jsonConfig["dataFilename"]
		self.appID = self.jsonConfig["appID"]
		self.intents = discord.Intents.default()
		self.intents.message_content = True

