from nsgi.application import AsyncServer
from nsgi.runner import Runner
from nsgi.responses import Response
from nsgi import Request

async def server(request : Request):
	if request.path == "/":
		res = Response("Hello.")
		return await res()
	elif request.path == "/web":
		res = """Hello. I am a webserver."""
		return res

runner = Runner(server)

runner.run()