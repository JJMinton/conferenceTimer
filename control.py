import asyncio;
import time;
import threading;
from concurrent.futures import CancelledError;

class LightControl():
    def __init__(self, loop, cleanUpFunc=None):
        self.loop = loop;
        self.thread = None;
        self.task = None;
        self.cleanUp = cleanUpFunc;
    def start(self, func):
        if self.thread is not None:
            self.stop();
        self.task = asyncio.async(func());
        self.thread = threading.Thread(target=loop_in_thread, args=(self.loop, [self.task,]));
        self.thread.start();
    def stop(self, cleanUp=None):
        self.task.cancel();
        self.thread.join()
        self.thread = None;
        if cleanUp is not None:
            cleanUp();
        else:
            if self.cleanUp is not None:
                self.cleanUpFunc();
def loop_in_thread(loop, tasks):
    asyncio.set_event_loop(loop);
    loop.run_until_complete(asyncio.wait(tasks));

@asyncio.coroutine
def starting(name=None, endTime=None):
    print('Speaker: {:}'.format(name));
    if endTime is not None:
	print('Starting in: {:}'.format(endTime));
    while True:
        print('-or');
        yield from asyncio.sleep(2.0);
@asyncio.coroutine
def speaking(name=None, endTime=None):
    if name is not None:
        print('Speaker: {:}'.format(name));
    if endTime is not None:
	print('Time remaining: {:}'.format(endTime));
    while True:
        print('g--');
        yield from asyncio.sleep(2.0);
@asyncio.coroutine
def speakingwarning(name=None, endTime=None):
    if name is not None:
        print('Speaker: {:}'.format(name));
    if endTime is not None:
	print('Time remaining: {:}'.format(endTime));
    while True:
        print('go-');
        yield from asyncio.sleep(2.0);
@asyncio.coroutine
def questions(name=None, endTime=None):
    if name is not None:
        print('Questions for {:}'.format(name));
    if endTime is not None:
	print('Time remaining: {:}'.format(endTime));
    while True:
        print('-o-');
        yield from asyncio.sleep(2.0);
@asyncio.coroutine
def questionswarning(name=None, endTime=None):
    if name is not None:
        print('Questions for {:}'.format(name));
    if endTime is not None:
	print('Time remaining: {:}'.format(endTime));
    while True:
        print('---');
        yield from asyncio.sleep(1.0);
        print('-o-');
        yield from asyncio.sleep(1.0);
@asyncio.coroutine
def change(name=None, endTime=None):
    if name is not None:
        print('Next speaker: {:}'.format(name));
    if endTime is not None:
	print('Starting at: {:}'.format(endTime));
    while True:
        print('--r');
        yield from asyncio.sleep(2.0);


lightControl = LightControl(asyncio.get_event_loop());

        

if __name__ == '__main__':

    lightControl.start(starting);
    time.sleep(2.1);
    #lightControl.stop()
    #print(lightControl.loop.is_running())
    lightControl.start(speaking);
    time.sleep(3);
    #lightControl.stop();
    lightControl.start(questionwarning);
    time.sleep(6);
    lightControl.stop(lambda: print('---'));

