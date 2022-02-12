from nsgi.plugins import Bot
from nsgi.responses import Response
from nsgi.runner import Runner
from nsgi import Request

async def main(request: Request):
	bot = Bot(loop=request.loop)
	await bot.start(token="token")
	if request.path == "/":
		return Response("hello")

runner = Runner(main)

runner.run()