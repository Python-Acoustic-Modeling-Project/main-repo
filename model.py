# Import libraries
import librosa
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.io import wavfile
import soundfile as sf

# Model class
class Model:

    # Class initialization method
    def __init__(self):

        self.filepath = None
        self.samplerate = None
        self.data = None

    # Load audio
    def load_audio(self, filepath):
        
        """
        Load an audio file and store the sample rate and data.
        """
        self.filepath = self.convert_to_wave(filepath)
        self.samplerate, self.data = wavfile.read(self.filepath)

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
    
    # Clean audio
    def clean_audio(self):
        """
        Clean the loaded audio date (remove metadata, combine channels).
        """
        if self.data is None:

            raise ValueError("No audio data loaded to clean.")
        
        if(len(self.data.shape) > 1):  # if stereo

            self.data = np.mean(self.data, axis=1).astype(np.int16)

    # Calculate RT60 values
    def calculate_rt60(self):
        """
        Estimate RT60 value for the currently loaded audio data.
        """

        if self.data is None:

            raise ValueError("No audio data loaded to analyze.")
        
        energy = np.cumsum(self.data[::-1] ** 2)[::-1]
        max_energy = energy[0]
        rt60 = np.where(energy < max_energy * 0.001)[0][0] / self.samplerate
        return rt60
    
    # Calculate resonant frequency
    def calculate_resnonant_frequency(self):
        """
        Find the dominant resonant frequency of the loaded audio data.
        """

        if self.data is None:

            raise ValueError("No audio data loaded to analyze.")
        
        spectrum = np.abs(np.fft.rfft(self.data))
        freqs = np.fft.rfftfreq(len(self.data), 1 / self.samplerate)
        peak_idx = np.argmax(spectrum)
        return freqs[peak_idx]
    
    # Visualize waveform
    def visualize_waveform(self):
        """
        Create and display a waveform plot of the loaded audio data.
        """

        if self.data is None:

            raise ValueError("No audio data loaded to visualize.")
        
        time = np.linespace(0, len(self.data) / self.samplerate, num=len(self.data))
        plt.figure()
        plt.plot(time, self.data)
        plt.title("Waveform")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.show()

    # Visualize RT60 bands
    def visualize_rt60_bands(self, bands):
        """
        Visualize RT60 values across specified frequency bands.
        """

        if self.data is None:

            raise ValueError("No audio data loaded to analyze.")
        
        # Declare empty list for RT60 bands
        rt60s = []

        # Iterate through bands, calculate RT60, and add to list
        for band in bands:

            band_data = self.data
            rt60s.append(self.calculate_rt60())

        plt.bar([f"{band[0]}-{band[1]} Hz" for band in bands], rt60s)
        plt.title("RT60 by Frequency Band")
        plt.xlabel("Frequency Band (Hz)")
        plt.ylabel("RT60 (s)")
        plt.show()