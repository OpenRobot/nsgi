"""
MIT License

Copyright (c) 2022-present OpenRobot

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

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
		self.server.start()
		return super().start(*args, **kwargs)