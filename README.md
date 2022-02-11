# nsgi

The newest contender in Server Gateway Interface.

## Why use this webserver?

This webserver is made with the newest version of `asyncio`, and `sockets`, it supports callablle-based interface and also class based. Not enough? Let me tell you how this project works.

## How it works

Basically, you create an application, let's say, an API, you run the api with our `Runner` class and want to visit it, you go to `http://development.com` (Go to your webserver IP), you will receive a response wich was triggerred from the `Response` you gave in the code.

It's as simple as it sounds.

### Example:

Want an example? Here:
```py
from nsgi.application import AsyncServer
from nsgi.runner import Runner
from nsgi.responses import Response

class Server(AsyncServer):
	def __init__(self) -> None:
		super().__init__()

s = server = Server()
runner = Runner(s)

@server.route("/", method="GET")
async def index(request):
	response = Response("Hello.")
	return await response()

runner.run()
```