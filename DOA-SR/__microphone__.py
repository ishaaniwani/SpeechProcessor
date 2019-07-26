import wave
import struct
from pydub import AudioSegment
from speech_recognition.vad import VoiceActivityDetector
import soundfile as sf

class Microphone(object):

    def __init__(self, x, y, fileName):
        self.x = x
        self.y = y
        self.durationSeconds = AudioSegment.from_wav(
            fileName).duration_seconds
        self.amplitudeList = []
        self.signal = AudioSegment.from_wav(fileName)

        waveFile = wave.open(fileName, 'r')
        length = waveFile.getnframes()
        self.sampleWidth = waveFile.getsampwidth()
        for i in range(0, length):
            waveData = waveFile.readframes(1)
            data = struct.unpack("<h", waveData)
            self.amplitudeList.append(int(data[0]))
        
        self.sampleRate = self.durationSeconds / length

        '''
        slicedSounds = self.signal[::500]
        slicedSounds = list(slicedSounds)
        for j in range(0 , len(slicedSounds)):
            sound = slicedSounds[j]
            isSpeech = False
            data = obj.detect_speech()
            for i in range(0 , len(data)): 
                if data[i][len(data[i]) - 1] == 1: 
                    isSpeech = True
                    self.firstSpeechSound = sound
                    break 
            if isSpeech == False: 
                self.firstSpeechSound = None
            else:
                break
        '''
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getDurationSeconds(self):
        return self.durationSeconds

    def getAmplitudeList(self):
        return self.amplitudeList

    def getSampleRate(self): 
        return self.sampleRate
        
    '''
    def getFirstSpeechSound(self): 
        return self.firstSpeechSound

    def getSpeechSoundAmplitudeList(self): 
        amplitudeList = []
        self.firstSpeechSound.export('trash/trash.wav')
        waveFile = wave.open('trash/trash.wav', 'r')
        length = waveFile.getnframes()
        for i in range(0, length):
            waveData = waveFile.readframes(1)
            data = struct.unpack("<h", waveData)
            amplitudeList.append(int(data[0]))
        return amplitudeList
    '''