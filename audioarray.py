from pydub import AudioSegment

class AudioArray(object):
    def __init__(self, array = []):
        self.sounds = array

    def add(self, audio):
        self.sounds.append(audio)

    def getNormalizedMeanAmplitude(self, audio):
        sounds = list(audio[::250])
        normalizedMeans = []
        for i in range(len(sounds)):
            normalizedMeans.append(abs(sounds[i].dBFS))
        if(len(normalizedMeans) == 0):
            return 0
        return sum(normalizedMeans)/len(normalizedMeans)
    
    def getMaxNormalizedAmplitude(self): 
        max = 0
        for i in range(len(self.sounds)): 
            if self.getNormalizedMeanAmplitude(self.sounds[i]) > self.getNormalizedMeanAmplitude(self.sounds[max]): 
                max = i 
        return max

    def overlaySounds(self, max): 
        combinedSignals = self.sounds[max] 
        i = 0
        while i < len(self.sounds): 
            if i is not max: 
                sound = self.sounds[i]
                sound = sound - 25
                combinedSignals = combinedSignals.overlay(sound)
            i = i + 1
        return combinedSignals
        