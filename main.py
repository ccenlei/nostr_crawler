#!/usr/bin/python3

import threading
import time
from crawl.nostr_beans import RequestUrl
from schedule.nostr_schedulers import AbstractExecutor, ExecutorFactory


class Processor(threading.Thread):

    def __init__(self, threadID, name, executor: AbstractExecutor):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.executor = executor

    def run(self):
        print(f'{self.threadID} - {self.name} start.')
        while self.executor.not_quit():
            self.executor.execute()
            time.sleep(30)
        print(f'{self.threadID} - {self.name} ended.')


if __name__ == '__main__':
    enter_url = RequestUrl(
        'https://api.nostr.band/nostr?method=trending&type=people&date=2023-06-01')
    executor = ExecutorFactory.new_excutor('v1', enter_url)
    processor1 = Processor(1, "Processor-1", executor)
    processor1.start()
    processor1.join()
    print("退出主线程")
