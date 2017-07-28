import asyncio

import RPi.GPIO as gpio

import config

gpio.setmode(config.PIN_MODE)
gpio.setup(config.GREEN_LIGHT, gpio.OUT)
gpio.setup(config.ORANGE_LIGHT, gpio.OUT)
gpio.setup(config.RED_LIGHT, gpio.OUT)

def switch_light(cmd_str):
    if cmd_str[0] == 'g':
        gpio.output(config.GREEN_LIGHT, 0)
    elif cmd_str[0] == '-':
        gpio.output(config.GREEN_LIGHT, 1)
    else:
        raise ValueError('incorrect input for green light')
    if cmd_str[1] == 'o':
        gpio.output(config.ORANGE_LIGHT, 0)
    elif cmd_str[1] == '-':
        gpio.output(config.ORANGE_LIGHT, 1)
    else:
        raise ValueError('incorrect input for orange light')
    if cmd_str[2] == 'r':
        gpio.output(config.RED_LIGHT, 0)
    elif cmd_str[2] == '-':
        gpio.output(config.RED_LIGHT, 1)
    else:
        raise ValueError('incorrect input for red light')


async def starting(loop):
    while True:
        switch_light('-or');
        await asyncio.sleep(2.0, loop=loop);
async def speaking(loop):
    while True:
        switch_light('g--');
        await asyncio.sleep(2.0, loop=loop);
async def speakingwarning(loop):
    while True:
        switch_light('go-');
        await asyncio.sleep(2.0, loop=loop);
async def questions(loop):
    while True:
        switch_light('-o-');
        await asyncio.sleep(2.0, loop=loop);
async def questionswarning(loop):
    while True:
        switch_light('---');
        await asyncio.sleep(1.0, loop=loop);
        switch_light('-o-');
        await asyncio.sleep(1.0, loop=loop);
async def stop(loop):
    while True:
        switch_light('--r');
        await asyncio.sleep(2.0, loop=loop);
def clear():
    switch_light('---');


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

