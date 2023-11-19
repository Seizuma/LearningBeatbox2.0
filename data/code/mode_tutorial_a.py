from config.config import *
from lib.modes.base_mode import *
import time
import aiohttp
import asyncio
import urllib.parse
import time


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


new_loop = asyncio.new_event_loop()
t = threading.Thread(target=start_loop, args=(new_loop,))
t.start()


async def send_data_to_server(pattern, detected_sound_characteristics):
    # Assuming detected_sound_characteristics is a dictionary with keys like 'power', 'percentage', etc.
    if all(detected_sound_characteristics[key] >= pattern['threshold'][key] for key in pattern['threshold']):
        encoded_data = urllib.parse.quote(pattern['sounds'][0])
        url = f"http://127.0.0.1:8001/receive_data?data={encoded_data}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        print(
                            f"Failed to send data, status code: {response.status}")
                    else:
                        print(
                            f"Data sent successfully: {pattern['sounds'][0]}")
        except Exception as e:
            print(f"Error sending data: {e}")


class TutorialMode(BaseMode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
                'percentage': 70,
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
                'percentage': 80,
            },
            'throttle': {
                'pressurized hi hat': 0.1
            }
        }
    ]

    # patternsContinuous = [
    #     {
    #         'name': 'throat bass',
    #         'sounds': ['throat bass'],
    #         'threshold': {
    #             'power': 100000,
    #             'percentage': 90,
    #         },
    #         'continual_threshold': {
    #             'power': 20000,
    #             'percentage': 60,
    #         },
    #         'throttle': {
    #             'throat bass': 0.1
    #         },
    #     },
    #     {
    #         'name': 'lips oscilation (from pash kick)',
    #         'sounds': ['lips oscilation (from pash kick)'],
    #         'threshold': {
    #             'power': 180000,
    #             'percentage': 90,
    #         },
    #         'continual_threshold': {
    #             'power': 20000,
    #             'percentage': 60,
    #         },
    #         'throttle': {
    #             'lips oscilation (from pash kick)': 0.1
    #         }
    #     }
    # ]
    # original_thresholds = {
    #     pattern['name']: pattern['threshold'].copy() for pattern in patterns}
    # last_detection_time = {pattern['name']: 0 for pattern in patterns}

    # @staticmethod
    # def adjust_threshold_based_on_interval(pattern_name):
    #     current_time = time.time()
    #     time_since_last_detection = current_time - \
    #         TutorialMode.last_detection_time.get(pattern_name, 0)
    #     for pattern in TutorialMode.patterns:
    #         if pattern['name'] == pattern_name:
    #             if time_since_last_detection < 1 / 22:
    #                 for key in pattern['threshold']:
    #                     pattern['threshold'][key] *= 0.9
    #             else:
    #                 for key in pattern['threshold']:
    #                     pattern['threshold'][key] = TutorialMode.original_thresholds[pattern_name][key]
    #             TutorialMode.last_detection_time[pattern_name] = current_time
    #             break

    def handle_sounds(self, dataDicts):
        tasks = []
        for pattern in self.patterns:
            detection_result = self.detect(pattern['name'])
            if detection_result:
                # # Adjust threshold based on interval
                # self.adjust_threshold_based_on_interval(pattern['name'])

                detected_sound_characteristics = {
                    key: pattern['threshold'][key] for key in pattern['threshold']}
                task = asyncio.run_coroutine_threadsafe(
                    send_data_to_server(pattern, detected_sound_characteristics), new_loop)
                tasks.append(task)
                print(f"Task for pattern '{pattern['name']}' created")

        for task in tasks:
            task.result()  # Wait for each task to complete

    async def send_data_and_adjust(self, pattern, new_loop):
        await send_data_to_server(pattern['sounds'][0])
        if pattern['is_continuous']:
            self.adjust_for_continuous_sounds(pattern)

    def adjust_for_continuous_sounds(self, pattern):
        # Adjust the pattern if it's continuous
        if pattern['is_continuous']:
            pattern['threshold']['power'] *= 0.8
            pattern['threshold']['percentage'] *= 0.8
            for sound in pattern['throttle']:
                pattern['throttle'][sound] *= 0.8
