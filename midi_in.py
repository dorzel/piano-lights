import mido
from neopixel import *
from math import ceil
from threading import Thread
from time import sleep

pixel_strip = Adafruit_NeoPixel(120, 18, 800000)
pixel_strip.begin()

# scale_factor is related to the max key velocity, 100.
# base_color is the base pixel color to be scaled with velocity later
scale_factor = 1/100
base_color = (255, 20, 20)
blank_color = Color(0, 0, 0)


class PixelWatcher:
    def __init__(self, strip):
        self._strip = strip
        self._pixels = {}
        self._watch_thread = None
        self.active = True

    def start(self):
        # spawn a new thread to process effects
        print('starting watch thread...')
        self._watch_thread = Thread(target=self.run_all_effects)
        print('watch thread: {}'.format(self._watch_thread))
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

    def add_effect(pixel_num, effect_func):
        # effect_func must take in an [r,g,b] list and perform operations in place
        # on those values. It also must return None when the effect is finished,
        # which means that it must monitor its own "doneness"
        self._pixels[pixel_num]['effect_func'] = effect_func

    def _run_effect(pixel_num):
        result = self._pixels[pixel_num]['effect_func'](self._pixels['current_color'])
        if result:
            # set the color after the effect function has modified the color values
            self._strip.setPixelColorRGB(pixel_num, self._pixels['current_color'][0],
                                                    self._pixels['current_color'][1],
                                                    self._pixels['current_color'][2])
        else:
            # effect has signaled that it is done
            self._remove_pixel(pixel_num)

    def run_all_effects(self):
        print('in run effects')
        while self.active:
            print('in run effect while loop')
            for pixel in self._pixels.keys():
                self._run_effect(pixel)
            # better to just call one show() after all effects have been run
            self._strip.show()
            sleep(0.1)

watcher = PixelWatcher(pixel_strip)


def set_blank():
    for i in range(pixel_strip.numPixels()):
        pixel_strip.setPixelColorRGB(i, 0, 0, 0)
    pixel_strip.show()

def color_from_velocity(velocity):
    return  [ceil(scale_factor*velocity*base_color[0]),
             ceil(scale_factor*velocity*base_color[1]),
             ceil(scale_factor*velocity*base_color[2])]

def set_pixel(note, velocity):
    if velocity:
        # note was pressed down
        try:
            print('put watch on pixel {}'.format(note))
            watcher.watch_pixel(note, color_from_velocity(velocity))
        except Exception as e:
            print(e)


# get midi input from piano, incoming data is a msg with attributes:
# note: note pressed, 21 being lowest, 108 being highest
# velocity: if key was pressed down, an int related to amount of force on
# press, if key was released, velocity is 0.
set_blank()
watcher.start()
try:
    for msg in mido.open_input(mido.get_input_names()[0]):
        print('in midi loop')
        if msg.type != 'clock':
            if msg.type != 'control_change':
                set_pixel(msg.note, msg.velocity)
            else:
                # floor pedal was pressed
                pass    
except KeyboardInterrupt:
    set_blank()
    watcher.stop()
    print('done.')
