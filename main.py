from util import abspath, join, exists
from w import Server
from sound import Sound
import sys, getopt
import asyncio, time

class Main:

    def __init__(self, host, port, media_path):
        self.media = Sound()
        self.loop = asyncio.get_event_loop()
        self.server = Server(host, port, self.background_tasks, self.shutdown_tasks)
        self.dir = media_path
        self.server.on_post('media', 'play', self.handle_play)
        self.server.on_post('media', 'stop', self.handle_stop)
        self.server.on_get('media', self.handle_get_media)

    async def handle_play(self, entity, item, action, data):
        print('handling play')
        filepath = self.get_path(item)
        print('file path: %s' % filepath)
        code = 200
        if not exists(filepath):
            print('media not found: %s' % filepath)
            code = 404
        else:
            print('playing %s' % item)
            if self.media.playing_file != filepath:
                await self.media.play(filepath)
        return (code, None)

    async def handle_stop(self, entity, item, action, data):
        filepath = self.get_path(item)
        code = 200
        if not exists(filepath):
            print('media not found: %s' % filepath)
            code = 404
        else:
            print('stopping %s' % item)
            await self.media.stop()
        return (code, None)

    async def handle_get_media(self, entity, attr, data):
        # tiny bug, file names get case lowered
        if attr == 'is_playing':
            is_playing, item = await self.media.is_playing()
            is_playing = str(is_playing).lower()
            return (200, '{"result": %s, "item": "%s"}' % (is_playing, item)) 
        else:
            return (404, '{"result": "not found"}') 


    def get_path(self, item):
        return abspath(join(self.dir, item))

    async def background_tasks(self, app):
        asyncio.ensure_future(self.media.background_check())

    async def shutdown_tasks(self, app):
        asyncio.ensure_future(self.media.on_shutdown())

    def run(self):
        self.server.run()

def usage():
    print("Usage: main.py -h [host] -p [port] -d [media dir]")

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h:p:d:", ["host=", "port=", "dir=", "help"])
    except getopt.GetoptError as err:
        print(str(err))  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    host = '*'
    port = 8080
    media_dir = './'
    
    for o, a in opts:
        if o in ("-h", "--host"):
            host = a
        elif o in ("-p", "--port"):
            port = a
        elif o in ("-d", "--dir"):
            media_dir = a
        else:
            usage()
            sys.exit()

    Main(host, port, media_dir).run()

main()
