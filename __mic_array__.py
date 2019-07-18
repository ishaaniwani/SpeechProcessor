import pydub
import math
from __microphone__ import Microphone


class MicrophoneArray(object):

    def __init__(self, mic_arr=[]):
        self.microphoneArray = mic_arr

    def add(self, sound):
        self.microphoneArray.append(sound)

    def getMaxDBFS(self):
        max = 0
        for i in range(len(self.microphoneArray)):
            if self.microphoneArray[i].getNormalizedDBFS() > self.microphoneArray[max].getNormalizedDBFS():
                max = i
        return max

    def getEstimatedAngle(self, max):
        return self.microphoneArray[max].angle

    def distance(self, mic1, mic2):
        return math.sqrt((mic2.x - mic1.x)**2 + (mic2.y - mic2.x)**2)

    def overallAngleEstimation(self):
        DOAs = []
        slicedSounds = [] 
        for i in range(len(self.microphoneArray)): 
            slicedSounds.append(self.microphoneArray[i].signal[::Microphone.CHUNK_MILLES])
        for i in range(len(slicedSounds)): 
            iDBFS = []
            for slicedSound in slicedSounds: 
                iDBFS.append(slicedSound[i])
            max = 0 
            for i in range(len(iDBFS)): 
                if iDBFS[i].dBFS > iDBFS[max].dBFS: 
                    max = i 
            self.quickSort(self.microphoneArray, 0 , len(self.microphoneArray) - 1, max)
            DOAs.append((1.0 * self.getEstimatedAngle(0) + 0.8 * self.getEstimatedAngle(1) + 0.6 * self.getEstimatedAngle(2)) / 3)
        return DOAs

    def partition(self, arr, low, high, maxIdx):
        i = (low-1)         # index of smaller element
        pivot = self.distance(arr[maxIdx] , arr[high])  # pivot

        for j in range(low, high):

            # If current element is smaller than or
            # equal to pivot
            if self.distance(arr[maxIdx] , arr[j]) <= pivot:

                # increment index of smaller element
                i = i+1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i+1], arr[high] = arr[high], arr[i+1]
        return (i+1)

    def quickSort(self,arr,low,high,maxIdx): 
        if low < high: 
  
            # pi is partitioning index, arr[p] is now 
            # at right place 
            pi = self.partition(arr,low,high, maxIdx) 
  
            # Separately sort elements before 
            # partition and after partition 
            self.quickSort(arr, low, pi-1 , maxIdx) 
            self.quickSort(arr, pi+1, high , maxIdx) 