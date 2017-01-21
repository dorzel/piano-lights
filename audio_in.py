# NOTICE: run `portaudio -D` before running this

from math import log, sqrt
from statistics import mean, stdev
from time import sleep

import pyaudio

from .config import (FREQUENCY_SPACING, DATA_FORMAT_FUNC, RFFT_FUNC,
                     SAMPLE_CHUNK, DATA_IN_FORMAT, AUDIO_SAMPLE_RATE,
                     AUDIO_CHANNELS, DATA_PROCESS_FORMAT)

magnitude = lambda x: sqrt(x.real ** 2 + x.imag ** 2)
freq_to_key = lambda freq: 12 * log(freq / 440, 2) + 49
index_to_freq = lambda index: index * FREQUENCY_SPACING
sort_select = lambda x: x[1]


def callback(in_data, frame_count, time_info, flags):
    data = DATA_FORMAT_FUNC(in_data, dtype=DATA_PROCESS_FORMAT)
    fft = RFFT_FUNC(data)
    mags = list(map(magnitude, fft))
    total_mean = mean(mags)
    stdev_limit = 10 * stdev(mags)
    sort = sorted(
        ((index_to_freq(mag[0]), mag[1]) for mag in enumerate(mags) if
         mag[1] > total_mean + stdev_limit), key=sort_select, reverse=True)
    print(sort[1:5])

    return in_data, pyaudio.paContinue

p = pyaudio.PyAudio()
stream = p.open(format=DATA_IN_FORMAT,
                channels=AUDIO_CHANNELS,
                rate=AUDIO_SAMPLE_RATE,
                input=True,
                stream_callback=callback,
                frames_per_buffer=SAMPLE_CHUNK)

stream.start_stream()
while stream.is_active():
    try:
        sleep(0.05)
    except KeyboardInterrupt:
        print('closing on key interrupt')
        break

stream.stop_stream()
stream.close()
p.terminate()
