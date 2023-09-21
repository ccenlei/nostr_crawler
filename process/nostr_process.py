#!/usr/bin/python3

import asyncio
import threading
import time

from crawl.nostr_beans import RequestUrl
from crawl.nostr_crawlers import CrawlerFactory
from distinct.nostr_distinctors import MemoryFactory


class CrawlerTask(object):
    pass


class Executor(object):
    distinctor = MemoryFactory().new_distinctor()
    url_list = []
    max_cons = 10
    quit_sig = False

    def __init__(self, enter_url: RequestUrl) -> None:
        self.url_list.append(enter_url)

    def not_quit(self) -> bool:
        return len(self.url_list) > 0 and not self.quit_sig

    def execute(self):
        if len(self.url_list) > 0:
            crawler = CrawlerFactory.new_crawler('v1')
            async_crawls = []
            asyncio.set_event_loop(asyncio.new_event_loop())
            while len(self.url_list) > 0 and len(async_crawls) < (self.max_cons + 1):
                url = self.url_list.pop(0)
                async_crawl = asyncio.ensure_future(crawler.crawl(url))
                async_crawls.append(async_crawl)
            loop = asyncio.get_event_loop()
            task_future = asyncio.gather(*async_crawls)
            loop.run_until_complete(task_future)
            pages = task_future.result()
            for page in pages:
                users = crawler.extract(page)
                # todo 入库users?
                print(len(users))
                req_urls = crawler.urls_find(page)
                dist_urls = [
                    d_url for d_url in req_urls
                    if self.distinctor.not_exist(d_url.url)
                ]
                self.url_list += dist_urls
        else:
            print('所有url执行完毕, 爬虫退出.')


class Processor(threading.Thread):

    def __init__(self, threadID, name, executor: Executor):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.executor = executor

    def run(self):
        print(f'{self.threadID} - {self.name} start.')
        while self.executor.not_quit:
            self.executor.execute()
            time.sleep(30)
        print(f'{self.threadID} - {self.name} ended.')
