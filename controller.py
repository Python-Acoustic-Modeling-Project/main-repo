# Include libraries
import os
import pygame
from model import Model
from view import View
import soundfile as sf
import librosa

# Controller class
class Controller:

    # Class initialization
    def __init__(self, root, model):
        """
        Initialize the controller, linking the model and the view.
        """

        # Set instance variables
        self.root = root
        self.model = model
        self.view = None
        self.is_playing = False

        # Initalize pygame mixer for audio playback
        pygame.mixer.init()

    # Set view
    def set_view(self, view):

        self.view = view
    
    # Load file
    def load_file(self, filepath):
        """
        Handles file loading via the model.
        """

        # Handle if a filepath does not exist
        if not os.path.exists(filepath):

            # Raise FileNotFound exception
            raise FileNotFoundError("The selected file does not exist.")
        
        # Otherwise, load the file via the filepath
        self.model.load_audio(filepath)
    
    # Clean data
    def clean_data(self):
        """
        Handles data cleaning via the model.
        Converts non-WAV files to WAV format and processes metadata.
        """

        # Convert audio file to WAV if not already in that format
        if self.model.file_format != "WAV":
            
            # Convert file to WAV
            new_file = self.model.convert_to_wave(self.model.filepath)

            # Load newly-converted WAV audio file
            self.model.load_audio(new_file)

    # Analyze data
    def analyze_data(self):
        """
        Performs audio analysis using the model and returns the results.
        """

        # Ensure audio data is loaded
        if self.model.data is None:

            raise ValueError("No audio data loaded. Please load an audio file first.")
        
        # Perform analysis
        results = {
            "length": len(self.model.data) / self.model.samplerate,
            "rt60": self.model.calculate_rt60(),
            "resonant_frequency": self.model.calculate_resonant_frequency(),
            "waveform": self.model.data,
            "rt60_low": self.model.rt60_visualization(5),
            "rt60_mid": self.model.rt60_visualization(1000),
            "rt60_high": self.model.rt60_visualization(5000)
        }

        # Return results
        return results
    
    # Play audio
    def play_audio(self):
        """
        Play the audio through pygame.
        """

        if not self.is_playing:  # if audio is not playing

            pygame.mixer.music.load(self.model.filepath)
            pygame.mixer.music.play()
            self.is_playing = True

    # Stop audio
    def stop_audio(self):
        """
        Stop the audio if it is playing.
        """

        if self.is_playing:  # if audio is playing

            pygame.mixer.music.stop()
            self.is_playing = False