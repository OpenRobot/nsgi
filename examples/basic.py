from nsgi.application import AsyncServer
from nsgi.runner import Runner
from nsgi.responses import Response

class Server(AsyncServer):
	def __init__(self) -> None:
		super().__init__()

server = Server()
runner = Runner(server)

@server.route("/", method="GET")
async def index(request):
	response = Response("Hello.")
	return await response() # or return response

runner.run()