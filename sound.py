import numpy as np 
from pydub import AudioSegment
from scipy.io.wavfile import read

'''
This is a wrapper class for the AudioSegment class in the pydub library. The purpose of this class was to make it 
easier to use the wav files for processing. 
'''


class Sound(object):
    '''
    Contructs an AudioSegment Object using an existing WAV File.
    fileName - Path to the existing WAV file.  
    '''
    def __init__(self, filename):
        self.fileName = filename
        self.wav = AudioSegment.from_wav(self.fileName)

    '''
    Adjusts volume of WAV file. Note: Method does not change wav volume to dbGain, but adds dbGain to existing WAV file. 
    dbGain - The addition or subtraction of volume, in terms of dB, on the file. 
    '''

    def adjustVolume(self, dBGain):
        self.wav = self.wav + dBGain

    '''
    Cuts the WAV file such that it only contains the first (milliseconds) of the wav file. 
    milleseconds - how big (in milleseconds) the WAV file will be 
    '''

    def sliceBeginningPortion(self, milleseconds):
        self.wav = self.wav[:milleseconds]

    '''
    Cuts the WAV file such that is only contains the last (milleseconds) of the wav file. 
    milleseconds - how big (in milleseconds) the WAV file will be 
    '''

    def sliceEndPortion(self, milleseconds):
        self.wav = self.wav[-milleseconds]

    '''
    Returns a copy of the encapsulated wav file. This method is intended for when the user wants to export 
    the sound to a wav file. 
    '''

    def getWav(self):
        return self.wav

    '''
    Returns the duration, in seconds, of the encapsulated wav file
    '''

    def getDuration(self):
        return self.wav.duration_seconds

    '''
    Return the dbFS of the wav file. 
    '''

    def getdBFS(self):
        return self.wav.dBFS

    '''
    Finds the normalized mean amplitude of the system. 
    '''

    def getNormalizedMeanAmplitude(self):
        sampleRate, wavData = read(self.fileName)
        matrix = wavData.tolist()
        normalizedMeans = []
        for array in matrix:
            mean = 0;  
            for element in array: 
                mean = mean + abs(element)
            normalizedMeans.append(mean)
        result = 0
        for mean in normalizedMeans: 
            result = result + mean
        result = result / len(normalizedMeans)
        return result