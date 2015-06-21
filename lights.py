import logging
import RPi.GPIO as GPIO

LIGHT_YES         = 18
LIGHT_NO          = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT_YES, GPIO.OUT)
GPIO.setup(LIGHT_NO, GPIO.OUT)

class LightsManager(object):
    def enable(self, light):
        logging.debug('Enabling light {}'.format(light))
        GPIO.output(light, False)

    def disable(self, light):
        logging.debug('Disabling light {}'.format(light))
        GPIO.output(light, True)
