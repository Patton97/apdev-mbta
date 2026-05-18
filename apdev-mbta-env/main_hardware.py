import board
import neopixel
from time import sleep
import asyncio
import threading

from apdev_led_neopixel.NeoPixelLEDPinController import NeoPixelLEDPinController

from apdev_led_neopixel.NeoPixelLEDPin import NeoPixelLEDPin

NUM_PIXELS = 50
BRIGHTNESS = 0.05
GPIO_DATA_PIN = board.D21

strip:neopixel.NeoPixel = neopixel.NeoPixel(GPIO_DATA_PIN, NUM_PIXELS, brightness=BRIGHTNESS, auto_write=False, pixel_order=neopixel.RGB)
pins:list[NeoPixelLEDPin] = [None] * NUM_PIXELS
pinControllers:list[NeoPixelLEDPinController] = [None] * NUM_PIXELS

async def __apiLoop():
    while True:
        NUM_FLASHING_PINS = 3
        for i in range(NUM_FLASHING_PINS):
            for pinController in pinControllers:
                pinController.set_is_lit(False)
            pinControllers[i].set_is_lit(True)
            await asyncio.sleep(5)

def __startApiLoop():
    asyncio.run(__apiLoop())

def run():
    for i in range(NUM_PIXELS):
        pins[i] = NeoPixelLEDPin(strip, i)
        pins[i].setOnColour((0, 255, 0))

        pinControllers[i] = NeoPixelLEDPinController(pins[i])
        pinControllers[i].set_is_lit(False)

    threading.Thread(target=__startApiLoop, daemon=True).start()

    while True:
        for pin in pins:
            if pin.getIsFlashing():
                pin._isLit = not pin._isLit
            else:
                pin._isLit = False
            pin.renderTick()
        strip.show()
        sleep(0.5)