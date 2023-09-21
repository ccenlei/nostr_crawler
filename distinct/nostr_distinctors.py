#!/usr/bin/python3

import abc


class MemoryDistinctor(object):

    def __init__(self) -> None:
        self.__targets_set = set()

    def not_exist(self, target: str) -> bool:
        if target not in self.__targets_set:
            self.__targets_set.add(target)
            return True
        return False


class RedisDistinctor(object):

    def not_exist(self, target: str) -> bool:
        pass


class AbstractFactory(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def new_distinctor(self):
        pass


class MemoryFactory(AbstractFactory):

    def new_distinctor(self):
        return MemoryDistinctor()
