import discord.ext.commands.bot
from discord.ext import commands
from discord.http import HTTPClient
from discord.ext import ipc

class Bot(discord.ext.commands.bot.Bot):
	def __init__(self, command_prefix, help_command=commands.DefaultHelpCommand(), description=None, loop = None, **options):
		super().__init__(command_prefix, help_command, description, **options)
		self.loop = loop
		self.server = ipc.Server(self, secret_key="AIO_SERVER")
		self.client = ipc.Client(port=8765, secret_key="AIO_SERVER")

	def run(self, token : str):
		self.server.start()
		self.loop.create_task(super().start(token))