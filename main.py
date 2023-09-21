#!/usr/bin/python3

from crawl.nostr_beans import RequestUrl

from process.nostr_process import Executor, Processor


def load_tasks():
    pass


if __name__ == '__main__':
    enter_url = RequestUrl(
        'https://api.nostr.band/nostr?method=trending&type=people&date=2023-09-21')
    executor = Executor(enter_url)
    processor1 = Processor(1, "Processor-1", executor)
    processor1.start()
    processor1.join()
    print("退出主线程")
