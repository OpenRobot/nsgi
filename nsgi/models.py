import typing, json, email, io, asyncio
from yarl import URL
from http import HTTPStatus

RAW_REQUEST = """{method} /{path} HTTP/1.1\r\nHost: {host}\r\nContent-Type: {content_type}\r\nContent-Length: {content_length}\r\n\r\n{data}"""

class Request:
	def __init__(self, method : str, path : str, headers : dict, loop) -> None:
		self.method = method
		self.path = path
		self.headers = headers
		self.loop : asyncio.AbstractEventLoop = loop

class HTTPRequest:
	def __init__(self, request : str, loop) -> None:
		self.request = request
		self.loop : asyncio.AbstractEventLoop = loop

	def parse(self):
		request_str = self.request
		part_one, part_two = request_str.split('\r\n\r\n')
		http_lines = part_one.split('\r\n')
		_, http_req = part_one.split("\r\n", 1)
		method, url, version = http_lines[0].split(' ')
		message = email.message_from_file(io.StringIO(http_req))
		headers = dict(message.items())
		return Request(method, url, headers, self.loop)