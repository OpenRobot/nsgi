import asyncio, socket
from .application import AsyncServer
from .models import *
from .route import Route
from .responses import Response

class Runner():
	def __init__(self, application : AsyncServer) -> None:
		self.loop = application.loop
		self.app = application
		self.server = s = server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	async def read_request(self, client):
		request = ''
		while True:
			chunk = (await self.loop.sock_recv(client, 50)).decode('utf8')
			request += chunk
			if len(chunk) < 50:
				break
		return request	

	async def handle_server(self, client):
		request = await self.read_request(client)
		request = HTTPRequest(request, self.app)
		request = request.parse()
		count = 0
		c = len(self.app.routes)-1
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
				response = Response(h, status_code=404)
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
		self.server = s = server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	async def read_request(self, client):
		request = ''
		while True:
			chunk = (await self.loop.sock_recv(client, 50)).decode('utf8')
			request += chunk
			if len(chunk) < 50:
				break
		return request	

	async def handle_server(self, client):
		request = await self.read_request(client)
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