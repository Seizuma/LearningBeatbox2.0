from config.config import *
from lib.modes.base_mode import *
import asyncio
import time


class TutorialMode(BaseMode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    patterns = [
        {
            'name': 'b',
            'sounds': ['b'],
            'threshold': {
                'power': 550000,
                'percentage': 90,
            },
            'throttle': {
                'b': 0.1
            }
        },
        {
            'name': 'k',
            'sounds': ['k'],
            'threshold': {
                'power': 300000,
                'percentage': 98,
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
                'power': 200000,
                'percentage': 98,
            },
            'throttle': {
                'hi hat': 0.05
            }
        },
        {
            'name': 'm',
            'sounds': ['m'],
            'threshold': {
                'power': 500000,
                'percentage': 98,
            },
            'throttle': {
                'm': 0.1
            }
        },
        {
            'name': 'throat bass',
            'sounds': ['throat bass'],
            'threshold': {
                'power': 650000,
                'percentage': 98,
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
                'power': 1400000,
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
                'power': 650000,
                'percentage': 98,
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
                'power': 700000,
                'percentage': 98,
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
                'power': 90000,
                'percentage': 98,
            },
            'throttle': {
                'pressurized hi hat': 0.1
            }
        },
        {
            'name': 'hollow lip roll',
            'sounds': ['hollow lip roll'],
            'threshold': {
                'power': 600000,
                'percentage': 98,
            },
            'throttle': {
                'hollow lip roll': 0.1
            }
        },
        {
            'name': 'lip roll (classic)',
            'sounds': ['lip roll (classic)'],
            'threshold': {
                'power': 400000,
                'percentage': 98,
            },
            'throttle': {
                'lip roll (classic)': 0.1
            }
        },
        {
            'name': 'Tutu (kim squeak)',
            'sounds': ['Tutu (kim squeak)'],
            'threshold': {
                'power': 200000,
                'percentage': 98,
            },
            'throttle': {
                'Tutu (kim squeak)': 0.1
            }
        },
        {
            'name': 'K Rimshot',
            'sounds': ['K Rimshot'],
            'threshold': {
                'power': 200000,
                'percentage': 98,
            },
            'throttle': {
                'K Rimshot': 0.1
            }
        },
        {
            'name': 'Palet K snare',
            'sounds': ['Palet K snare'],
            'threshold': {
                'power': 200000,
                'percentage': 98,
            },
            'throttle': {
                'Palet K Snare': 0.1
            }
        },
        {
            'name': 'Vibration Bass',
            'sounds': ['Vibration Bass'],
            'threshold': {
                'power': 200000,
                'percentage': 98,
            },
            'continual_threshold': {
                'power': 20000,
                'percentage': 60,
            },
            'throttle': {
                'Vibration Bass': 0.1
            }
        }
    ]

    def handle_sounds(self, dataDicts):
        for pattern in self.patterns:
            detection_result = self.detect(pattern['name'])
            if detection_result:
                detected_sound_characteristics = {
                    key: pattern['threshold'][key] for key in pattern['threshold']}
                if all(detected_sound_characteristics[key] >= pattern['threshold'][key] for key in pattern['threshold']):
                    print(f"Detected: {pattern['name']}")

        # for task in tasks:
        #     task.result()  # Wait for each task to complete

    def adjust_for_continuous_sounds(self, pattern):
        # Adjust the pattern if it's continuous
        if pattern['is_continuous']:
            pattern['threshold']['power'] *= 0.8
            pattern['threshold']['percentage'] *= 0.8
            for sound in pattern['throttle']:
                pattern['throttle'][sound] *= 0.8
