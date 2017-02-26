from __future__ import division, print_function

from random import randint

import mido
from neopixel import *

from .pixel_watcher import PixelWatcher

# scale_factor is related to the max key velocity, 100.
scale_factor = 1/100
blank_color = Color(0, 0, 0)


def set_blank(strip):
    """set the strip to all black, clearing all colors"""
    for i in range(strip.numPixels()):
        strip.setPixelColorRGB(i, 0, 0, 0)
    strip.show()


def random_color_from_velocity(velocity):
    return [int(scale_factor*velocity*randint(0, 255)),
            int(scale_factor*velocity*randint(0, 255)),
            int(scale_factor*velocity*randint(0, 255))]


def reduce_effect(rgb_in):
    if not all(comp == 0 for comp in rgb_in):
        return [comp - 6 if comp > 0 and comp - 6 > 0 else 0 for comp in rgb_in]
    else:
        # all components are 0, ending the effect
        return None


def set_pixel(note, velocity, watcher, effect):
    if velocity:
        # key was pressed down
        try:
            watcher.watch_pixel(note, random_color_from_velocity(velocity))
            watcher.add_effect(note, effect)
        except Exception as e:
            print(e)
    else:
        # key has been released
        pass


pixel_strip = Adafruit_NeoPixel(120, 18, 800000)
pixel_strip.begin()
pixel_watcher = PixelWatcher(pixel_strip)
pixel_watcher.start()
set_blank(pixel_strip)
# get midi input from piano, incoming data is a msg with attributes:
# note: note pressed, 21 being lowest, 108 being highest
# velocity: if key was pressed down, an int related to amount of force on
# press, if key was released, velocity is 0.
try:
    input_device = [name for name in mido.get_input_names() if 'Digital' in name]
    if input_device:
        for msg in mido.open_input(input_device[0]):
            if msg.type != 'clock':
                if msg.type != 'control_change':
                    set_pixel(msg.note, msg.velocity, pixel_watcher,
                              reduce_effect)
                else:
                    # floor pedal was pressed
                    pass
    else:
        raise Exception("Piano was not found, did you turn the piano on before"
                        " running this? Devices found: {}"
                        .format(mido.get_input_names()))
except KeyboardInterrupt:
    print('done')
except Exception as e:
    print(e)
finally:
    pixel_watcher.stop()
    set_blank(pixel_strip)
