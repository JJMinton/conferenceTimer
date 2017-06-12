from datetime import datetime

import asyncio
from concurrent.futures import CancelledError
from inspect import isawaitable

import itertools
from collections import Iterable, Callable

class Controller():
    def __init__(self, loop=None, universal_callbacks=[]):
        if loop is not None:
            self.loop = loop
        if isinstance(universal_callbacks, Iterable):
            for val in universal_callbacks:
                if not isinstance(val, Callable):
                    raise TypeError('universal_callbacks must be callable or a list of callables')
            self.universal_callbacks = universal_callbacks
        elif isinstance(universal_callbacks, Callable):
            self.universal_callbacks = [universal_callbacks,]
        else:
            raise TypeError('universal_callbacks must be callable or a list of callables')
        self.tasks = []

    def __del__(self):
        self.stop_all()
        #del self.loop

    def __getitem__(self, key):
        return self.tasks[key]

    def start(self, coroutine_list):
        if callable(coroutine_list):
            coroutine_list = [coroutine_list,]
        if not isinstance(coroutine_list, Iterable):
            raise TypeError('the input must be a async function or a list of async functions')
        for coro in coroutine_list:
            print(coro)
            self.tasks.append(self.run_in_background(coro))
        return self

    def stop(self, key):
        self.tasks[key].cancel()
        asyncio.wait_for(self.tasks[key], 100, loop=self.loop)
        #try:
        #    self.loop.run_until_complete(self.tasks[key])
        #except CancelledError:
        #    pass
        del self.tasks[key]
        return self
    
    def stop_all(self, call_backs=[]):
        while self.tasks:
            self.stop(-1)
        if isinstance(call_backs, Callable):
            call_backs = [call_backs,]
        for func in call_backs + self.universal_callbacks:
            try:
                self.loop.run_until_complete(func())
            except TypeError:
                func()
        return self

    def run_in_background(self, func):
        if callable(func):
            tmp = func(self.loop)
            if asyncio.iscoroutine(tmp):
                return asyncio.ensure_future(tmp, loop=self.loop)
        raise TypeError("func must be async function that returns a coroutine.")

    def run_in_foreground(self, func):
        if callable(func):
            tmp = func(self.loop)
            if asyncio.iscoroutine(tmp):
                return self.loop.run_until_complete(asyncio.ensure_future(tmp, loop=self.loop))
        raise TypeError("func must be async function that returns a coroutine.")

    def sleep(self, sleep_time):
        self.loop.run_until_complete(asyncio.ensure_future(asyncio.sleep(sleep_time, loop=self.loop), loop=self.loop))
        return self

    def sleep_until(self, target_date_time):
        #raise NotImplementedError()
        sleep_seconds = (target_date_time - datetime.now()).total_seconds()
        self.sleep(sleep_seconds)
        return self

    @property
    def loop(self):
        if not hasattr(self, '_loop'):
            self._loop = asyncio.get_event_loop()
        return self._loop
    @loop.setter
    def loop(self, val):
        if not hasattr(self, '_loop'):
            self._loop = val
        else:
            raise ValueError('loop has already been set and cannot be reset')
    @loop.deleter
    def loop(self):
        if not hasattr(self, '_loop'):
            raise ValueError('loop has been set and cannot be deleted.')




if __name__ == '__main__':
    
    def print_wait_print(func_name, sleep_time=2):
        async def print_wait_print(loop):
            print('starting ' + func_name)
            await asyncio.sleep(sleep_time, loop=loop)
            print('ending ' + func_name)
        return print_wait_print

    async def ticker(loop):
        for i in itertools.count():
            print(i)
            await asyncio.sleep(1, loop=loop)

    control = Controller()
    control.start(ticker)
    control.start(print_wait_print('function 1'))
    control.sleep(4)
    control.start(print_wait_print('function 2'))
    control.sleep(3)
    #control.stop()
    control.start([print_wait_print('function 4',3), print_wait_print('function 3', 1)])
    control.sleep(3)
    control.start(print_wait_print('function 6',3))
    control.sleep(1)
    control.start(print_wait_print('function 5',1))
    control.sleep(2)

