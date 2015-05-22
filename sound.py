import logging
import pyglet
from pyglet.resource import ResourceNotFoundException
from threading import Thread
import threading


class SoundManager(Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

    def run(self):
        logging.debug('Starting sound manager')
        pyglet.app.run()

    def play(self, path, loop=False):
        logging.debug('Playing sound {}, loop={}'.format(path, loop))

        try:
            media = pyglet.resource.media(path)
            player = media.play()
    
            if loop:
                player.eos_action = player.EOS_LOOP
    
            sound = Sound(player)
            return sound
        except ResourceNotFoundException:
            logging.error('Could not find sound {}'.format(path))

class Sound(object):
    def __init__(self, player):
        self.player = player

    def set_volume(self, volume):
        self.player.volume = volume

    def is_playing(self):
        return self.player._playing

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.next()
