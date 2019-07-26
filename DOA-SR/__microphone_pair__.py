from __microphone__ import Microphone 
import math
import numpy as np 
import speech_recognition as sr
import scipy.signal.signaltools
from xcorr import xcorr

class MicrophonePair(object):

    def calculateDelay(self, x , y):       
        a = np.asarray(x)
        b = np.asarray(y)
        lags, c = xcorr(a , b, normed=True, maxlags=(len(a) - 1) )
        timeDelay = lags[np.argmax(c)]
        return timeDelay
    
    def distance(self, a, b): 
        x1 = a.getX()
        y1 = a.getY()
        x2 = b.getX()
        y2 = b.getY()
        return math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )

    def __init__(self, mic1, mic2): 
        self.mic1 = mic1
        self.mic2 = mic2

        self.listMic1 = mic1.getAmplitudeList()
        self.listMic2 = mic2.getAmplitudeList()

        self.delay = self.calculateDelay(self.listMic1, self.listMic2)
        print(self.delay)
        self.doa = math.asin( (self.delay * 340) / self.distance(self.mic1 , self.mic2) )
    
    def getDOAEstimation(self): 
        return self.doa
        