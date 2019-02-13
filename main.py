from util import abspath, join, exists
from w import Server
from sound import Sound
import sys, getopt

class Main:

    def __init__(self, host, port, media_path):
        self.media = Sound()
        self.server = Server(host, port)
        self.dir = media_path
        self.server.on('play', self.handle_play)
        self.server.on('stop', self.handle_stop)
        self.server.on('is_playing', self.handle_is_playing)

    async def handle_play(self, action, data):
        filepath = self.get_path(data)
        code = 200
        if not exists(filepath):
            print('media not found: %s' % filepath)
            code = 404
        else:
            print('playing %s' % data['file'])
            await self.media.play(filepath)
        return (code, None)

    async def handle_stop(self, action, data):
        filepath = self.get_path(data)
        code = 200
        if not exists(filepath):
            print('media not found: %s' % filepath)
            code = 404
        else:
            print('stopping %s' % data['file'])
            await self.media.stop()
        return (code, None)

    async def handle_is_playing(self, action):
        return (200, str(await self.media.is_playing()).lower())


    def get_path(self, data):
        filename = data['file']
        return abspath(join(self.dir, filename))

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
