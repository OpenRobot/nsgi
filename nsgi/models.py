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

import typing
import asyncio
import io
import email
from yarl import URL

from http import HTTPStatus


__all__ = ["Request", "HTTPRequest"]

RAW_REQUEST = """{method} /{path} HTTP/1.1\r\nHost: {host}\r\nContent-Type: {content_type}\r\nContent-Length: {content_length}\r\n\r\n{data}"""

class Request:
	"""The request that is passed into a callable or an endpoint callback

	Contains an event loop, method, headers and path to use in your callable or route callback.
	
	"""
	def __init__(self, method : str, path : str, headers : dict, loop) -> None:
		self.method = method
		self.path = path
		self.headers = headers
		self.loop : asyncio.AbstractEventLoop = loop

class HTTPRequest:
	def __init__(self, request : str, loop) -> None:
		self.request = request
		self.loop : asyncio.AbstractEventLoop = loop

	def parse(self) -> Request:
		request_str = self.request
		part_one, part_two = request_str.split('\r\n\r\n')
		http_lines = part_one.split('\r\n')
		_, http_req = part_one.split("\r\n", 1)
		method, url, version = http_lines[0].split(' ')
		message = email.message_from_file(io.StringIO(http_req))
		headers = dict(message.items())
		return Request(method, url, headers, self.loop)