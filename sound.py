import vlc
import time

class Sound:

    def __init__(self):
        self.instances = {}
        self.playing_instance = None

    async def play(self, filename):
        if self.playing_instance:
            self.playing_instance.stop()
        if filename not in self.instances:
            self.instances[filename] = vlc.MediaPlayer("file://" + filename)
        p = self.instances[filename]
        self.playing_instance = p
        p.play()
        return p

    async def stop(self):
        p = self.playing_instance
        if p and p.is_playing():
            p.stop()
            self.playing_instance = None

    async def is_playing(self):
        return self.playing_instance != None
