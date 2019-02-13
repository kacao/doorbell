import json
from aiohttp import web
from util import abspath, sanitize

class Server:

    def __init__(self, host, port=8080):
        self.host = host
        self.port = port
        self.handlers = {}
        self.app = web.Application()
        self.app.router.add_post('/api', self.handle)

    def on(self, action, handler):
        self.handlers[action] = handler

    async def handle(self, req):

        if req.method != 'POST':
            return
        code = 200

        if req.can_read_body:
            data = json.loads(await req.text())
            action = sanitize(data['action'])
            filename = sanitize(data['name'])
            if action in self.handlers:
                handler = self.handlers[action]
                await handler(action=action, data={'file': filename})
        else:
            code = 400
            print('bad request')

        return web.Response(status=code)

    def run(self):
        return web.run_app(self.app, host=self.host, port=self.port)

        
