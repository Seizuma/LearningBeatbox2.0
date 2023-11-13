from config.config import *
from lib.modes.base_mode import *
import time


class TutorialMode(BaseMode):

    patterns = [
        {
            'name': 'b',
            'sounds': ['b'],
            'threshold': {
                'power': 600000,
                'frequency': 34,
                'percentage': 85,
                'below_frequency': 40,
            },
            'throttle': {
                'b': 0.1
            }
        },
        {
            'name': 'k',
            'sounds': ['k'],
            'threshold': {
                'power': 270000,
                'percentage': 85,
                # 'frequency': 40,
            },
            'throttle': {
                'k': 0.1
            }
        },
        {
            'name': 'hi hat',
            'sounds': ['hi hat'],
            'threshold': {
                'power': 180000,
                'percentage': 85,
            },
            'throttle': {
                'hi hat': 0.05
            }
        },
        {
            'name': 'm',
            'sounds': ['m'],
            'threshold': {
                'power': 400000,
                'percentage': 90,
            },
            'throttle': {
                'm': 0.1
            }
        },
    ]

    def handle_sounds(self, dataDicts):
        if (self.detect('b')):
            self.press('b')
        elif (self.detect('k')):
            self.press('k')
        elif (self.detect('hi hat')):
            self.press('t')
        elif (self.detect('m')):
            self.press('m')
        return
