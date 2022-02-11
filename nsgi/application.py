import asyncio, typing
from .route import Route

class AsyncServer(object):
	def __init__(self) -> None:
		self.loop = asyncio.get_event_loop()
		self.routes = {}

	def route(self, path : str, method : str = "GET"):
		def wrapper(func : typing.Callable):
			self.routes[path] = Route(path, func, method)
		return wrapper