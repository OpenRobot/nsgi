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

import asyncio
import socket
import typing

from .application import AsyncServer
from .models import *
from .route import Route
from .responses import HTMLResponse


__all__ = ["Runner", "RawRunner"]

class Runner:
	def __init__(self, application : typing.Union[AsyncServer, typing.Callable]) -> None:
		self.loop = asyncio.get_event_loop()
		self.app = application
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	async def read_request(self, client):
		request = b''
		while True:
			chunk = (await self.loop.sock_recv(client, 50)).decode('utf8')
			request += chunk
			if len(chunk) < 50:
				break
		return request	

	async def handle_server(self, client: socket.socket):
		request: bytes = await self.read_request(client)
		request = request.decode('utf8')
		request = HTTPRequest(request, self.app)
		request = request.parse()
		for route in self.app.routes:
			if request.path == route and request.method == self.app.routes[route].method:
				route_ = self.app.routes[route]
				ran = await route_(request)
				response = await ran()
				if not isinstance(response, bytes):
					response = await response()
				await self.loop.sock_sendall(client, response)
				client.close()
			else:
				h = """<!DOCTYPE html>\n<h1>\n404\n</h1>\n<h2>\nNot Found\n</h2>"""
				response = HTMLResponse(h, status_code=404)
				response = await response()
				await self.loop.sock_sendall(client, response)
				client.close()


	async def start(self, host : str = "localhost", port : int = 5000):
		self.server.bind((host, port))
		self.server.listen(1)
		self.server.setblocking(False)
		while True:
			client, _ = await self.loop.sock_accept(self.server)
			await self.handle_server(client)

	def run(self, host : str = "localhost", port : int = 5000):
		try:
			self.loop.run_until_complete(self.start(host, port))
		except KeyboardInterrupt:
			self.server.close()

class RawRunner():
	def __init__(self, application : typing.Coroutine) -> None:
		self.loop = asyncio.get_event_loop()
		self.app = application
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	async def read_request(self, client):
		request = b''
		while True:
			chunk = (await self.loop.sock_recv(client, 50)).decode('utf8')
			request += chunk
			if len(chunk) < 50:
				break
		return request	

	async def handle_server(self, client: socket.socket):
		request: bytes = await self.read_request(client)
		request = request.decode("utf-8")
		request = HTTPRequest(request, self.loop)
		request = request.parse()
		response = await self.app(request)
		resp = response
		if not isinstance(resp, bytes):
			resp = await response()
		await self.loop.sock_sendall(client, resp)
		client.close()


	async def start(self, host : str = "localhost", port : int = 5000):
		self.server.bind((host, port))
		self.server.listen(1)
		self.server.setblocking(False)
		while True:
			client, _ = await self.loop.sock_accept(self.server)
			await self.handle_server(client)

	def run(self, host : str = "localhost", port : int = 5000):
		try:
			self.loop.run_until_complete(self.start(host, port))
		except KeyboardInterrupt:
			self.server.close()