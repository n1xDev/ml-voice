import numpy
from matplotlib import pyplot, mlab
import scipy.io.wavfile
from collections import defaultdict

SAMPLE_RATE = 44100
WINDOW_SIZE = 2048
WINDOW_STEP = 512 

def get_wave_data(wave_filename):
    sample_rate, wave_data = scipy.io.wavfile.read(wave_filename)
    assert sample_rate == SAMPLE_RATE, sample_rate
    if isinstance(wave_data[0], numpy.ndarray):
        wave_data = wave_data.mean(1)
    return wave_data

def show_specgram(wave_data):
    fig = pyplot.figure()
    ax = fig.add_axes((0.1, 0.1, 0.8, 0.8))
    ax.specgram(wave_data,
        NFFT=WINDOW_SIZE, noverlap=WINDOW_SIZE - WINDOW_STEP, Fs=SAMPLE_RATE)
    pyplot.show()

wave_data = get_wave_data('b1.wav')
show_specgram(wave_data)