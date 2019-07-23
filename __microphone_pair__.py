import math
from pydub import AudioSegment
from __microphone__ import Microphone
from scipy.io import wavfile
import numpy as np
import wave 
import struct
import numpy as np


class MicrophonePair(object):

    AMPLITUDE_THRESHOLD = 0.1
    CORR_THRESHOLD = 5
    DIFFERENCE_THRESHOLD = 10

    def __init__(self, mic1, mic2):
        self.mic1 = mic1
        self.mic2 = mic2

    def calculateTimeDelay(self):
        amplitudes1 = self.mic1.getAmplitudeList()
        amplitudes2 = self.mic2.getAmplitudeList()

        duration_seconds = AudioSegment.from_wav(self.mic1.fileName).duration_seconds
        numFrames = len(amplitudes1)
        sampleRate = duration_seconds / numFrames

        for i in range(0, numFrames):
            if amplitudes1[i] > 200 or amplitudes1[i] < -200:
                frame1 = i
                break

        for i in range(0, numFrames):
            if (amplitudes2[i] - amplitudes2[frame1]) < self.DIFFERENCE_THRESHOLD:
                frame2 = i
                break

        frameDiff = frame1 - frame2
        timeDelay = sampleRate * frameDiff
        return timeDelay

    def doaEstimation(self):
        delay = self.calculateTimeDelay()
        c = 340
        distance = 3.4
        Theta = math.sin((delay * c) / distance)
        Theta = math.degrees(Theta)
        return Theta

    def calculatePhaseDifference(self):
        a = np.asarray(self.mic1.getAmplitudeList())
        b = np.asarray(self.mic2.getAmplitudeList())
        xcorr = np.correlate(a , b)
        delay = np.argmax(xcorr)
        return delay

    '''
    def calculatePhaseDifference(self, maxPossibleDelay): 
        xcorr = []

        x = self.getAmplitudeList(self.mic1.fileName)
        y = self.getAmplitudeList(self.mic2.fileName)
        mx = sum(x) / len(x)
        my = sum(y) / len(y)

        if maxPossibleDelay > len(y) or maxPossibleDelay > len(x): 
            if len(y) > len(x): 
                maxPossibleDelay = len(x)
            else: 
                maxPossibleDelay = len(y)

        for d in range(-maxPossibleDelay , maxPossibleDelay): 
            numerator = 0 
            denominator = 0 
            for i in range(0 , len(x)): 
                xNumerator = x[i] - mx
                yIndex = i + d 
                if yIndex < 0: 
                    yIndex = abs(i + d) % maxPossibleDelay
                yNumerator = y[yIndex] - my 

                numerator = numerator + xNumerator * yNumerator 
            xDenominator = 0 
            yDenominator = 0
            for i in range(0 , len(x)): 
                xDenominator = xDenominator + (x[i] - mx)**2 
            xDenominator = math.sqrt(xDenominator)
            for i in range(0 , len(y)): 
                yIndex = i + d
                if yIndex < 0: 
                    yIndex = (len(y) - 1) - (abs(d) % len(y))
                yDenominator = yDenominator + (y[yIndex] - my)**2
            denominator = denominator + xDenominator + yDenominator
            corr = numerator / denominator 
            xcorr.append(corr) 
        return xcorr
    '''