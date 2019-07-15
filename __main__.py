import speech_recognition as sr
from pydub import AudioSegment
from sound import Sound

sound1 = Sound('wavfiles/you_got_it.wav')
sound2 = Sound('wavfiles/slap.wav')
sound3 = Sound('wavfiles/chicken.wav')

problem = sound1.wav.overlay(sound2.wav)
problem = problem.overlay(sound3.wav)
problem.export('wavfiles/problem.wav' , format = 'wav')

sounds = [sound1, sound2, sound3]

max = 0
for i in range(len(sounds)):
    if sounds[i].getNormalizedMeanAmplitude() > sounds[max].getNormalizedMeanAmplitude():
        max = i

print(max)

combinedSignal = sounds[max].wav
for sound in sounds:
    if sound is not sounds[max]:
        sound.wav = sound.wav - 20
        combinedSignal.overlay(sound.wav, loop = True)

combinedSignal.export('wavfiles/solution.wav' , format = 'wav')

''' Recognizing wav file '''
r = sr.Recognizer()
with sr.AudioFile('wavfiles/solution.wav') as source:
    audio = r.record(source)
    try:
        text = r.recognize_google(audio)
    except:
        text = 'Unable to recognize source'
print(text)
