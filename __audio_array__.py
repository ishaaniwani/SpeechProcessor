from pydub import AudioSegment
from scipy.signal import correlate
import numpy as np 

class AudioArray(object):

    CHUNK_MILLES = 50
    DEFAULT_WEIGHT = 15
    AMP_THRES = 0.1

    '''
    Constructs an array of AudioSegment objects. If not array is passed in, then there will be a blank array 
    array - array of AudioSegment objects to define the wrapper array
    '''
    def __init__(self, array = []):
        self.sounds = array

    '''
    Appends an Audiosegment Object to the array 
    audio - the AudioSegment object 
    '''
    def add(self, audio):
        self.sounds.append(audio)

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

    '''
    Calculates the phase time difference between two sound files by comparing 
    where the same chunk of data are, and getting the difference between the times. 
    sound1 - the first wav file 
    sound2 - the second wav file, will analyze this one to see if it is in sound1 
    Note: This is a work in progress. 
    '''
    def calculatePhaseDifference(self, sound1, sound2): 
        slicedSound1 = sound1[::self.CHUNK_MILLES]
        slicedSound2 = sound2[::self.CHUNK_MILLES]
        
        slicedSound1 = list(slicedSound1)
        slicedSound2 = list(slicedSound2)
        
        time1 = 0 
        time2 = 0 

        for i in range(len(slicedSound1)): 
            if slicedSound1[i].max_possible_amplitude > self.AMP_THRES: 
                time1 = self.CHUNK_MILLES + i * self.CHUNK_MILLES
                self.chunk1 = slicedSound1[i]
                print(time1)
                break

        for i in range(len(slicedSound2)): 
            if slicedSound2[i] == self.chunk1:
                time2 = self.CHUNK_MILLES + i * self.CHUNK_MILLES 
                print(time2)
                break

        return time2 - time1