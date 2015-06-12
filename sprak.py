from Queue import Queue
import logging
import pygame
from pygame.constants import QUIT, K_ESCAPE, K_F11
from threading import Thread
from time import sleep

from lights import LIGHT_YES, LIGHT_NO


BUTTON_PRIMARY = 1
BUTTON_MIDDLE = 2
BUTTON_SECONDARY = 3
BUTTON_SCROLL_UP = 4
BUTTON_SCROLL_DOWN = 5

class EventQueueWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.daemon = True
        self.queue  = queue

    def run(self):
        while True:
            self.queue.get(True).run()


class SprakController(object):
    def __init__(self, sounds, lights):
        pygame.display.set_mode((320, 240))
        pygame.display.toggle_fullscreen()

        self.running          = True
        self.sounds           = sounds
        self.lights           = lights
        self.background_sound = None
        self.is_on            = False
        self.events           = [YesEvent(self), NoEvent(self)]
        self.event_queue      = Queue()
        self.event_worker     = EventQueueWorker(self.event_queue).start()

        self.set_volume(0.5)

    def set_volume(self, volume):
        volume = max(0.0, min(1.0, volume))
        self.volume = volume

        if self.background_sound:
            self.background_sound.set_volume(volume)

        logging.debug('Setting volume to {}'.format(volume))

    def run(self):
        try:
            while self.running:
                try:
                    event = pygame.event.wait()

                    if event.type == QUIT:
                        logging.debug('Received pygame quit event')
                        break
                    elif event.type == pygame.KEYDOWN:
                        if event.key == K_ESCAPE:
                            self.event_queue.put(QuitEvent(self))
                        elif event.key == K_F11:
                            pygame.display.toggle_fullscreen()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == BUTTON_PRIMARY:
                            self.event_queue.put(YesEvent(self))
                        elif event.button == BUTTON_SECONDARY:
                            self.event_queue.put(NoEvent(self))
                        elif event.button == BUTTON_MIDDLE:
                            self.event_queue.put(SprakPowerButtonEvent(self))
                        elif event.button == BUTTON_SCROLL_UP:
                            self.set_volume(self.volume + 0.1)
                        elif event.button == BUTTON_SCROLL_DOWN:
                            self.set_volume(self.volume - 0.1)
                except Exception as e:
                    logging.error(e)

            logging.debug('Stopping game')
        finally:
            pygame.quit()


class SprakEvent(object):
    def __init__(self, sprak, name):
        self.sprak = sprak
        self.name = name

    def run(self):
        logging.debug('Running event {}'.format(self.name))

class QuitEvent(SprakEvent):
    def __init__(self, sprak):
        SprakEvent.__init__(self, sprak, 'Quit')

    def run(self):
        SprakEvent.run(self)
        self.sprak.running = False

class SprakPowerButtonEvent(SprakEvent):
    def __init__(self, sprak):
        SprakEvent.__init__(self, sprak, 'PowerButton')

    def run(self):
        SprakEvent.run(self)

        if self.sprak.is_on:
            logging.debug('Turning off sprak')
            self.sprak.background_sound.fadeout(1000)
            self.sprak.sounds.play('snd/fly-by.wav')
            self.sprak.is_on = False

            for _i in range(24):
                self.sprak.lights.enable(LIGHT_YES)
                self.sprak.lights.enable(LIGHT_NO)
                sleep(0.1)
                self.sprak.lights.disable(LIGHT_YES)
                self.sprak.lights.disable(LIGHT_NO)
                sleep(0.04)
        else:
            logging.debug('Turning on sprak')
            self.sprak.background_sound = self.sprak.sounds.play('snd/background.wav', loops=-1, fadein=1000)

            self.sprak.sounds.play('snd/ascend.wav')
            sleep(0.097)

            for _i in range(0, 4):
                t = 0.075
                self.sprak.lights.enable(LIGHT_YES)
                sleep(t)
                sleep(t)
                self.sprak.lights.enable(LIGHT_NO)
                self.sprak.lights.disable(LIGHT_YES)
                sleep(t)
                self.sprak.lights.disable(LIGHT_NO)
                sleep(t)

            self.sprak.is_on = True

class ResponseEvent(SprakEvent):
    def __init__(self, sprak, name, light_id):
        SprakEvent.__init__(self, sprak, name)
        self.light_id = light_id

    def _enable_light(self):
        self.sprak.lights.enable(self.light_id)

    def _disable_light(self):
        self.sprak.lights.disable(self.light_id)

    def run(self):
        SprakEvent.run(self)

        if self.sprak.is_on:
            self.sprak.sounds.play('snd/response.wav').set_volume(1.0)
            self._disable_light()
            sleep(1.49)
            self._enable_light()
            sleep(0.367)
            self._disable_light()
            sleep(0.129)
            self._enable_light()
            sleep(0.367)
            self._disable_light()

class YesEvent(ResponseEvent):
    def __init__(self, sprak):
        ResponseEvent.__init__(self, sprak, 'Yes', LIGHT_YES)

class NoEvent(ResponseEvent):
    def __init__(self, sprak):
        ResponseEvent.__init__(self, sprak, 'No', LIGHT_NO)

