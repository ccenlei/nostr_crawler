#!/usr/bin/python3

import abc
import json
import re

from crawl.nostr_beans import Page


class AbstractDBService(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def save_datas(self, datas, page: Page):
        pass


class FileDBService(AbstractDBService):

    def __init__(self) -> None:
        super().__init__()
        self.dir_path = '/Users/coushi/Downloads/nostr/'
        self.list_url_pattern = '.*?date=(\d{4}-\d{2}-\d{2})'

    def save_datas(self, datas, page: Page):
        url = page.src_url.url
        date_match = re.search(self.list_url_pattern, url)
        date_str = date_match.group(1)
        file_path = self.dir_path + date_str + '.json'
        with open(file_path, mode='w') as file:
            json_list = list(map(lambda x: x.to_json(), datas))
            datas_str = json.dumps(json_list)
            file.write(datas_str)


class DBServiceFactory(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def new_dbservice(self) -> AbstractDBService:
        pass


class FileDBServiceFactory(DBServiceFactory):
    def new_dbservice(self) -> AbstractDBService:
        return FileDBService()
