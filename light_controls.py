import asyncio
import random

import config
if config.HARDWARE_FLAG:
    import RPi.GPIO as gpio


def switch_light(cmd_str):
    if config.DEBUG_FLAG:
        print(cmd_str)
    if config.HARDWARE_FLAG:
        if cmd_str[2] == 'g':
            gpio.output(config.GREEN_LIGHT, 1)
        elif cmd_str[2] == '-':
            gpio.output(config.GREEN_LIGHT, 0)
        else:
            raise ValueError('incorrect input for green light')
        if cmd_str[1] == 'o':
            gpio.output(config.ORANGE_LIGHT, 1)
        elif cmd_str[1] == '-':
            gpio.output(config.ORANGE_LIGHT, 0)
        else:
            raise ValueError('incorrect input for orange light')
        if cmd_str[0] == 'r':
            gpio.output(config.RED_LIGHT, 1)
        elif cmd_str[0] == '-':
            gpio.output(config.RED_LIGHT, 0)
        else:
            raise ValueError('incorrect input for red light')


async def starting(loop):
    while True:
        switch_light('---');
        await asyncio.sleep(3.0, loop=loop);
        switch_light('-o-');
        await asyncio.sleep(3.0, loop=loop);
async def speaking(loop):
    while True:
        switch_light('--g');
        await asyncio.sleep(2.0, loop=loop);
async def speaking_warning(loop):
    while True:
        switch_light('-og');
        await asyncio.sleep(2.0, loop=loop);
async def questions(loop):
    while True:
        switch_light('-o-');
        await asyncio.sleep(2.0, loop=loop);
async def questions_warning(loop):
    while True:
        switch_light('ro-');
        await asyncio.sleep(2.0, loop=loop);
async def stop(loop):
    while True:
        switch_light('r--');
        await asyncio.sleep(2.0, loop=loop);
async def empty_schedule(loop):
    while True:
        switch_light(random.choice(['-','r']) + random.choice(['-', 'o']) + random.choice(['-','g']))
        await asyncio.sleep(1.0, loop=loop);
def clear():
    switch_light('---');


def debug():
    import time
    switch_light('rog')
    while True:
        pass
        
def debug_flash():
    import time
    while True:
        switch_light('rog')
        time.sleep(0.5)
        switch_light('---')
        time.sleep(0.5)

if __name__ == '__main__':
    from controller import Controller

    light_control = Controller(universal_callbacks=clear)
    light_control.start(starting)
    light_control.sleep(4.1)
    light_control.stop_all()
    light_control.start(speaking)
    light_control.sleep(6)
    light_control.stop_all()
    light_control.start(questionswarning)
    light_control.sleep(4)
    light_control.stop_all()

