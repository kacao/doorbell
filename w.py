import json
from aiohttp import web
from util import abspath, sanitize


class Server:

    def __init__(self, host, port, background_tasks, shutdown_tasks):
        self.host = host
        self.port = port
        self.app = web.Application()
        self.app.on_startup.append(background_tasks)
        self.app.on_cleanup.append(shutdown_tasks)
        self.post_handlers = {}
        self.get_handlers = {}

        routes = web.RouteTableDef()
        self.app.router.add_get('/api/{entity}/{attr}', self.get_handle)
        self.app.router.add_post('/api/{entity}/{item}/{action}', self.post_handle)

    def on_post(self, entity, action, handler):
        if entity not in self.post_handlers:
            self.post_handlers[entity] = {}
        self.post_handlers[entity][action] = handler

    def on_get(self, entity, handler):
        self.get_handlers[entity] = handler

    async def get_handle(self, req):
        
        code = 200
        text = ''
        info = req.match_info

        if ('entity' not in info) or ('attr' not in info):
            code = 400
            print('bad request')
        else:
            entity = sanitize(info['entity'])
            attr = sanitize(info['attr'])
            if entity in self.get_handlers:
                handler = self.get_handlers[entity]
                code, text = await handler(entity=entity, attr=attr, data={'query': req.query})
        return web.Response(status=code, content_type='application/json', text=text)

    async def post_handle(self, req):

        code = 200
        text = ''
        info = req.match_info

        if ('entity' not in info) or ('action' not in info) or ('item' not in info):
            code = 400
            print('bad request')
        else: 
            entity = sanitize(info['entity'])
            action = sanitize(info['action'])
            item = sanitize(info['item'])
            if entity in self.post_handlers:
                if action in self.post_handlers[entity]:
                    handler = self.post_handlers[entity][action]
                    code, res_text = await handler(entity=entity, action=action, item=item, data={'query': req.query, 'body': await req.text()})

        return web.Response(status=code, content_type='application/json', text=text)

    def run(self):
        return web.run_app(self.app, host=self.host, port=self.port)

        
