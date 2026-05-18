import board
import neopixel
from time import sleep

from apdev_led_neopixel.NeoPixelLEDPinController import NeoPixelLEDPinController

def run():

    NUM_PIXELS = 50
    BRIGHTNESS = 0.05
    PIN = board.D21

    strip = neopixel.NeoPixel(PIN, NUM_PIXELS, brightness=BRIGHTNESS, auto_write=False, pixel_order=neopixel.RGB)
    pinControllers:list[NeoPixelLEDPinController] = [None] * NUM_PIXELS
    for i in range(NUM_PIXELS):
        pinControllers[i] = NeoPixelLEDPinController(strip, i, (0, 255, 0))
        pinControllers[i].set_is_lit(False)

    while True:

        pinControllers[2].set_is_lit(False)
        pinControllers[0].set_is_lit(True)
        strip.show()
        sleep(5)

        pinControllers[0].set_is_lit(False)
        pinControllers[1].set_is_lit(True)
        strip.show()
        sleep(5)

        pinControllers[1].set_is_lit(False)
        pinControllers[2].set_is_lit(True)
        strip.show()
        sleep(5)