import pydub
import math

class Microphone(object):

    CHUNK_MILLES = 50 

    '''
    '''
    def __init__(self, x, y, fileName): 
        self.mx = x 
        self.my = y 
        self.signal = pydub.AudioSegment.from_wav(fileName)
        
    '''
    Breaks wav file into chunks and gets abs(dBFS) of each of them to get the mean
    '''
    def getNormalizedDBFS(self):
        sounds = list(self.signal[::self.CHUNK_MILLES])
        normalizedMeans = []
        for i in range(len(sounds)):
            normalizedMeans.append(abs(sounds[i].dBFS))
        if(len(normalizedMeans) == 0):
            return 0
        return sum(normalizedMeans)/len(normalizedMeans)

    @property
    def weight(self): 
        return self.weight

    @property
    def x(self): 
        return self.mx

    @property
    def y(self): 
        return self.my
    
    @property 
    def signal(self): 
        return self.signal
    
    def adjustWeighting(self, dB): 
        self.signal = self.signal - dB
    
    @property
    def angle(self): 
        a = self.x
        b = self.y 
        degrees = math.degrees(math.atan(abs(b)/abs(a)))
        if a > 0 and b > 0: 
            return degrees 
        elif a < 0 and b > 0:
            return 180 - degrees
        elif a < 0 and b < 0:
            return 180 + degrees 
        elif a > 0 and b < 0: 
            return 360 - degrees
        return degrees