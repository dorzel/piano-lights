# piano-lights

### Midi-based (Basic functionality done)
Takes input from any digital piano that supports midi-out,
in this case a Yamaha P45-B, and light up neopixels corresponding to
the keys pressed on the piano, with many other effects. The piano midi
out is connected to a raspberry pi usb mic input and read from with the
`mido` library.

### Audio-based (WIP)
Takes in audio from a Digital Piano audio out jack and performs an FFT
on the incoming data, doing its best to reduce noise and identify keys
pressed based on the obtained frequencies and mapping them to the
frequencies of the keys on the piano.

#### Audio Input
To get the pi to take analog audio input, you'll need a small usb audio
in jack. Anything similar to
[this](https://www.amazon.com/Plugable-Headphone-Microphone-Aluminum-Compatibility/dp/B00NMXY2MO)
should work.

#### Midi input
To get midi input into the pi, you'll just need to plug the usb side
of the cable into any of the pi's usb ports, and the other end into your
piano's midi out port.

#### Executing the code
To run piano-lights, simply:

`cd piano-lights`

`python midi/midi_in.py` or `python audio/audio_in.py`

To exit:

`ctrl+c`
