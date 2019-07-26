from __microphone__ import Microphone 
from __microphone_pair__ import MicrophonePair
from speech_recognition.vad import VoiceActivityDetector
from xcorr import xcorr 

mic1 = Microphone(0 , 0 , 'WavFileDatabase/Data1/mic1.wav')
mic2 = Microphone(0.15 , 0 , 'WavFileDatabase/Data1/mic2.wav')

amp1 = mic1.getSpeechSoundAmplitudeList()