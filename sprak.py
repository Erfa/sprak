from Queue import Queue
import logging
from pymouse import PyMouseEvent
from threading import Thread
from time import sleep

from lights import LIGHT_YES, LIGHT_NO


BUTTON_PRIMARY = 1
BUTTON_SECONDARY = 2
BUTTON_MIDDLE = 3
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


class SprakController(PyMouseEvent):
    def __init__(self, sounds, lights):
        PyMouseEvent.__init__(self)
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

    def click(self, x, y, button, press):
        if press:
            try:
                if button == BUTTON_PRIMARY:
                    self.event_queue.put(YesEvent(self))
                elif button == BUTTON_SECONDARY:
                    self.event_queue.put(NoEvent(self))
                elif button == BUTTON_MIDDLE:
                    self.event_queue.put(SprakPowerButtonEvent(self))
                elif button == BUTTON_SCROLL_UP:
                    self.set_volume(self.volume + 0.1)
                elif button == BUTTON_SCROLL_DOWN:
                    self.set_volume(self.volume - 0.1)
            except Exception as e:
                logging.error(e)

class SprakEvent(object):
    def __init__(self, sprak, name):
        self.sprak = sprak
        self.name = name

    def run(self):
        pass

class SprakPowerButtonEvent(SprakEvent):
    def __init__(self, sprak):
        SprakEvent.__init__(self, sprak, 'PowerButton')

    def run(self):
        if self.sprak.is_on:
            logging.debug('Turning off sprak')
            self.sprak.background_sound.fadeout(1000)
            self.sprak.sounds.play('snd/fly-by.wav', fadein=1000)
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
            self.sprak.background_sound = self.sprak.sounds.play('snd/background.wav', loops=-1, fadein=1)

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

