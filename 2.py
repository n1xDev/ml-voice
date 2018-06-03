import numpy, wave, scipy.io.wavfile, math, wavefile, sys, json, string
from matplotlib import pyplot, mlab, ticker
from collections import defaultdict

main_filename = "1.wav"

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
    #pyplot.show()
    print("WAVE DATA: ")
    print(wave_data[0])
    #specToJSON(wave_data)
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
        print("FramesCount(channel length): " + str(framesCount))
        print("Full Frames Count: " + str(wav.getnframes()))
        dif = round(float(wav.getnframes()) / float(framesCount))
        for i in range(0, framesCount):
            if channel[i] > 80:
                start = i
                break
        i = framesCount - 1
        while i > 0:
            if channel[i] > 80:
                end = i
                break
            i -=1
    #start = (float(start) / float(SAMPLE_RATE)) - 0.085
    #end = (float(end) / float(SAMPLE_RATE)) + 0.085
    res = []
    res.append(start)
    res.append(end)
    res.append(dif)
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
                all_zero = False
                break
        if all_zero:
            pass
            '''print 'silence found at frame %s' % w.tell()
            print 'silence found at second %s' % (w.tell()/w.getframerate())'''
    print("[+] mute analyzing -- done!")

def cutWav(filename, start, end, dif):
    new_name = 'new_' + filename
    win= wave.open(filename, 'rb')
    wout= wave.open(new_name, 'wb')
    print("New CUT WAV: " + new_name)
    print(str(start) + " -(start/end)- " + str(end))
    print("FrameRate: " + str(win.getframerate()))
    print("nFrames: " + str(win.getnframes()))
    #start, end = (start*dif) - (start/6), (end*dif) + (end/6)
    start, end = (start*dif) - 1000, (end*dif) + 1000
    print(dif)
    print("New: " + str(start) + " -(start/end)- " + str(end))
    s0, s1= int(start), int(end) #40000, 60000 # interval
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
        channel = channel[0::wav.getnframes()/800/32]
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
    #pyplot.show()

def getAmplGram(filename):
    wr = wave.open(filename, 'r')
    sz = 44100 # Read and process 1 second at a time.
    da = numpy.fromstring(wr.readframes(sz), dtype=numpy.int16)
    wr.close()
    left, right = da[0::2], da[1::2]
    print(left)
    print(right)
    print(da)
    print("AMPL DONE!")

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

def specToJSON(arr_data):
    spec_arr = []
    with open('data.json') as data_file:
        spec_arr = json.loads(data_file.read())
        i = 0
        while i < len(arr_data):
            spec_arr['spec'].append(arr_data[i])
            i += 1
    file = open("data.json","w")
    json.dump(spec_arr ,file, indent=4)

def ExpendArr(out, out_len, source, source_len):
    k = float((float(out_len) - 1.0) / float(source_len - 1.0))
    i = 1
    while i < out_len - 1:
        i1 = int(i/k)
        frac = float(float(i)/float(k) - float(i1))
        out[i] = float(float(source[i1]) * (1.0 - frac) + float(source[i1+1]) * frac)
        i += 1
    out[0] = source[0]
    out[out_len - 1] = source[source_len - 1]
    return out

def ExpendWaveData(filename):
    src = get_wave_data(filename)
    out = [None] * 5000
    out = ExpendArr(out, len(out), src, len(src))
    print(len(src))
    print(len(out))
    filename = filename[:5]
    f = open(filename + '.txt', 'w')
    #f = open(filename + '.txt', 'a')
    for i in range(0, len(out)):
        f.write(str(out[i]) + '\n')
    return out

def doGeneral():
    global main_filename
    arr = list(range(1, 44))
    for i in range(0, len(arr)):
        main_filename = str(arr[i]) + '.wav'
        print(main_filename)
        Main(str(arr[i]))

def Main(letter):
    wdata = get_wave_data(main_filename)
    print("Min&Max Amplitude: " + str(getMinMaxAmpl(main_filename)))
    print("Per frame: " + getPerFrame(main_filename, getWaveDuration(main_filename)))
    cutting = omniCut(letter + '.wav')
    cutWav(main_filename, cutting[0], cutting[1], cutting[2])
    analyzeMute(main_filename)
    getWaveDuration(main_filename)
    wdata = get_wave_data("new_" + main_filename)
    show_specgram(wdata)
    getAmplitudeGram(main_filename)
    getAmplGram("new_" + main_filename)
    ExpendWaveData("new_" + main_filename)

doGeneral()