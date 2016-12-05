import asyncio;
import time;

from controller import Controller

async def starting():
    while True:
        print('-or');
        await asyncio.sleep(2.0);
async def speaking():
    while True:
        print('g--');
        await asyncio.sleep(2.0);
async def speakingwarning():
    while True:
        print('go-');
        await asyncio.sleep(2.0);
async def questions():
    while True:
        print('-o-');
        await asyncio.sleep(2.0);
async def questionswarning():
    while True:
        print('---');
        await asyncio.sleep(1.0);
        print('-o-');
        await asyncio.sleep(1.0);
async def change():
    while True:
        print('--r');
        await asyncio.sleep(2.0);
def clear():
    print('---');


if __name__ == '__main__':

    light_control = Controller(universal_callbacks=clear)
    light_control.start(starting())
    light_control.sleep(2.1)
    light_control.stop_all()
    light_control.start(speaking())
    light_control.sleep(3)
    light_control.stop_all()
    light_control.start(questionswarning())
    light_control.sleep(2)
    light_control.stop_all()

