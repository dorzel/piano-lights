# piano-lights

### Midi
Takes input from any digital piano that supports midi-out,
in this case a Yamaha P45-B, and light up neopixels corresponding to
the keys pressed on the piano, with many other effects. The piano midi
out is connected to a raspberry pi usb input, and read from with the
`mido` library.

### Audio (WIP)
Takes in audio from a Digital Piano audio out jack and performs an FFT
on the incoming data, doing its best to reduce noise and identify keys
pressed based on the obtained frequencies and mapping them to the
frequencies of the keys on the piano.

To get the pi to take audio input, you need a small usb audio in jack.