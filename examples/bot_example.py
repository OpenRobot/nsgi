from nsgi.plugins import Bot
from nsgi.responses import Response
from nsgi.runner import Runner
from nsgi import Request

async def main(request: Request):
	if request.path == "/":
		bot = Bot(loop=request.loop)
		await bot.start(token="token")
		await (await bot.fetch_channel(channel_id)).send("Hello!")
		return Response("hello")

runner = Runner(main)

runner.run()