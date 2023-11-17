from config.config import *
from lib.modes.base_mode import *
import time
import aiohttp
import asyncio
import urllib.parse


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


new_loop = asyncio.new_event_loop()
t = threading.Thread(target=start_loop, args=(new_loop,))
t.start()


async def send_data_to_server(data):
    print(f"Sending data to server: {data}")
    if "0.000000" not in data:
        encoded_data = urllib.parse.quote(data)
        url = f"http://127.0.0.1:8001/receive_data?data={encoded_data}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        print(
                            f"Failed to send data, status code: {response.status}")
                    else:
                        print(f"Data sent successfully: {data}")
        except Exception as e:
            print(f"Error sending data: {e}")


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

    def handle_sounds(self, dataDicts):
        tasks = []
        for pattern in self.patterns:
            detection_result = self.detect(pattern['name'])
            print(
                f"Checking pattern '{pattern['name']}': Detected = {detection_result}")
            if detection_result:
                # Correctly calling the standalone function
                task = asyncio.run_coroutine_threadsafe(
                    send_data_to_server(pattern['sounds'][0]), new_loop)
                tasks.append(task)
                print(f"Task for pattern '{pattern['name']}' created")

        # Optionally, you can wait for all tasks to complete
        for task in tasks:
            task.result()  # This will wait for each task to complete

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
