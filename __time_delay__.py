# This is a demo program to calculate the phase difference between two audio files.
import wave
import math
import struct
from pydub import AudioSegment

DIFFERENCE_THRESHOLD = 10

def getAmplitudeList(fileName):

    amplitudeList = []

    waveFile = wave.open(fileName, 'r')
    length = waveFile.getnframes()
    for i in range(0, length):
        waveData = waveFile.readframes(1)
        data = struct.unpack("<h", waveData)
        amplitudeList.append(int(data[0]))

    return amplitudeList


def calculateTimeDelay(fileName1, fileName2):
    amplitudes1 = getAmplitudeList(fileName1)
    amplitudes2 = getAmplitudeList(fileName2)

    duration_seconds = AudioSegment.from_wav(fileName1).duration_seconds
    numFrames = len(amplitudes1)
    sampleRate = duration_seconds / numFrames

    for i in range(0 , numFrames):
        if amplitudes1[i] > 200 or amplitudes1[i] < -200: 
            frame1 = i        
            break 

    for i in range(0, numFrames):
        if (amplitudes2[i] - amplitudes2[frame1]) < DIFFERENCE_THRESHOLD: 
            frame2 = i
            break

    frameDiff = frame1 - frame2
    timeDelay = sampleRate * frameDiff
    return timeDelay

def doaEstimation(timeDelay):
    c = 340 
    distance = 3.4  
    Theta = math.sin( (timeDelay * c) / distance )
    Theta = math.degrees(Theta)
    return Theta 
    
# Recieved Signal representations
soundFileName1 = 'wavfiles/can_you_keep_a_secret.wav'
soundFileName2 = 'wavfiles/post_can_you_keep_a_secret.wav'

timeDelay = calculateTimeDelay(soundFileName1 , soundFileName2) 
Theta = doaEstimation(timeDelay)
print Theta 