import pyaudio
import numpy as np

# various constants

AUDIO_CHANNELS = 1
AUDIO_SAMPLE_RATE = 44100
SAMPLE_CHUNK = 2048
DATA_FORMAT = pyaudio.paInt16
FREQUENCY_SPACING = AUDIO_SAMPLE_RATE/int(SAMPLE_CHUNK / 2)
RFFT_FUNC = np.fft.rfft
DATA_FORMAT_FUNC = np.fromstring
