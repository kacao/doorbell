import vlc

class Sound:

    def __init__(self):
        self.instances = {}

    async def play(self, filename):
        if filename not in self.instances:
            self.instances[filename] = vlc.MediaPlayer("file://" + filename)
        p = self.instances[filename]
        p.play()
        return p

    async def stop(self, filename):
        if filename in self.instances:
            self.instances[filename].stop()
