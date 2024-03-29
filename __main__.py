import speech_recognition as sr
from pydub import AudioSegment
from __mic_array__ import MicrophoneArray
from __microphone__ import Microphone

soundFile1 = 'wavfiles/awaiting.wav'
soundFile2 = 'wavfiles/awaiting.wav'
soundFile3 = 'wavfiles/awaiting.wav'
soundFile4 = 'wavfiles/awaiting.wav'

soundFile5 = 'wavfiles/awaiting.wav'
soundFile6 = 'wavfiles/awaiting.wav'
soundFile7 = 'wavfiles/awaiting.wav'
soundFile8 = 'wavfiles/awaiting.wav'

mic1 = Microphone(0.06914, 0.01095, soundFile1)
mic2 = Microphone(0.062375, 0.03177, soundFile2)
mic3 = Microphone(0.0495, 0.0495, soundFile3)
mic4 = Microphone(0.03178, 0.06237, soundFile4)

mic5 = Microphone(-0.06914, 0.01095, soundFile5)
mic6 = Microphone(-0.062375, 0.03177, soundFile6)
mic7 = Microphone(-0.0495, 0.0495, soundFile7)
mic8 = Microphone(-0.03178, 0.06237, soundFile8)

'''
Places AudioSegment objects into the wrapper class 
'''
mic_arr1 = MicrophoneArray([mic1, mic2, mic3, mic4])
mic_arr2 = MicrophoneArray([mic5, mic6, mic7, mic8])

circularMicrophoneArray = [mic_arr1, mic_arr2]


'''
Processes and overlays the signals to show what the solution is like 
'''
solution1 = mic_arr1.testOverlaySignals()
solution1.export('wavfiles/solution1.wav', format='wav')
angle1 = mic_arr1.overallAngleEstimation()

solution2 = mic_arr2.testOverlaySignals()
solution2.export('wavfiles/solution2.wav', format='wav')
angle2 = mic_arr2.overallAngleEstimation()

''' Recognizing wav file (solution)'''
r = sr.Recognizer()
with sr.AudioFile('wavfiles/solution1.wav') as source:
    audio = r.record(source)
    try:
        text1 = r.recognize_google(audio)
    except:
        text1 = 'Unable to recognize source'
print(text1)
print(angle1)

''' Recognizing wav file (solution)'''
r = sr.Recognizer()
with sr.AudioFile('wavfiles/solution2.wav') as source:
    audio = r.record(source)
    try:
        text2 = r.recognize_google(audio)
    except:
        text2 = 'Unable to recognize source'
print(text2)
print(angle2)
