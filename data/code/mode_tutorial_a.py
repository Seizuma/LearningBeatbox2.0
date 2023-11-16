from config.config import *
from lib.modes.base_mode import *
import time


class TutorialMode(BaseMode):

    patterns = [
        {
            'name': 'b',
            'sounds': ['b'],
            'threshold': {
                'power': 155000,
                'frequency': 34,
                'percentage': 77,
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
                'power': 75000,
                'percentage': 95,
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
                'power': 60000,
                'percentage': 90,
            },
            'throttle': {
                'hi hat': 0.05
            }
        },
        {
            'name': 'm',
            'sounds': ['m'],
            'threshold': {
                'power': 80000,
                'percentage': 80,
            },
            'throttle': {
                'm': 0.1
            }
        },
        {
            'name': 'throat bass',
            'sounds': ['throat bass'],
            'threshold': {
                'power': 100000,
                'percentage': 90,
            },
            'continual_threshold': {
                'power': 20000,
                'percentage': 60,
            },
            'throttle': {
                'throat bass': 0.1
            }
        },
        {
            'name': 'lips oscilation (from pash kick)',
            'sounds': ['lips oscilation (from pash kick)'],
            'threshold': {
                'power': 180000,
                'percentage': 90,
            },
            'continual_threshold': {
                'power': 20000,
                'percentage': 60,
            },
            'throttle': {
                'lips oscilation (from pash kick)': 0.1
            }
        },
        {
            'name': 'Fart bass (villain)',
            'sounds': ['Fart bass (villain)'],
            'threshold': {
                'power': 180000,
                'percentage': 90,
            },
            'continual_threshold': {
                'power': 20000,
                'percentage': 60,
            },
            'throttle': {
                'Fart bass (villain)': 0.1
            }
        },
        {
            'name': 'Vocalized lips oscilation',
            'sounds': ['Vocalized lips oscilation'],
            'threshold': {
                'power': 180000,
                'percentage': 90,
            },
            'continual_threshold': {
                'power': 20000,
                'percentage': 60,
            },
            'throttle': {
                'Vocalized lips oscilation': 0.1
            }
        },
        {
            'name': 'pressurized hi hat',
            'sounds': ['pressurized hi hat'],
            'threshold': {
                'power': 40000,
                'percentage': 90,
            },
            'throttle': {
                'pressurized hi hat': 0.1
            }
        }
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
        elif (self.detect('throat bass')):
            self.press('o')
        elif (self.detect('lips oscilation (from pash kick)')):
            self.press('v')
        elif (self.detect('Fart bass (villain)')):
            self.press('f')
        elif (self.detect('Vocalized lips oscilation')):
            self.press('v')
            self.press('e')
            self.press('u')
        elif (self.detect('pressurized hi hat')):
            self.press('t')
            self.press('s')
        return


"""
patternsDiscrete = [
        {
            'name': 'b',
            'sounds': ['b'],
            'threshold': {
                'power': 155000,
                'frequency': 34,
                'percentage': 77,
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
                'power': 75000,
                'percentage': 95,
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
                'power': 60000,
                'percentage': 90,
            },
            'throttle': {
                'hi hat': 0.05
            }
        },
        {
            'name': 'm',
            'sounds': ['m'],
            'threshold': {
                'power': 80000,
                'percentage': 80,
            },
            'throttle': {
                'm': 0.1
            }
        },
    ],

    patternsContinuous = [
        {
            {
                'name': 'throat bass',
                        'sounds': ['throat bass'],
                        'threshold': {
                            'power': 100000,
                            'percentage': 90,
                        },
                'continual_threshold': {
                            'power': 20000,
                            'percentage': 60,
                        },
                'throttle': {
                            'throat bass': 0.1
                        }
            },
            {
                'name': 'lips oscilation (from pash kick)',
                'sounds': ['lips oscilation (from pash kick)'],
                'threshold': {
                    'power': 180000,
                    'percentage': 90,
                },
                'continual_threshold': {
                    'power': 20000,
                    'percentage': 60,
                },
                'throttle': {
                    'lips oscilation (from pash kick)': 0.1
                }
            }
        }
    ] 
    """
