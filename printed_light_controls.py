import asyncio;
import time;

from controller import Controller

async def starting(loop):
    while True:
        print('-or');
        await asyncio.sleep(2.0, loop=loop)
async def speaking(loop):
    while True:
        print('g--');
        await asyncio.sleep(2.0, loop=loop)
async def speakingwarning(loop):
    while True:
        print('go-');
        await asyncio.sleep(2.0, loop=loop)
async def questions(loop):
    while True:
        print('-o-');
        await asyncio.sleep(2.0, loop=loop)
async def questionswarning(loop):
    while True:
        print('---');
        await asyncio.sleep(1.0, loop=loop)
        print('-o-');
        await asyncio.sleep(1.0, loop=loop)
async def stop(loop):
    while True:
        print('--r');
        await asyncio.sleep(2.0, loop=loop)
def clear():
    print('---');


if __name__ == '__main__':

    light_control = Controller(universal_callbacks=clear)
    light_control.start(starting)
    light_control.sleep(2.1)
    light_control.stop_all()
    light_control.start(speaking)
    light_control.sleep(3)
    light_control.stop_all()
    light_control.start(questionswarning)
    light_control.sleep(2)
    light_control.stop_all()

