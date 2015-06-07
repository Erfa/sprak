import logging
import pyglet
from pyglet.resource import ResourceNotFoundException
from threading import Thread


class SoundManager(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True

    def run(self):
        logging.debug('Starting sound manager')
        pyglet.app.run()

    def play(self, path, loop=False, volume=None):
        logging.debug('Playing sound {}, loop={}'.format(path, loop))

        try:
            media = pyglet.resource.media(path)
            player = media.play()

            logging.info('Volume is at {}'.format(player.volume))

            if loop:
                player.eos_action = player.EOS_LOOP
    
            sound = Sound(path, player)

            if volume:
                sound.set_volume(volume)
            return sound
        except ResourceNotFoundException:
            logging.error('Could not find sound {}'.format(path))

class Sound(object):
    def __init__(self, path, player):
        self.path = path
        self.player = player

    def set_volume(self, volume):
        logging.debug('Setting volume of {} to {}'.format(self.path, volume))
        self.player.volume = volume
        return self

    def is_playing(self):
        return self.player._playing

    def play(self):
        self.player.play()
        return self

    def pause(self):
        self.player.pause()
        return self

    def stop(self):
        self.player.next()
        return self
