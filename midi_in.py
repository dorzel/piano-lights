import mido
from neopixel import *
from math import ceil

pixel_strip = Adafruit_NeoPixel(120, 18, 800000)
pixel_strip.begin()

# scale_factor is related to the max key velocity, 100.
# base_color is the base pixel color to be scaled with velocity later
scale_factor = 1/100
base_color = (255, 20, 20)
blank_color = Color(0, 0, 0)


def set_blank():
    for i in range(pixel_strip.numPixels()):
        pixel_strip.setPixelColorRGB(i, 0, 0, 0)
    pixel_strip.show()

def color_from_velocity(velocity):
    return  Color(ceil(scale_factor*velocity*base_color[0]),
                 ceil(scale_factor*velocity*base_color[1]),
                 ceil(scale_factor*velocity*base_color[2]))

def set_pixel(note, velocity):
    if velocity:
        # note was pressed down
        try:
            pixel_strip.setPixelColor(note, color_from_velocity(velocity))
            pixel_strip.show()
        except Exception as e:
            print(e)
    else:
        pixel_strip.setPixelColorRGB(note, 0, 0, 0)
        pixel_strip.show()


# get midi input from piano, incoming data is a msg with attributes:
# note: note pressed, 21 being lowest, 108 being highest
# velocity: if key was pressed down, an int related to amount of force on
# press, if key was released, velocity is 0.
set_blank()
while True:
    try:
        for msg in mido.open_input(mido.get_input_names()[0]):
            if msg.type != 'clock':
                set_pixel(msg.note, msg.velocity)
    except KeyboardInterrupt:
        print('done.')
        break
