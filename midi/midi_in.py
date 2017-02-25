from __future__ import division, print_function
import mido
from neopixel import *
from threading import Thread
from time import sleep
from random import randint

# scale_factor is related to the max key velocity, 100.
scale_factor = 1/100
blank_color = Color(0, 0, 0)


class Pixel:
    def __init__(self):
        pass


class Effect:
    def __init__(self):
        pass


class PixelWatcher:
    def __init__(self, strip):
        self._strip = strip
        self._pixels = {}
        self._watch_thread = None
        self.active = True

    def start(self):
        # spawn a new thread to process effects
        self._watch_thread = Thread(target=self.run_all_effects)
        self._watch_thread.start()

    def stop(self):
        self.active = False
        self._watch_thread.join()

    def watch_pixel(self, pixel_num, initial_color):
        # sets a pixel to be watched. initial_color must be in [r,g,b] form.
        if not pixel_num in self._pixels:
            self._pixels[pixel_num] = {'current_color': initial_color}
        else:
            # when pressed again, reset the color
            self._pixels[pixel_num]['current_color'] = initial_color

    def _remove_pixel(self, pixel_num):
        self._pixels.pop(pixel_num)

    def add_effect(self, pixel_num, effect_func):
        # effect_func must take in an [r,g,b] list and return a new list of
        # transformed rgb values. It also must return None when the effect is
        # finished, which means that it must monitor its own "doneness"
        self._pixels[pixel_num]['effect_func'] = effect_func

    def _run_effect(self, pixel_num):
        result = self._pixels[pixel_num]['effect_func'](self._pixels[pixel_num]['current_color'])
        if result:
            # set the color after the effect function has modified the color
            # values
            self._pixels[pixel_num]['current_color'] = result
            self._strip.setPixelColorRGB(pixel_num, result[0],
                                                    result[1],
                                                    result[2])
        else:
            # effect has signaled that it is done by returning None
            self._remove_pixel(pixel_num)

    def run_all_effects(self):
        while self.active:
            for pixel_num in list(self._pixels.keys()):
                self._run_effect(pixel_num)
            # better to just call one show() after all effects have been run
            self._strip.show()
            # this sleep controls how fast all of the effects are done, just
            # need to hand calibrate it with the effect functions for now.
            sleep(0.05)


def set_blank():
    for i in range(pixel_strip.numPixels()):
        pixel_strip.setPixelColorRGB(i, 0, 0, 0)
    pixel_strip.show()


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


def set_pixel(note, velocity):
    if velocity:
        # key was pressed down
        try:
            watcher.watch_pixel(note, random_color_from_velocity(velocity))
            watcher.add_effect(note, reduce_effect)
        except Exception as e:
            print(e)
    else:
        # key has been released
        pass

pixel_strip = Adafruit_NeoPixel(120, 18, 800000)
pixel_strip.begin()
watcher = PixelWatcher(pixel_strip)
# get midi input from piano, incoming data is a msg with attributes:
# note: note pressed, 21 being lowest, 108 being highest
# velocity: if key was pressed down, an int related to amount of force on
# press, if key was released, velocity is 0.
set_blank()
watcher.start()
try:
    input_device = [name for name in mido.get_input_names() if 'Digital' in name][0]
    if input_device:
        for msg in mido.open_input(input_device):
            if msg.type != 'clock':
                if msg.type != 'control_change':
                    set_pixel(msg.note, msg.velocity)
                else:
                    # floor pedal was pressed
                    pass
    else:
        raise Exception("Piano was not found, did you turn the piano on before"
                        " running this? Devices found: {}"
                        .format(mido.get_input_names()))
except KeyboardInterrupt:
    print('done.')
except Exception as e:
    print(e)
finally:
    watcher.stop()
    set_blank()
