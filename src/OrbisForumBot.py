from discord.ext import commands
import discord
import json

class OrbisForumBot(commands.Bot):
	def __init__(self, botConfig):
		super().__init__(command_prefix = botConfig.prefix, intents = botConfig.intents)
		self.dataFilename = botConfig.dataFilename
		self.channels = dict()
		try:
			with open(self.dataFilename, "r") as f:
				self.channels = json.load(f)
		except FileNotFoundError:
			self.saveChannels()
	
	def saveChannels(self):
		with open(self.dataFilename, "w") as f:
			json.dump(self.channels, f)
	
	@commands.command()
	async def ping(self, interaction: discord.Interaction):
		await interaction.response.send_message("Pong !")
	
	@commands.command()
	async def start(self, interaction: discord.Interaction):
		self.channels[interaction.guild_id] = interaction.channel_id
		self.saveChannels()
		await interaction.response.send_message(
			f"Feed channel started ! RSS Updates will be sent here in {interaction.channel.mention}."
		)
	
	@commands.command()
	async def stop(self, interaction: discord.Interaction):
		del self.channels[interaction.guild_id]
		self.saveChannels()
		await interaction.response.send_message(
			f"Feed channel stopped ! RSS Updates will no longer be sent here in {interaction.channel.mention}."
		)
	
	def feed(self, topic):
		for channel in self.channels.values():
			self.get_channel(channel).send(topic)
			print(f"Sent to {channel}: {topic}")
	
	@bot.event()
	async def on_ready(self):
		print(f"Bot ready ! Logged in as {self.user}")

