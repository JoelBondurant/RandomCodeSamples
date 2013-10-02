import math
import wave
import struct



def synthComplex(toneNum, wavFile):
    coef = [1]
    freq = [100 * math.exp(toneNum / (2 * math.pi))]
    datasize = 5000
    frate = 44100.00  
    amp = 8000.0 
    sine_list=[]
    for x in range(datasize):
        samp = 0
        for k in range(len(freq)):
            samp = samp + coef[k] * math.sin(2*math.pi*freq[k]*(x/frate))
        sine_list.append(samp)
    nchannels = 1
    sampwidth = 2
    framerate = int(frate)
    nframes=datasize
    comptype= "NONE"
    compname= "not compressed"
    for s in sine_list:
        wavFile.writeframes(struct.pack('h', int(s*amp/2)))


def arccot(x, unity):
    sum = xpower = unity // x
    n = 3
    sign = -1
    while 1:
        xpower = xpower // (x*x)
        term = xpower // n
        if not term:
            break
        sum += sign * term
        sign = -sign
        n += 2
    return sum

def pi(digits):
    unity = 10 ** (digits + 10)
    pi = 4 * (4 * arccot(5, unity) - arccot(239, unity))
    return pi // 10 ** 10


print("Starting pi tones.")
piTonesFile = wave.open("pitones.wav","w")
piTonesFile.setparams((1, 2, 44100, 10000, "NONE", "not compressed"))
numTones = 1000
piStr = str(pi(numTones))

for i in range(1, numTones):
	toneNum = int(piStr[i]) + 1
	synthComplex(toneNum, piTonesFile)

piTonesFile.close()
print("Finished pi tones.")




