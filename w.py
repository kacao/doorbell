import json
from aiohttp import web
from util import abspath, sanitize

class Server:

    def __init__(self, host, port=8080):
        self.host = host
        self.port = port
        self.handlers = {}
        self.app = web.Application()
        self.app.router.add_get('/api', self.get_handle)
        self.app.router.add_post('/api', self.post_handle)

    def on(self, action, handler):
        self.handlers[action] = handler

    async def get_handle(self, req):
        
        if req.method != 'GET':
            return web.Response(status=400)

        code = 200
        res = ''

        if 'action' in req.query:
            action = req.query['action']
            handler = self.handlers[action]
            code, res = await handler(action=action)
        text= '{"result": %s}' % res
        return web.Response(status=code, content_type='application/json', text=text)

    async def post_handle(self, req):

        if req.method != 'POST':
            return web.Response(status=400)

        code = 200

        if req.can_read_body:
            data = json.loads(await req.text())
            action = sanitize(data['action'])
            filename = sanitize(data['name'])
            if action in self.handlers:
                handler = self.handlers[action]
                code, res = await handler(action=action, data={'file': filename})
        else:
            code = 400
            print('bad request')

        return web.Response(status=code)

    def run(self):
        return web.run_app(self.app, host=self.host, port=self.port)

        
