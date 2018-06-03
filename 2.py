import numpy, wave, scipy.io.wavfile, math, wavefile, sys
from matplotlib import pyplot, mlab, ticker
from collections import defaultdict

main_filename = "b1.wav"

SAMPLE_RATE = 44100
WINDOW_SIZE = 2048
WINDOW_STEP = 512 

#################################################################################

types = {
    1: numpy.int8,
    2: numpy.int16,
    4: numpy.int32
}

wav = wave.open(main_filename, mode="r")
(nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()

duration = nframes / framerate
w, h = 800, 300
k = nframes/w/32
DPI = 72
peak = 256 ** sampwidth / 2

content = wav.readframes(nframes)
samples = numpy.fromstring(content, dtype=types[sampwidth])

pyplot.figure(1, figsize=(float(w)/DPI, float(h)/DPI), dpi=DPI)
pyplot.subplots_adjust(wspace=0, hspace=0)

def format_time(x, pos=None):
    global duration, nframes, k
    progress = int(x / float(nframes) * duration * k)
    mins, secs = divmod(progress, 60)
    hours, mins = divmod(mins, 60)
    out = "%d:%02d" % (mins, secs)
    if hours > 0:
        out = "%d:" % hours
    return out

def format_db(x, pos=None):
    if pos == 0:
        return ""
    global peak
    if x == 0:
        return "-inf"
    db = 20 * math.log10(abs(x) / float(peak))
    return int(db)

#################################################################################

def get_wave_data(filename):
    sample_rate, wave_data = scipy.io.wavfile.read(filename)
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
    fig.savefig("test.png")
    print("[+] specgram showing -- done!")

def getWaveDuration(filename):
    w = wave.open(filename, 'r')
    time = (1.0 * w.getnframes ()) / w.getframerate ()
    return time

def getPerFrame(filename, time):
    w = wave.open(filename, 'r')
    res = float(time)/float(w.getnframes())
    res = format(res, '.8f')
    return res

def omniCut(filename):
    start = 0
    end = 0
    for n in range(nchannels):
        channel = samples[n::nchannels]
        channel = channel[0::k]
        if nchannels == 1:
            channel = channel - peak
        framesCount = len(channel)
        for i in range(0, framesCount):
            if channel[i] > 200:
                start = i
                break
        i = framesCount - 1
        while i > 0:
            if channel[i] > 200:
                end = i
                break
            i -=1
    start = (float(start) / float(SAMPLE_RATE)) - 0.085
    end = (float(end) / float(SAMPLE_RATE)) + 0.085
    res = []
    res.append(start)
    res.append(end)
    return res

def analyzeMute(filename):
    w = wave.open(filename, 'r')
    da = numpy.fromstring(w.readframes(44100), dtype=numpy.int16)
    print(str(len(da)) + " is len, one value: " + str(da[30000]))
    rate, data = scipy.io.wavfile.read(filename)
    t = numpy.arange(len(data[:,0]))*1.0/rate
    print(t[1])
    for i in range(w.getnframes()):
        frame = w.readframes(1)
        all_zero = True
        for j in range(len(frame)):
            if ord(frame[j]) > 0:
                #print('found >0 at ' + str(j))
                all_zero = False
                break
        if all_zero:
            pass
            '''print 'silence found at frame %s' % w.tell()
            print 'silence found at second %s' % (w.tell()/w.getframerate())'''
    print("[+] mute analyzing -- done!")

def cutWav(filename, start, end):
    new_name = 'new_' + filename
    win= wave.open(filename, 'rb')
    wout= wave.open(new_name, 'wb')
    t0, t1= start, end # interval
    s0, s1= int(t0*win.getframerate()), int(t1*win.getframerate())
    win.readframes(s0) # discard
    frames= win.readframes(s1-s0)
    wout.setparams(win.getparams())
    wout.writeframes(frames)
    win.close()
    wout.close()
    print("[+] audiofile cutting -- done!")

def getAmplitudeGram(filename):
    for n in range(nchannels):
        channel = samples[n::nchannels]
        channel = channel[0::k]
        if nchannels == 1:
            channel = channel - peak
        axes = pyplot.subplot(2, 1, n+1, axisbg="k")
        for i in range(0, len(channel)):
            if channel[i] > 100:
                pass
                #print(i)
                #print("Channel vertical line: " + str(i))
        axes.plot(channel, "g")
        #print(channel[10000])
        axes.yaxis.set_major_formatter(ticker.FuncFormatter(format_db))
        pyplot.grid(True, color="w")
        axes.xaxis.set_major_formatter(ticker.NullFormatter())

    axes.xaxis.set_major_formatter(ticker.FuncFormatter(format_time))
    pyplot.savefig("wave", dpi=DPI)
    pyplot.show()

def getMinMaxAmpl(filename):
    w = wavefile.load(filename)
    signal = w[1][0]
    frames = str(len(signal))+" frames"
    minAmpl = str(min(abs(signal))*100)
    maxAmpl = str(max(abs(signal))*100)
    res = []
    res.append(minAmpl)
    res.append(maxAmpl)
    return res

def Main():
    print("Min&Max Amplitude: " + str(getMinMaxAmpl(main_filename)))
    print("Per frame: " + getPerFrame(main_filename, getWaveDuration(main_filename)))
    cutting = omniCut('b1.wav')
    cutWav(main_filename, cutting[0], cutting[1])
    getAmplitudeGram('new_' + main_filename)
    analyzeMute(main_filename)
    getWaveDuration(main_filename)
    show_specgram(get_wave_data('new_' + main_filename))


Main()