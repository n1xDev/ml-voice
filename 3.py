import wavefile, sys

# returns the contents of the wav file as a double precision float array
def wav_to_floats(filename = 'b2.wav'):
    w = wavefile.load(filename)
    print(w[1][0])
    return w[1][0]

signal = wav_to_floats()
print "read "+str(len(signal))+" frames"
print  "in the range "+str(min(abs(signal))*100)+" to "+str(max(abs(signal))*100)