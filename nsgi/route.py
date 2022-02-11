import typing, datetime

class Route:
	def __init__(self, path : str, endpoint : typing.Callable[..., typing.Coroutine[typing.Any, typing.Any, typing.Any]], method : str) -> None:
		self.path = path
		self.endpoint = endpoint
		self.method = method

	async def __call__(self, request = None) -> typing.Any:
		if request:
			return await self.endpoint(request)
		return await self.endpoint()