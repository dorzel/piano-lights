import mido
from neopixel import Adafruit_NeoPixel, Color
from math import ceil

pixel_strip = Adafruit_NeoPixel(120, 18, 800000, False, 255)

# rgb of base color to set pixels to
base_color = (255, 20, 20)
scale_factor = 1/255
blank_color = Color(0, 0, 0)


def color_from_velocity(velocity):
    return Color(ceil(scale_factor*base_color[0]),
                 ceil(scale_factor*base_color[1]),
                 ceil(scale_factor*base_color[2]))


def set_pixel(note, velocity):
    if velocity:
        # note was pressed down
        pixel_strip.setPixelColor(note, color_from_velocity(velocity))
    else:
        pixel_strip.setPixelColor(note, blank_color)

# get midi input from piano, incoming data is a msg with attributes:
# note: note pressed, 21 being lowest, 108 being highest
# velocity: if key was pressed down, an int related to amount of force on
# press, if key was released, velocity is 0.
for msg in mido.open_input(mido.get_input_names()[0]):
    if msg.type != 'clock':
        set_pixel(msg.note, msg.velocity)
