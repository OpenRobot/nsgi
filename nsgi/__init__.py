
"""
AsyncServer
----------

A server built with `asyncio` and `sockets`.

Example:
```python3.10
from asyncserver.application import AsyncServer
from asyncserver.runner import Runner
from asyncserver.responses import Response

server = AsyncServer()
runner = Runner(server)

@server.route("/", method="GET")
async def index():
	return Response("Hello.")

runner.run()
```

"""

from .application import AsyncServer
from .runner import Runner
from .responses import (JSONResponse, Response, HTMLResponse)
from .route import Route
from .models import *

__version__ = "1.0.0"