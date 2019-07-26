from __future__ import division
from pydub import AudioSegment
from xcorr import xcorr
import docopt
import scipy.io.wavfile as wavfile
import scipy
import numpy as np
from speech_recognition.vad import VoiceActivityDetector
import wave
import struct
from scikits import audiolab
import soundfile as sf

def read_wave(file_name):
    #Reads a .wav file.
    #Takes the path, and returns (PCM audio data, sample rate).
    sample_rate, pcm_data = wavfile.read(file_name) 
    return sample_rate, pcm_data

def write_wave(file_name, sample_rate, pcm_data):
    # Writes a .wav file.
    # Takes path, PCM audio data, and sample rate.
    wavfile.write(file_name, sample_rate, pcm_data)

def calculate_mean_frequency(y, fs):
    """
    Compute mean frequency

    :param y: 1-d signal
    :param fs: sampling frequency [Hz]
    :return: mean frequency
    """
    spec = np.abs(np.fft.rfft(y))
    freq = np.fft.rfftfreq(len(y), d=1/fs)    
    amp = spec / spec.sum()
    mean = (freq * amp).sum()
    return mean 

sound_file_1 = 'WavFileDatabase/Data2/mic1.wav'
sound_file_2 = 'wavFileDatabase/Data2/mic2.wav'

# Downsampled version of the sound file - so it can be processed by VAD
sample_rate, pcm_data = read_wave(sound_file_1)
write_wave('experiment/test1.wav', 32000, pcm_data) 

sample_rate2, pcm_data2 = read_wave(sound_file_2)
write_wave('experiment/test2.wav', 32000, pcm_data)

# Splits sound file into 40 millesecond chunks of the audio file 
audio = AudioSegment.from_wav('experiment/test1.wav')
audio2 = AudioSegment.from_wav('experiment/test2.wav')
slicedSounds = audio[::40]
slicedSounds = list(slicedSounds)

speechTimeStart = 0
j = 0

# If the current splicedSounds has voice, then get the next 500 milleseconds and export it
for i in range(0 , len(slicedSounds)):
    # Exports AudioSegment object to an actual wav file so that VAD can detect if there is speech
    slicedSounds[i].export('experiment/holder.wav', format='wav')
    obj = VoiceActivityDetector('experiment/holder.wav')
    speech_data = obj.detect_speech() 
    Found = False
    speech = None
    speech2 = None
    speech_data = np.asarray(speech_data)
    # If there is speech inside 
    for array in speech_data: 
        if speech_data[0 , speech_data[0].size - 1] == 1 or speech_data[1 , speech_data[0].size - 1] == 1:
            speechTimeStart = i * 40
            if speechTimeStart + 500 < audio.duration_seconds * 500:
                speech = audio[speechTimeStart:speechTimeStart + 500]
                speech2 = audio2[speechTimeStart:speechTimeStart + 500]
            else: 
                speech = audio[speechTimeStart:((audio.duration_seconds * 1000) - 1)]
                speech2 = audio2[speechTimeStart:((audio.duration_seconds * 1000) - 1)]
            j = i
            Found = True
            break
    if Found == True:
        break

speech.export('file1.wav', format='wav')
speech2.export('file2.wav', format='wav')

sample_rate, pcm_data = read_wave('file1.wav')
slicedData = pcm_data[::3]

arr_freq = []
for data_slice in slicedData: 
    data_slice = np.asarray(data_slice)
    mean_freq = calculate_mean_frequency(data_slice, sample_rate)
    mean_freq = int(mean_freq * (10**3)) / 10**3
    arr_freq.append(mean_freq)

sample_rate, pcm_data = read_wave('file2.wav')
slicedData = pcm_data[::3]

arr_freq1 = []
for data_slice in slicedData:
    data_slice = np.asarray(data_slice)
    mean_freq = calculate_mean_frequency(data_slice, sample_rate)
    mean_freq = int(mean_freq * (10**3)) / 10**3
    arr_freq1.append(mean_freq)

print arr_freq[::50]
print arr_freq1[::50]

'''
speech.set_channels(1)
speech2.set_channels(1)

speech_data1 = AudioSegment.getSampleArray(speech2)


amp_arr = []
array = AudioSegment.getSampleArray(speech)
for num in array: 
    amp_arr.append(int(num/10))

amp_arr1 = []
array = AudioSegment.getSampleArray(speech2)
for num in array:  
    amp_arr1.append(int(num/10))

print amp_arr[0:50]
print '------'
print amp_arr1[0:50]
'''