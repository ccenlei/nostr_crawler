#!/usr/bin/python3

import abc
import asyncio

from crawl.nostr_beans import RequestUrl
from crawl.nostr_crawlers import CrawlerFactory
from distinct.nostr_distinctors import MemoryFactory
from schedule.nostr_db import FileDBServiceFactory


class CrawlerTask(object):
    pass


class AbstractExecutor(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def not_quit(self) -> bool:
        pass

    @abc.abstractmethod
    def execute(self):
        pass


class ExecutorV1(AbstractExecutor):
    distinctor = MemoryFactory().new_distinctor()
    url_list = []
    max_cons = 10
    quit_sig = False

    def __init__(self, enter_url: RequestUrl) -> None:
        self.url_list.append(enter_url)
        self.crawler = CrawlerFactory.new_crawler('v1')
        self.dbservice = FileDBServiceFactory().new_dbservice()

    def not_quit(self) -> bool:
        return len(self.url_list) > 0 and not self.quit_sig

    def execute(self):
        if len(self.url_list) > 0:
            async_crawls = []
            asyncio.set_event_loop(asyncio.new_event_loop())
            while len(self.url_list) > 0 and len(async_crawls) < (self.max_cons + 1):
                url = self.url_list.pop(0)
                async_crawl = asyncio.ensure_future(self.crawler.crawl(url))
                async_crawls.append(async_crawl)
            loop = asyncio.get_event_loop()
            task_future = asyncio.gather(*async_crawls)
            loop.run_until_complete(task_future)
            pages = task_future.result()
            for page in pages:
                users = self.crawler.extract(page)
                if len(users) > 0:
                    self.dbservice.save_datas(users, page)
                req_urls = self.crawler.urls_find(page)
                dist_urls = [
                    d_url for d_url in req_urls
                    if self.distinctor.not_exist(d_url.url)
                ]
                self.url_list += dist_urls
        else:
            print('所有url执行完毕, 爬虫退出.')


class ExecutorFactory(object):

    @staticmethod
    def new_excutor(version: str, enter_url: RequestUrl) -> AbstractExecutor:
        if version == 'v1':
            return ExecutorV1(enter_url)
        raise RuntimeError(f'Dont support such version : {version}')
