import librosa
import soundfile as sf
import numpy as np
from scipy.io import wavfile

# Converts the given audio file to a .wav
# Returns the new .wav filepath
def convert_to_wav(audio_filepath):
    if not audio_filepath.lower().endswith(".wav"):
        y, sr = librosa.load(audio_filepath, sr=None)
        output_filepath = ".".join(audio_filepath.split(".")[:-1]) + ".wav"
        sf.write(output_filepath, y, sr, format="wav")

    return output_filepath

# This reads the given audio file
# Returns a tuple (samplerate, audio_data)
def load_audio_file(audio_filepath):
    # Converts audio file to .wav if necessary
    audio_filepath = convert_to_wav(audio_filepath)

    # Read the wav file
    samplerate, audio_data = wavfile.read(audio_filepath)

    return samplerate, audio_data

# Combines multi-channel audio data into single-channel audio data
# Returns the single-channel audio data
def combine_multi_channel_audio(audio_data):
    # Check that there is multiple channels
    if data.shape[1] > 1:
        single_channel_data = np.mean(audio_data, axis=1, dtype=np.int16)
        return single_channel_data

    # Return the input audio data if there is only one channel
    return audio_data

# Cleans the audio data and removes meta-data
# Returns the data without meta tags
# TODO: IMPLEMENT THIS FUNCTION
def remove_metatags(samplerate, audio_data):
    pass

# Returns the length in seconds of the given audio
def length_of_audio(samplerate, audio_data):
    return audio_data.shape[0] / samplerate

