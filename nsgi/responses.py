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
from http import HTTPStatus

__all__ = ["Response", "HTMLResponse", "JSONResponse"]

RES = 'HTTP/1.1 {status} {status_msg}\r\nContent-Type: {type}\r\nContent-Encoding: UTF-8\r\nAccept-Ranges: bytes\r\nConnection: closed\r\n\r\n{data}'

class Response:
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