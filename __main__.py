import speech_recognition as sr
from pydub import AudioSegment
from __audio_array__ import AudioArray

'''
Constructs AudioSegment objects 
'''
sound1 = AudioSegment.from_wav('wavfiles/can_you_keep_a_secret.wav')
sound2 = AudioSegment.from_wav('wavfiles/crowd_laugh.wav')
sound3 = AudioSegment.from_wav('wavfiles/footsteps.wav')

'''
Places AudioSegment objects into the wrapper class 
'''
sounds = AudioArray([sound1, sound2, sound3])

'''
Overlays signals without any processing to show what that is like 
'''
problem = sound1.overlay(sound2)
problem = problem.overlay(sound3)
problem.export('wavfiles/problem.wav', format='wav')

TDOA = sounds.calculatePhaseDifference(
    AudioSegment.from_wav('wavfiles/can_you_keep_a_secret.wav'),
    AudioSegment.from_wav('wavfiles/post_can_you_keep_it_a_secret.wav'))
print(TDOA)

'''
Processes and overlays the signals to show what the solution is like 
'''
solution = sounds.testOverlaySignals()
solution.export('wavfiles/solution.wav', format='wav')

''' Recognizing wav file (solution)'''
r = sr.Recognizer()
with sr.AudioFile('wavfiles/solution.wav') as source:
    audio = r.record(source)
    try:
        text = r.recognize_google(audio)
    except:
        text = 'Unable to recognize source'
print(text)
