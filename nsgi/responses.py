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

import re
import typing
from http import HTTPStatus, cookies

__all__ = ["Response", "HTMLResponse", "JSONResponse"]

class ResponseData:
	def __init__(self, status, status_msg, type) -> None:
		self.lines = f"""HTTP/1.1 {status} {status_msg}\r\nContent-Type: {type}\r\nContent-Encoding: UTF-8\r\nAccept-Ranges: bytes\r\nConnection: closed"""

	def output(self) -> typing.Any:
		return bytes(self.lines, "ascii")

	def add_line(self, data : str):
		self.lines += f"\r\n{data}"

	def add_response(self, data):
		self.lines += f"\r\n\r\n{data}"

class Response:
	def __init__(self, data : typing.Any, status_code = 200, content_type : str = "text/html") -> None:
		self.status_code = status_code
		self.status_msg = (HTTPStatus(status_code)).phrase
		self.content_type = content_type
		self.data = data
		self.headers = {}

	def set_cookie(self, name : str, value : typing.Any):
		cookie = cookies.SimpleCookie()
		cookie[name] = value
		output = cookie.output()
		output = output.split(":")
		self.headers[output[0]] = output[1]

		
	async def __call__(self):
		res = ResponseData(self.status_code, self.status_msg, self.content_type)
		for header in self.headers:
			res.add_line(f"{header}: {self.headers[header]}")
		res.add_response(self.data)
		return res.output()

class ByteResponse(Response):
	def __init__(self, data: typing.Any, status_code=200, content_type: str = "application/octet-stream") -> None:
		super().__init__(data, status_code, content_type)

class HTMLResponse(Response):
	def __init__(self, data: typing.Any, status_code=200, content_type: str = "text/html") -> None:
		super().__init__(data, status_code, content_type)

class JSONResponse(Response):
	def __init__(self, data: typing.Any, status_code=200, content_type: str = "application/json") -> None:
		super().__init__(data, status_code, content_type)