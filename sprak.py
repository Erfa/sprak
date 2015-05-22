import logging
from pymouse import PyMouseEvent
from time import sleep

from lights import LIGHT_YES


BUTTON_PRIMARY = 1
BUTTON_SECONDARY = 2
BUTTON_MIDDLE = 3
BUTTON_SCROLL_UP = 4
BUTTON_SCROLL_DOWN = 5

class SprakController(PyMouseEvent):
    def __init__(self, sounds, lights):
        PyMouseEvent.__init__(self)
        self.sounds           = sounds
        self.lights           = lights
        self.background_sound = sounds.play('snd/background.wav', loop=True)
        self.events           = [YesEvent(self, 'Yes')]
        self.selected_event   = 0

    def click(self, x, y, button, press):
        if press:
            try:
                if button == BUTTON_PRIMARY:
                    event = self.events[self.selected_event]
                    logging.debug(u'Running event {}'.format(event.name))
                    event.run()
                elif button == BUTTON_SECONDARY:
                    logging.debug('Reseting selected event to 0')
                    self.selected_event = 0
                elif button == BUTTON_MIDDLE:
                    if self.background_sound.is_playing():
                        self.background_sound.pause()
                    else:
                        self.background_sound.play()
                elif button == BUTTON_SCROLL_UP:
                    self.selected_event = (self.selected_event - 1) % len(self.events)
                    logging.debug('Selecting previous event ({})'.format(self.selected_event))
                elif button == BUTTON_SCROLL_DOWN:
                    self.selected_event = (self.selected_event + 1) % len(self.events)
                    logging.debug('Selecting next event ({})'.format(self.selected_event))
            except Exception as e:
                logging.error(e)

class SprakEvent(object):
    def __init__(self, sprak, name):
        self.sprak = sprak
        self.name = name

    def run(self):
        pass

class YesEvent(SprakEvent):
    def run(self):
        self.sprak.sounds.play('snd/yes.wav')
        sleep(1)
        self.sprak.lights.enable(LIGHT_YES)
        sleep(0.5)
        self.sprak.lights.disable(LIGHT_YES)
        sleep(0.1)
        self.sprak.lights.enable(LIGHT_YES)
        sleep(0.5)
        self.sprak.lights.disable(LIGHT_YES)
