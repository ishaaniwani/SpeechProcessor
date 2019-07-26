from pydub import AudioSegment
from vad import VoiceActivityDetector

sound = AudioSegment.from_wav('Test1-master/Test/mic1.wav')
slicedSounds = sound[::500]
slicedSounds = list(slicedSounds)

for i in range(0 , len(slicedSounds)):
    slicedSounds[i].export('trash.wav',format='wav')
    obj = VoiceActivityDetector('trash.wav')
    data = obj.detect_speech()
    Found = False
    for i in range(0 , len(data)): 
        if data[i][len(data[i]) - 1] == 1: 
            speech = AudioSegment.from_wav('trash.wav')
            speech.export('speech.wav',format='wav')
            Found = True
    if Found:
        break