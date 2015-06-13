import logging
import pygame
import os
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

    def play(self, path, loops=0, volume=None, fadein=0):
        logging.debug('Playing sound {}, loops={}'.format(path, loops))

        if not path in self._sounds:
            d = os.path.dirname(os.path.realpath(__file__))
            path = os.path.join(d, path)
            print path
            self._sounds[path] = pygame.mixer.Sound(path)

        channel = self._sounds[path].play(loops=loops, fade_ms=fadein)

        return channel
