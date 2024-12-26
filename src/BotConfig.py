import json
import discord

class BotConfig():
	def __init__(self, jsonFile):
		with open(jsonFile) as f:
			self.jsonConfig = json.load(f)
		self.prefix = self.jsonConfig["prefix"]
		self.dataFilename = self.jsonConfig["dataFilename"]
		self.intents = discord.Intents.default()
		self.intents.message_content = True

