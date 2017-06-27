from threading import Thread
from time import sleep
from pixel import Pixel


class PixelWatcher:
    def __init__(self, strip):
        self._strip = strip
        self._pixels = {}
        self._watch_thread = None
        self._active = True

    def start(self):
        # spawn a new thread to process effects
        self._watch_thread = Thread(target=self._run_all_effects)
        self._watch_thread.start()

    def stop(self):
        self._active = False
        self._watch_thread.join()

    def watch_pixel(self, pixel_num, initial_color):
        # sets a pixel to be watched. initial_color must be in [r,g,b] form.
        if pixel_num not in self._pixels:
            self._pixels[pixel_num] = Pixel(pixel_num, initial_color)
        else:
            # when pressed again, reset the color
            self._pixels[pixel_num].reset_color()

    def _remove_pixel(self, pixel_num):
        self._pixels.pop(pixel_num)

    def add_effect(self, pixel_num, effect_func):
        # effect_func must take in an [r,g,b] list and return a new list of
        # transformed rgb values. It also must return None when the effect is
        # finished, which means that it must monitor its own "doneness"
        self._pixels[pixel_num].effect_func = effect_func

    def _run_effect(self, pixel_num):
        result = self._pixels[pixel_num].effect_func(self._pixels[pixel_num].current_color)
        if result:
            # set the color after the effect function has modified the color
            # values
            self._pixels[pixel_num].current_color = result
            self._strip.setPixelColorRGB(pixel_num, result[0],
                                                    result[1],
                                                    result[2])
        else:
            # effect has signaled that it is done by returning None
            self._remove_pixel(pixel_num)

    def _run_all_effects(self):
        """continuously run the effects for each currently watched pixel"""
        while self._active:
            for pixel_num in list(self._pixels.keys()):
                self._run_effect(pixel_num)
            # better to just call one show() after all effects have been run
            self._strip.show()
            # this sleep controls how fast all of the effects are done, just
            # need to hand calibrate it with the effect functions for now.
            sleep(0.05)
