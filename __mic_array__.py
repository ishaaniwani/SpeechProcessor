from pydub import AudioSegment
import math
from __microphone__ import Microphone


class MicrophoneArray(object):

    CHUNK_MILLES = 50
    DEFAULT_WEIGHT = 15
    AMP_THRES = 0.1

    def __init__(self, mic_arr=[]):
        self.microphoneArray = mic_arr
        self.sounds = []
        for mic in self.microphoneArray: 
            self.sounds.append(mic.signal)

    def add(self, mic):
        self.microphoneArray.append(mic)

    def getMaxDBFS(self):
        max = 0
        for i in range(len(self.microphoneArray)):
            if self.microphoneArray[i].getNormalizedDBFS() > self.microphoneArray[max].getNormalizedDBFS():
                max = i
        return max

    ''' 
    Splits the wav file into 250 millesecond chunks, finds the absolute value of max DB in that chunk,
    and then divides by the number of chunks, resulting in the normalized mean amplitude of the wav file 
    audio - the AudioSegment object to be processed for the aforementioned 
    '''
    def getNormalizedMeanAmplitude(self, audio):
        sounds = list(audio[::self.CHUNK_MILLES])
        normalizedMeans = []
        for i in range(len(sounds)):
            normalizedMeans.append(abs(sounds[i].dBFS))
        if(len(normalizedMeans) == 0):
            return 0
        return sum(normalizedMeans)/len(normalizedMeans)
    
    '''
    Returns the index of the AudioSegment object that has the greatest normalizedMeanAmplitude 
    '''
    def getMaxNormalizedAmplitude(self, audios): 
        max = 0
        for i in range(len(audios)): 
            if self.getNormalizedMeanAmplitude(audios[i]) > self.getNormalizedMeanAmplitude(audios[max]): 
                max = i 
        return max

    '''
    Overlays all the sound signals together. Also uses the weighting function to reduce dB response from other wav files. 
    max - the index of the AudioSegment object with the greatest normalized mean amplitude. Does not negatively affect weighting 
    of this one. 
    '''
    def overlaySounds(self, max, audio): 
        combinedSignals = audio[max] 
        i = 0
        while i < len(audio): 
            if i is not max: 
                sound = audio[i]
                sound = sound - self.weightedFunction(max , i)
                combinedSignals = combinedSignals.overlay(sound)
            i = i + 1
        return combinedSignals

    '''
    Calculates the dB response to remove from the specified sound signel. This is for future reference. 
    '''
    def weightedFunction(self, max, i): 
        return self.DEFAULT_WEIGHT

    '''
    '''
    def testOverlaySignals(self): 
        slicedSounds = []
        combinedSignals = AudioSegment.from_wav('wavfiles/silence.wav')
        for sound in self.sounds: 
            slicedSound = sound[::self.CHUNK_MILLES]
            slicedSound = list(slicedSound)
            slicedSounds.append(slicedSound)

        rangeSlicedSounds = slicedSounds[0]

        for M in range(len(rangeSlicedSounds)): 
            slicedM = []
            slicedM = list(slicedM)  
            for slicedSound in slicedSounds:
                slicedSound = list(slicedSound) 
                slicedM.append(slicedSound[M])
            max = self.getMaxNormalizedAmplitude(slicedM)
            sound = self.overlaySounds(max, slicedM)
            combinedSignals = combinedSignals + sound
        return combinedSignals

    def getEstimatedAngle(self, max):
        return self.microphoneArray[max].angle

    def distance(self, mic1, mic2):
        return math.sqrt((mic2.x - mic1.x)**2 + (mic2.y - mic2.x)**2)

    def overallAngleEstimation(self):
        DOAs = []
        slicedSounds = [] 
        for i in range(len(self.microphoneArray)): 
            slicedSounds.append(self.microphoneArray[i].signal[::Microphone.CHUNK_MILLES])
        for i in range(len(slicedSounds)): 
            iDBFS = []
            for slicedSound in slicedSounds: 
                iDBFS.append(slicedSound[i])
            max = 0 
            for i in range(len(iDBFS)): 
                if iDBFS[i].dBFS > iDBFS[max].dBFS: 
                    max = i 
            self.quickSort(self.microphoneArray, 0 , len(self.microphoneArray) - 1, max)
            DOAs.append((1.0 * self.getEstimatedAngle(0) + 0.8 * self.getEstimatedAngle(1) + 0.6 * self.getEstimatedAngle(2)) / 3)
        return DOAs

    def partition(self, arr, low, high, maxIdx):
        i = (low-1)         # index of smaller element
        pivot = self.distance(arr[maxIdx] , arr[high])  # pivot

        for j in range(low, high):

            # If current element is smaller than or
            # equal to pivot
            if self.distance(arr[maxIdx] , arr[j]) <= pivot:

                # increment index of smaller element
                i = i+1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i+1], arr[high] = arr[high], arr[i+1]
        return (i+1)

    def quickSort(self,arr,low,high,maxIdx): 
        if low < high: 
  
            # pi is partitioning index, arr[p] is now 
            # at right place 
            pi = self.partition(arr,low,high, maxIdx) 
  
            # Separately sort elements before 
            # partition and after partition 
            self.quickSort(arr, low, pi-1 , maxIdx) 
            self.quickSort(arr, pi+1, high , maxIdx) 

    