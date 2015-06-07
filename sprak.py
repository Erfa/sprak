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
        self.background_sound = sounds.play('snd/background.wav', loop=True)
        self.events           = [YesEvent(self), NoEvent(self)]
        self.event_queue      = Queue()
        self.event_worker     = EventQueueWorker(self.event_queue).start()

        self.set_volume(0.5)

    def set_volume(self, volume):
        volume = max(0.0, min(1.0, volume))
        self.background_sound.set_volume(volume)
        self.volume = volume
        logging.debug('Setting volume to {}'.format(volume))

    def click(self, x, y, button, press):
        if press:
            try:
                if button == BUTTON_PRIMARY:
                    self.event_queue.put(YesEvent(self))
                elif button == BUTTON_SECONDARY:
                    self.event_queue.put(NoEvent(self))
                elif button == BUTTON_MIDDLE:
                    if self.background_sound.is_playing():
                        self.background_sound.pause()
                    else:
                        self.background_sound.play()
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

class ResponseEvent(SprakEvent):
    def __init__(self, sprak, name, light_id):
        SprakEvent.__init__(self, sprak, name)
        self.light_id = light_id

    def _enable_light(self):
        self.sprak.lights.enable(self.light_id)

    def _disable_light(self):
        self.sprak.lights.disable(self.light_id)

    def run(self):
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

