import logging

LIGHT_YES         = 0
LIGHT_NO          = 1
LIGHT_BODY_LOWER  = 2
LIGHT_BODY_MIDDLE = 3
LIGHT_BODY_UPPER  = 4
LIGHT_STOMAGE     = 5
LIGHT_HEAD        = 6

class LightsManager(object):
    def enable(self, light):
        logging.debug('Enabling light {}'.format(light))
