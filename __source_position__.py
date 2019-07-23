from __microphone_pair__ import MicrophonePair
from __microphone__ import Microphone 

mic1 = Microphone(0 , 0 , 'wavfiles/can_you_keep_a_secret.wav')
mic2 = Microphone(3.4 , 0 , 'wavfiles/post_can_you_keep_a_secret.wav')

micPair = MicrophonePair(mic1 , mic2)
phaseDiff = micPair.calculatePhaseDifference()
timeDelay = micPair.calculateTimeDelay()
print(timeDelay)
print(phaseDiff)