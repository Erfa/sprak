#!/usr/bin/env python
import logging

from lights import LightsManager
from sound import SoundManager
from sprak import SprakController


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    sounds = SoundManager()
    sounds.start()

    lights = LightsManager()

    sprak = SprakController(sounds, lights)
    sprak.run()
