import numpy as np 
from scipy.io import wavfile
from vad import VoiceActivityDetector
from pydub import AudioSegment
from xcorr import xcorr
import math
import speech_recognition as sr 

# Returns the start of speech of a wav file. If no speech is detected, then returns -1
def getSpeechStartTime(soundFileName):
    v = VoiceActivityDetector(soundFileName)
    windows = v.detect_speech()
    for i in range(0, len(windows)):
        arr = windows[i]
        if arr[len(arr) - 1] == 1:
            return i * 10 # VAD breaks wav file into 20 millesecond chunks 
    return -1 

soundFileName1 = 'Data3/mic1.wav'
soundFileName2 = 'Data3/mic2.wav'
speechTimeStart = getSpeechStartTime(soundFileName1)

print speechTimeStart

sound1 = AudioSegment.from_wav(soundFileName1)
sound2 = AudioSegment.from_wav(soundFileName2)

sound1 = sound1[speechTimeStart - 100:speechTimeStart + 400]
sound2 = sound2[speechTimeStart - 100:speechTimeStart + 400]

sound1.export('speech1.wav',format='wav')
sound2.export('speech2.wav',format='wav')

duration_seconds = sound1.duration_seconds

sample_rate, data = wavfile.read('speech1.wav')
sample_rate2, data2 = wavfile.read('speech2.wav')

speech1 = []
for num in data: 
    speech1.append(abs(num / 1000))

speech2 = []
for num in data2:
    speech2.append(abs(num / 1000))

lags, coeff = xcorr(speech1, speech2, maxlags=len(speech1) - 1)

# Direction of arrival calculation
delay = (duration_seconds * lags[np.argmax(coeff)]) / len(speech1) / 20
c = 340 
d = 0.2 

print delay

doa = math.degrees(math.asin( (delay * c) / d ) )
print doa

if doa < 90:
    r = sr.Recognizer()
    with sr.WavFile(soundFileName1) as source:
        audio = r.record(source)

    text = r.recognize_google(audio)
    print text
else: 
    r = sr.Recognizer()
    with sr.WavFile(soundFileName2) as source:
        audio = r.record(source)
    
    text = r.recognize_google(audio)
    print text