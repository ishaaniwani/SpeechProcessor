import math
from pydub import AudioSegment
from __microphone__ import Microphone
from scipy.io import wavfile
import numpy as np
import wave 
import struct


class MicrophonePair(object):

    AMPLITUDE_THRESHOLD = 0.1
    CORR_THRESHOLD = 5
    DIFFERENCE_THRESHOLD = 10

    def __init__(self, mic1, mic2):
        self.mic1 = mic1
        self.mic2 = mic2

    def getAmplitudeList(self , fileName):

        amplitudeList = []

        waveFile = wave.open(fileName, 'r')
        length = waveFile.getnframes()
        for i in range(0, length):
            waveData = waveFile.readframes(i - i + 1)
            data = struct.unpack("<h", waveData)
            amplitudeList.append(int(data[0]))

        return amplitudeList

    def calculateTimeDelay(self):
        amplitudes1 = self.getAmplitudeList(self.mic1.fileName)
        amplitudes2 = self.getAmplitudeList(self.mic2.fileName)

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

    def calculatePhaseDifference(self, maxPossibleDelay): 
        xcorr = []

        x = self.getAmplitudeList(self.mic1.fileName)
        y = self.getAmplitudeList(self.mic2.fileName)
        mx = sum(x) / len(x)
        my = sum(y) / len(y)

        for d in range(0, maxPossibleDelay):
            numerator = 0
            denominator = 0 
            for i in range(0 , len(x)):
                xNumerator = x[i] - mx
                yIndex = i - d
                if yIndex < 0:
                    yIndex = len(y) - d
                yNumerator = y[i] - my

                numerator = numerator + xNumerator * yNumerator
            xDenominator = 0 
            yDenominator = 0 
            for i in range(0, len(x)): 
                xDenominator = xDenominator + (x[i] - mx)**2 
            xDenominator = math.sqrt(xDenominator)

    @property
    def mic1(self):
        return self.mic1

    @property
    def mic2(self):
        return self.mic2
