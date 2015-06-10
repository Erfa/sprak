import logging
import pygame
from threading import Thread

class SoundManager(Thread):
    def __init__(self):
        Thread.__init__(self)        
        pygame.init()
        pygame.mixer.init()
        self._sounds = {}
        self.daemon = True

    def run(self):
        logging.debug('Starting sound manager')

    def play(self, path, loop=False, volume=None):
        logging.debug('Playing sound {}, loop={}'.format(path, loop))

        if not path in self._sounds:
            self._sounds[path] = pygame.mixer.Sound(path)

        loops = -1 if loop else 1
        player = self._sounds[path].play(loops=loops)

        logging.info('Volume is at {}'.format(player.get_volume()))

        sound = Sound(path, player)

        if volume:
            sound.set_volume(volume)
        return sound

class Sound(object):
    def __init__(self, path, player):
        self.path = path
        self.player = player

    def set_volume(self, volume):
        logging.debug('Setting volume of {} to {}'.format(self.path, volume))
        self.player.set_volume(volume)
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
