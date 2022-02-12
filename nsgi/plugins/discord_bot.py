import discord
from discord.ext import commands
from discord.http import HTTPClient
from discord.ext import ipc
from typing import *
import asyncio

class Bot(discord.Client):
	def __init__(self, *, loop: Optional[asyncio.AbstractEventLoop] = None, **options: Any):
		super().__init__(loop=loop, intents=discord.Intents.all(), **options)
		self.server = ipc.Server(self, secret_key="AIO_SERVER")
		self.client = ipc.Client(port=8765, secret_key="AIO_SERVER")

	@property
	def user(self):
		return self.__user

	async def start(self, bot = True, *args, **kwargs):
		ran = await self.http.static_login(bot=bot, *args, **kwargs)
		self.__user = ran