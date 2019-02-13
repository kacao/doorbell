from util import abspath, join
from w import Server
from sound import Sound
import sys

class Main:

    def __init__(self, media_path):
        host = '*'
        port = 8080
        l = len(sys.argv)
        if l == 2:
            host = sys.argv[1]
        elif l > 2:
            host = sys.argv[1]
            port = sys.argv[2]
        print(sys.argv)
        self.media = Sound()
        print("host: %s / port: %s" % (host, port))
        self.server = Server(host, port)
        self.dir = media_path
        self.server.on('play', self.handle_play)
        self.server.on('stop', self.handle_stop)

    async def handle_play(self, action, data):
        filepath = self.get_path(data)
        print('playing %s' % data['file'])
        await self.media.play(filepath)

    async def handle_stop(self, action, data):
        filepath = self.get_path(data)
        print('stopping %s' % data['file'])
        await self.media.stop(filepath)

    def get_path(self, data):
        filename = data['file']
        return abspath(join(self.dir, filename))

    def run(self):
        self.server.run()

main = Main('.')
main.run()

