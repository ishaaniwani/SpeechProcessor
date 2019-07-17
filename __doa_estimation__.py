import pydub
from __mic_array__ import MicrophoneArray
from __microphone__ import Microphone

soundFile1 = 'wavfiles/can_you_keep_a_secret.wav' 
soundFile2 = 'wavfiles/footsteps.wav'
soundFile3 = 'wavfiles/silence.wav'

mic1 = Microphone(4 , 4 , soundFile1)
mic2 = Microphone(6, 2, soundFile2)
mic3 = Microphone(2, 6, soundFile3)

mic_arr = MicrophoneArray([mic1 , mic2 , mic3])
angle = mic_arr.overallAngleEstimation()

print(angle)