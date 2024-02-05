import threading
import socket
import requests
from time import time

class UpdatePosterThread(threading.Thread):
    def __init__(self, test_size):
        threading.Thread.__init__(self)
        # self.start_time = start_time
        self.test_size = test_size
        # self.duration = duration

    def run(self):
        print(f"==== test migration sender running...")
        start_time = time()
        TESTING_MIGRATION_TIMES = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        counters = [0] * len(TESTING_MIGRATION_TIMES)
        is_done = 0
        while True:
            right_now = time() - start_time

            for i in range(len(TESTING_MIGRATION_TIMES) - 1, -1, -1):
                if TESTING_MIGRATION_TIMES[i] < right_now and counters[i] == 0:
                    # TESTING_MIGRATION_DESTS
                    print(f'sending to {i} to migrate to {i+1}')
                    url = f'http://3.91.73.130:8000/assignments/postupdate'
                    data = {"source_id": i, "proxy_len": self.test_size}
                    response = requests.post(url, json=data)

                    counters[i] = 1
                    is_done += 1
            if is_done == len(TESTING_MIGRATION_TIMES):break
        print('migation work is done.')
