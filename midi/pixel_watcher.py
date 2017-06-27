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

    def add_effect(self, pixel_num, effect):
        """set the pixels effect to the given instantiated effect class"""
        self._pixels[pixel_num].set_effect(effect())

    def _run_effect(self, pixel_num):
        result = self._pixels[pixel_num].run_effect()
        if result:
            # set the color after the effect function has modified the color
            # values
            self._pixels[pixel_num].set_color(result)
            self._strip.setPixelColorRGB(pixel_num, result[0],
                                                    result[1],
                                                    result[2])
        else:
            # effect has signaled that it is done by returning None
            self._remove_pixel(pixel_num)

    def _run_all_effects(self):
        """continuously run the effects for each currently watched pixel"""
        while self._active:
            for pixel_num in self._pixels:
                self._run_effect(pixel_num)
            # better to just call one show() after all effects have been run
            self._strip.show()
            # this sleep controls how fast all of the effects are done, just
            # need to hand calibrate it with the effect functions for now.
            sleep(0.05)
