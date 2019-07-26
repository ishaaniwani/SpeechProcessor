import speech_recognition as sr
import numpy as np 
from vad import VoiceActivityDetector
from pydub import AudioSegment

sound = AudioSegment.from_wav('WavFileDatabase/Data1/mic2.wav')
slicedSounds = sound[::500]
slicedSounds = list(slicedSounds)
for i in range(0 , len(slicedSounds)):
    slicedSounds[i].export('trash.wav',format='wav')
    obj = VoiceActivityDetector('trash.wav')
    data = obj.detect_speech()
    weights = []
    for i in range(0 , len(data)): 
        if data[i][len(data[i]) - 1] == 1: 
            print(1)
            break 
    print(0)

r = sr.Recognizer()
with sr.WavFile('WavFileDatabase/Data1/mic1.wav') as source:
    audio = r.record(source)

    text = r.recognize_google(audio)
print(text)