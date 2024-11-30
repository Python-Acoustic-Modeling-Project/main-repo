# Import libraries
import librosa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, butter, lfilter
from scipy.io import wavfile
import soundfile as sf

# Model class
class Model:

    # Class initialization method
    def __init__(self):

        self.filepath = None
        self.samplerate = None
        self.data = None
        self.rt60_added = 0.0

    # Load audio
    def load_audio(self, filepath):
        
        """
        Load an audio file and store the sample rate and data.
        """
        self.filepath = self.convert_to_wave(filepath)
        self.samplerate, self.data = wavfile.read(self.filepath)
        self.spectrum, self.freq, self.t, self.im = plt.specgram(self.data, Fs=self.samplerate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
        self.file_format = "WAV"

    # Convert audio to WAV format
    def convert_to_wave(self, filepath):
        """
        Convert an audio file to WAV format if not already in that format.
        """
        if not filepath.lower().endswith(".wav"):  # if file format/extension is not .wav

            y, sr = librosa.load(filepath, sr=None)
            output_filepath = ".".join(filepath.split(".")[:-1]) + ".wav"
            sf.write(output_filepath, y, sr, format="wav")
            return output_filepath
        
        return filepath

    # Calculate RT60 values
    def calculate_rt60(self):
        """
        Estimate RT60 value for the currently loaded audio data.
        """

        if self.data is None:

            raise ValueError("No audio data loaded to analyze.")
        
        rt60= self.rt60_added / 3
        self.rt60_added = 0
        return rt60
    
    # Calculate resonant frequency
    def calculate_resonant_frequency(self):
        """
        Find the dominant resonant frequency of the loaded audio data.
        """

        if self.data is None:

            raise ValueError("No audio data loaded to analyze.")
        
        spectrum = np.abs(np.fft.rfft(self.data))
        freqs = np.fft.rfftfreq(len(self.data), 1 / self.samplerate)
        peak_idx = np.argmax(spectrum)
        return freqs[peak_idx]

    def find_target_frequency(self, limit):
        for x in self.freq:
            if x > limit:
                break
        return x

    def frequency_check(self, value):
        target_frequency = self.find_target_frequency(value)
        index_of_frequency = np.where(self.freq == target_frequency)[0][0]
        data_for_frequency = self.spectrum[index_of_frequency]

        try:
            data_in_db_fun = 10 * np.log10(data_for_frequency)
        except:
            pass

        return data_in_db_fun

    def find_nearest_value(self,array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    def rt60_visualization(self, value):
        """
        Find the data need for the visualization of the rt60 value at different frequencies.
        """

        data_in_db = self.frequency_check(value)

        # find max decidable value
        idx_max = np.argmax(data_in_db)
        max_dB = data_in_db[idx_max]

        # slice array from max value
        sliced_array = data_in_db[idx_max:]

        # max - 5 dB
        max_5 = max_dB - 5
        value_max_5 = self.find_nearest_value(sliced_array, max_5)
        idx_max_5 = np.where(data_in_db == value_max_5)

        # max - 25dB
        max_25 = max_dB - 25
        max_25 = self.find_nearest_value(sliced_array, max_25)
        idx_max_25 = np.where(data_in_db == max_25)

        # rt60 calculation at current frequency
        rt20 = (self.t[idx_max_5] - self.t[idx_max_25])[0]
        rt60 = abs(rt20 * 3)
        self.rt60_added += rt60

        # List to be returned storing the information needed to plot
        plot_info = [self.t, data_in_db, self.t[idx_max], self.t[idx_max_5], self.t[idx_max_25],\
                    data_in_db[idx_max], data_in_db[idx_max_5], data_in_db[idx_max_25]]
        return plot_info

