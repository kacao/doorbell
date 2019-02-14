import vlc
from vlc import *
import time
import asyncio
import ctypes

class Sound:

    def __init__(self):
        self.players = {}
        self.playing_instance = None
        self.playing_file = ''
        self.vlc_instance = vlc.Instance()
        self.should_stop_checking = False

        self.playing_instance = {
            'filepath': '',
            'should_stop': False,
            'player': None,
            'length': -1
        }

    # vlc plays in a separated threa hence we need to 
    # check for finished plays and call player.stop()
    async def background_check(self):
        while self.should_stop_checking == False:
            if self.playing_instance['should_stop'] == True:
                await self._stop()
            await asyncio.sleep(.5)

    # called when gracefully exit
    async def on_shutdown(self):
        print('media cleaning up')
        if self.playing_instance['player']:
            self.playing_instance['player'].stop()

    # reset current player's info, ready to play again
    async def _stop(self):
        self.playing_instance['should_stop'] = False
        self.playing_instance['player'].stop()
        self.playing_instance['filepath'] = ''
        self.playing_instance['player'] = None

    # unless stopped, new play is ignored until the current play is over
    async def play(self, filepath):
        # something is playing, ignore
        if self.playing_instance['player']:
            return()

        if filepath not in self.players:
            media = self.vlc_instance.media_new_path(filepath)
            p = self.vlc_instance.media_player_new()
            p.set_media(media)
            self.players[filepath] = p
        
        player = self.players[filepath]
        self.playing_instance['player'] = player
        self.playing_instance['filepath'] = filepath
        self.playing_instance['should_stop'] = False

        events = player.event_manager()
        events.event_attach(vlc.EventType.MediaPlayerEndReached, self._sound_finished)
        events.event_attach(vlc.EventType.MediaPlayerPlaying, self._sound_playing)
        player.play()

    # called by vlc when it has reached the end of a media play
    def _sound_finished(self, data):
        # this is called in a separated thread (not managed by us)
        self.playing_instance['should_stop'] = True

    # vlc starts playing, get_length() is not available before this
    def _sound_playing(self, data):
        # this is called in a separated thread (not managed by us)
        print('playing %s ms' % self.playing_instance['player'].get_length())

    async def stop(self):
        if self.playing_instance['player']:
            await self._stop()

    async def is_playing(self):
        if self.playing_instance:
            return (True, self.playing_file)
        else:
            return (False, '')
