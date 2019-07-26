from pydub import AudioSegment
from vad import VoiceActivityDetector
import webrtcvad 
import wave 
import scipy.io.wavfile as wavfile

def read_wave(path):
    """Reads a .wav file.

    Takes the path, and returns (PCM audio data, sample rate).
    """
    wf = wave.open(path, 'rb')
    sample_rate = wf.getframerate()
    pcm_data = wf.readframes(wf.getnframes())
    wf.close()
    return pcm_data, sample_rate


def write_wave(path, audio, sample_rate):
    """Writes a .wav file.

    Takes path, PCM audio data, and sample rate.
    """
    wavfile.write(path, sample_rate, audio)

soundFileLocation = 'mic1.wav'

# Sample wav file at an acceptable frequency
rate, data = wavfile.read(soundFileLocation)
write_wave(soundFileLocation, data, 32000)
sound = AudioSegment.from_wav(soundFileLocation)
sound.export(soundFileLocation, format='wav')

# Split wav file into segments of 30 milleseconds
slicedSounds = sound[::30]
slicedSounds = list(slicedSounds)

for i in range(0, len(slicedSounds)):
    speechFileLocation = 'new_speech.wav'
    slicedSounds[i].export(speechFileLocation, format='wav')
    vad = webrtcvad.Vad()
    rate, data = wavfile.read(speechFileLocation)
    speech = vad.is_speech()
    break

'''
for i in range(0, len(slicedSounds)):
    print i
    speechFileLocation = 'new_speech.wav'
    slicedSounds[i].export(speechFileLocation,format='wav')
    VAD = VoiceActivityDetector(speechFileLocation)
    speech_data = VAD.detect_speech()
    Found = False
    for arr in speech_data:
        if arr[len(arr) - 1] == 1:
            Found = True
            break
    if Found:
        break
'''