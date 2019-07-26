import xcorr
import numpy as np 
from __microphone__ import Microphone

mic1 = Microphone(0,0, 'WavFileDatabase/Data2/mic1.wav')
mic2 = Microphone(0,0,'WavFileDatabase/Data2/mic2.wav')

test1 = mic1.getAmplitudeList()
test2 = mic2.getAmplitudeList()

test1 = test1[0:50]
test2 = test2[0:50]

a = np.asarray(test1)
b = np.asarray(test2)

lags, c = xcorr.xcorr(test2, test1 ,normed=True, maxlags=49 )
print lags
print c
