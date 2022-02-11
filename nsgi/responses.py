import re
import typing
from aiohttp import ClientSession
from http import HTTPStatus

RES = 'HTTP/1.1 {status} {status_msg}\r\nContent-Type: {type}\r\nContent-Encoding: UTF-8\r\nAccept-Ranges: bytes\r\nConnection: closed\r\n\r\n{data}'

class Response():
	def __init__(self, data : typing.Any, status_code = 200, content_type : str = "text/html") -> None:
		self.status_code = status_code
		self.status_msg = (HTTPStatus(status_code)).phrase
		self.content_type = content_type
		self.data = data

	async def __call__(self):
		res = RES.format(status=self.status_code, status_msg=self.status_msg, type=self.content_type, data=self.data)
		return bytes(res, "ascii")

class HTMLResponse(Response):
	def __init__(self, data: typing.Any, status_code=200, content_type: str = "text/html") -> None:
		super().__init__(data, status_code, content_type)

class JSONResponse(Response):
	def __init__(self, data: typing.Any, status_code=200, content_type: str = "application/json") -> None:
		super().__init__(data, status_code, content_type)