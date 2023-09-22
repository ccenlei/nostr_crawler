#!/usr/bin/python3

import abc
import calendar
import datetime
import re
from typing import List
import aiohttp

from crawl.nostr_beans import BeanFactory, Page, RequestUrl


class AbstractCrawler(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def urls_find(self, page=Page) -> List[RequestUrl]:
        pass

    @abc.abstractmethod
    def extract(self, page=Page):
        pass

    @abc.abstractmethod
    def crawl(self, nostr_url=RequestUrl) -> Page:
        pass


class CrawlerV1(AbstractCrawler):
    desc = 'nostr crawler v1.'
    # https://api.nostr.band/nostr?method=trending&type=people&date=2023-09-20
    list_url_pattern = '.*?date=(\d{4}-\d{2}-\d{2})'

    def urls_find(self, page=Page) -> List[RequestUrl]:
        src_url = page.src_url
        tar_str = src_url.url
        urls = []
        print(f'start to find urls : {tar_str}')
        if bool(re.match(self.list_url_pattern, tar_str)):
            date_match = re.search(self.list_url_pattern, tar_str)
            date_str = date_match.group(1)
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            first_day = date_obj.replace(day=1)
            _, last_day = calendar.monthrange(first_day.year, first_day.month)
            for day in range(1, last_day + 1):
                current_date = first_day.replace(day=day)
                current_date_str = current_date.strftime("%Y-%m-%d")
                url = RequestUrl(
                    f'https://api.nostr.band/nostr?method=trending&type=people&date={current_date_str}')
                urls.append(url)
        return urls

    def extract(self, page=Page):
        url = page.src_url.url
        data = page.page
        users = []
        print(f'start to extract : {url}')
        if bool(re.match(self.list_url_pattern, url)):
            peoples = data['people']
            while len(peoples) > 0:
                people = peoples.pop(0)
                profile = people['profile']
                user = BeanFactory.to_nostr_user(profile)
                users.append(user)
        return users

    async def crawl(self, nostr_url=RequestUrl) -> Page:
        url = nostr_url.url
        heads = nostr_url.heads
        timeout = nostr_url.timeout
        print(f'start to crawl : {url}')
        async with aiohttp.ClientSession() as session:
            res = await session.get(url=url, headers=heads, timeout=timeout)
            json_data = await res.json()
            page = Page(json_data, nostr_url)
            for n, v in res.cookies.items():
                n_str = str(n)
                v_str = str(v)
                # Set-Cookie: _zap=56a8ebda-44f9-4fb9-80bd-be17455d6ca4; Domain=zhihu.com; expires=Sat, 20 Sep 2025 12:58:25 GMT; Path=/
                match = re.search('=(.*?); Domain', v_str)
                page.cookies[n_str] = match.group(1)
        return page


class CrawlerFactory(object):

    @staticmethod
    def new_crawler(version: str) -> AbstractCrawler:
        if version == 'v1':
            return CrawlerV1()
        raise RuntimeError(f'Dont support such version : {version}')
