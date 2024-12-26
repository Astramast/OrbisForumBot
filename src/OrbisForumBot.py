from discord.ext import commands
import discord
import json
import requests

class OrbisForumBot(commands.Bot):
	def __init__(self, botConfig):
		super().__init__(command_prefix = botConfig.prefix, intents = botConfig.intents)
		self.dataFilename = botConfig.dataFilename
		self.appID = botConfig.appID
		self.DISCORD_TOKEN = botConfig.DISCORD_TOKEN
		self.channels = dict()
		try:
			with open(self.dataFilename, "r") as f:
				self.channels = json.load(f)
		except FileNotFoundError:
			self.saveChannels()
	
	def saveChannels(self):
		with open(self.dataFilename, "w") as f:
			json.dump(self.channels, f)
	
	@discord.app_commands.command(name="ping", description="Ping the bot")
	async def ping(self, interaction: discord.Interaction):
		await interaction.response.send_message("Pong !")
	
	@discord.app_commands.command(name="startfeed", description="Start the RSS feed")
	@discord.app_commands.checks.has_permissions(administrator = True)
	async def startFeed(self, interaction: discord.Interaction):
		self.channels[interaction.guild_id] = interaction.channel_id
		self.saveChannels()
		await interaction.response.send_message(
			f"Feed channel started ! RSS Updates will be sent here in {interaction.channel.mention}."
		)
	
	@discord.app_commands.command(name="stopfeed", description="Stop the RSS feed")
	@discord.app_commands.checks.has_permissions(administrator = True)
	async def stopFeed(self, interaction: discord.Interaction):
		del self.channels[interaction.guild_id]
		self.saveChannels()
		await interaction.response.send_message(
			f"Feed channel stopped ! RSS Updates will no longer be sent here in {interaction.channel.mention}."
		)
	
	def feed(self, topic):
		for channel in self.channels.values():
			self.get_channel(channel).send(topic)
			print(f"Sent to {channel}: {topic}")
	
	def declareCommands(self, guildID):
		url = f"https://discord.com/api/v10/applications/{self.appID}/guilds/{guildID}/commands"
		commands = [{"name": "ping", "description": "Ping the bot", "type": 1},
					{"name": "startfeed", "description": "Start the RSS feed", "type": 1},
					{"name": "stopfeed", "description": "Stop the RSS feed", "type": 1}]
		headers = {"Authorization": f"Bot {self.DISCORD_TOKEN}"}
		r = requests.post(url, headers = headers, json=commands)
		print(r)
		print(r.json())

	async def on_ready(self):
		for guild in self.guilds:
			self.declareCommands(guild.id)
			print(f"Declared commands for {guild}")
		print(f"Bot ready ! Logged in as {self.user}")
	
#	async def setup_hook(self):
#		self.tree.add_command(self.ping)
#		self.tree.add_command(self.startFeed)
#		self.tree.add_command(self.stopFeed)

