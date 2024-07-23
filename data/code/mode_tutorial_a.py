import sys
import json
from config.config import *
from lib.modes.base_mode import *
import time


class TutorialMode(BaseMode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_detection_time = {}

    patterns = [
        {
            'name': 'b',
            'sounds': ['b'],
            'threshold': {
                    'power': 695912,
                    'percentage': 83.77,
                    'frequency': 36.17,
            },
            'throttle': {
                'b': 0.1
            }
        },
        {
            'name': 'd (from bdb)',
            'sounds': ['d (from bdb)'],
            'threshold': {
                    'power': 200000,
                    'percentage': 83,
                    'frequency': 36,
            },
            'throttle': {
                'd (from bdb)': 0.1
            }
        },
        {
            'name': 'k',
            'sounds': ['k'],
            'threshold': {
                    'power': 250000,
                    'percentage': 98,
                    ' frequency': 75,
            },
            'throttle': {
                'k': 0.1
            }
        },
        {
            'name': 'hi hat',
            'sounds': ['hi hat'],
            'threshold': {
                    'power': 410000,
                    'percentage': 98,
                    ' frequency': 140,
            },
            'throttle': {
                'hi hat': 0.1
            }
        },
        {
            'name': 'm',
            'sounds': ['m'],
            'threshold': {
                    'power': 300000,
                    'percentage': 98,
                    'frequency': 75,
            },
            'throttle': {
                'm': 0.1
            }
        },
        {
            'name': 'throat bass',
            'sounds': ['throat bass'],
            'threshold': {
                    'power': 670000,
                    'percentage': 95,
                    'frequency': 36,
            },
            'continual_threshold': {
                'power': 50000,
                'percentage': 90,
            },
            'throttle': {
                'throat bass': 0.1
            }
        },
        {
            'name': 'lips oscilation (from pash kick)',
            'sounds': ['lips oscilation (from pash kick)'],
            'threshold': {
                    'power': 1250000,
                    'percentage': 96,
                    'frequency': 34.96,
            },
            'continual_threshold': {
                'power': 500000,
                'percentage': 90,
            },
            'throttle': {
                'lips oscilation (from pash kick)': 0.1
            }
        },
        {
            'name': 'Fart bass (villain)',
            'sounds': ['Fart bass (villain)'],
            'threshold': {
                    'power': 810000,
                    'percentage': 97,
                    'frequency': 35,
            },
            'continual_threshold': {
                'power': 410000,
                'percentage': 85,
            },
            'throttle': {
                'Fart bass (villain)': 0.1
            }
        },
        {
            'name': 'Vocalized lips oscilation',
            'sounds': ['Vocalized lips oscilation'],
            'threshold': {
                    'power': 900000,
                    'percentage': 93,
                    'frequency': 35,
            },
            'continual_threshold': {
                'power': 530000,
                'percentage': 85,
            },
            'throttle': {
                'Vocalized lips oscilation': 0.1
            }
        },
        {
            'name': 'pressurized hi hat',
            'sounds': ['pressurized hi hat'],
            'threshold': {
                    'power': 120000,
                    'percentage': 95,
                    'frequency': 140,
            },
            'throttle': {
                'pressurized hi hat': 0.1
            }
        },
        {
            'name': 'hollow lip roll',
            'sounds': ['hollow lip roll'],
            'threshold': {
                    'power': 380000,
                    'percentage': 90,
                    'frequency': 35,
            },
            'throttle': {
                'hollow lip roll': 0.1
            }
        },
        {
            'name': 'lip roll (classic)',
            'sounds': ['lip roll (classic)'],
            'threshold': {
                    'power': 115000,
                    'percentage': 96,
                    'frequency': 50,
            },
            'throttle': {
                'lip roll (classic)': 0.1
            }
        },
        {
            'name': 'Tutu (kim squeak)',
            'sounds': ['Tutu (kim squeak)'],
            'threshold': {
                    'power': 185000,
                    'percentage': 98,
                    'frequency': 100,
            },
            'throttle': {
                'Tutu (kim squeak)': 0.1
            }
        },
        {
            'name': 'K Rimshot',
            'sounds': ['K Rimshot'],
            'threshold': {
                    'power': 165000,
                    'percentage': 90,
                    'frequency': 50,
            },
            'throttle': {
                'K Rimshot': 0.1
            }
        },
        {
            'name': 'Palet K snare',
            'sounds': ['Palet K snare'],
            'threshold': {
                    'power': 160000,
                    'percentage': 95,
                    'frequency': 80,
            },
            'throttle': {
                'Palet K Snare': 0.1
            }
        },
        {
            'name': 'Vibration Bass',
            'sounds': ['Vibration Bass'],
            'threshold': {
                    'power': 760000,
                    'percentage': 98,
                    # 'frequency': 36,
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
        current_time = time.time()
        for pattern in self.patterns:
            sound_name = pattern['name']
            detection_result = self.detect(sound_name)

            if detection_result and self._can_detect_sound(sound_name, current_time):
                detected_sound_characteristics = {
                    key: pattern['threshold'][key] for key in pattern['threshold']}
                if all(detected_sound_characteristics[key] >= pattern['threshold'][key] for key in pattern['threshold']):
                    print(f"Detected: {sound_name}")
                    self.last_detection_time[sound_name] = current_time

    def _can_detect_sound(self, sound_name, current_time):
        throttle_time = self._get_throttle_time(sound_name)
        last_time = self.last_detection_time.get(sound_name, 0)
        return (current_time - last_time) > throttle_time

    def _get_throttle_time(self, sound_name):
        for pattern in self.patterns:
            if pattern['name'] == sound_name:
                return pattern['throttle'].get(sound_name, 0.05)
        return 0.05
