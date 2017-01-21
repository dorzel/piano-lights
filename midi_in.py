import mido
from neopixel import Adafruit_NeoPixel


pixel_strip = Adafruit_NeoPixel(120, 18, 800000, False, 255)





def set_pixel(note, velocity):
	if velocity:
		# note 

	else:
		











# get midi input from piano, incoming data is a msg with attributes:
# note: note pressed, 21 being lowest, 108 being highest
# velocity: if key was pressed down, an int related to amount of force on press,
# if key was released, velocity is 0.
for msg in mido.open_input(mido.get_input_names()[0]):
	if msg.type != 'clock':
		set_pixel(msg.note, msg.velocity)


# notes go from 21 to 108
